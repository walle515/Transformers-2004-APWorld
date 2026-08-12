import struct
#from pwd import struct_passwd

from Scripts.pine import Pine, pcsx2
from Data.tf_data import add_minicon
from enum import IntEnum
from Scripts.mips_mods import MipsMod
import asyncio

class GameAddress(IntEnum):
    gameadd_minicon_unlocks = 0x7173C0
    gameadd_level_unlocks = 0x717114 #episode length = 0x4C
    gameadd_episode_function = 0x351B0C

class CleanAddress(IntEnum):
    cleanadd_level_unlocked = 0x1FAED00
    cleanadd_pickup_code = 0x1FAECE0

class PineCommand(IntEnum):
    comm_nothing = 0
    comm_get_health = 1
    comm_set_health = 2
    comm_get_game_id = 3
    comm_status = 4
    comm_exit = 5
    comm_unlock_minicon = 6
    comm_apply_mod = 7
    comm_read_location = 8

def raw_bytes_to_float(read_output: int) -> float:
    return struct.unpack("<f", struct.pack("<I", read_output))[0]

def get_location_id(read_values: list[int]) -> int:
    '''Location IDs are written to the game by Exodus using the 4 values of its orientation,
    since this conveniently lets us get all 4 digits. However, in order to not make the camera
    cutscenes absolutely horrible, we have to scale down those digits within the quaternion.
    So, each digit is stored in the hundreths place in-game. When we extract them, we need to
    multiply them back to their correct place.

    If this seems a bit convoluted, it might be. I like it though.
    '''
    factor = 100000
    location_value = 0
    rounding_place = -3
    for value in read_values:
        float_value = raw_bytes_to_float(value)
        if float_value > 1:
            #this accounts for the scalar value, which needs to be approximately 1.
            #in an ideal world, we would subtract the modified ID from this instead of adding it
            float_value -= 1
        rounded_float = round(float_value*factor, rounding_place)
        location_value += int(rounded_float)
        factor /= 10
        rounding_place += 1
    return location_value

def get_user_command() -> tuple[PineCommand, ...]:
    user_input = input('\n> ')

    command_list = user_input.split()
    command = command_list[0]
    if len(command_list) > 1:
        args = command_list[1]
    else:
        args = None

    if command == "get_health":
        return(PineCommand.comm_get_health,)

    if command == "get_game_id":
        return(PineCommand.comm_get_game_id,)

    if command == "status":
        return(PineCommand.comm_status,)

    if command == "exit":
        return(PineCommand.comm_exit,)

    if command == "set_health":
        value: float = float(args)
        return(PineCommand.comm_set_health, value,)

    if command == "minicon":
        return(PineCommand.comm_unlock_minicon, args,)

    if command == "mod":
        return(PineCommand.comm_apply_mod, args,)

def read_target_addresses() -> tuple[PineCommand, ...]:
    minicon_unlocks = pcsx2.read_int32(GameAddress.gameadd_minicon_unlocks)
    if minicon_unlocks & 0x1000: #0x1000 is Endgame
        print("Archipelago item pickup detected.")
        pcsx2.write_int32(GameAddress.gameadd_minicon_unlocks, minicon_unlocks ^ 0x1000)
        pickup_instance = pcsx2.read_int32(0x01FAECD0)
        #we also need to decrease the minicon collection count for the current level
        #TODO: make command execution its own function instead of relying on the monitor_ram loop
        return (PineCommand.comm_read_location, pickup_instance,)
    level_unlocks = pcsx2.read_int32(CleanAddress.cleanadd_level_unlocked)
    if level_unlocks != 0:
        #for now, just unlocking the next episode and reset the bit
        unlock_episode(level_unlocks + 1)
        pcsx2.write_int32(CleanAddress.cleanadd_level_unlocked, 0)
    return (PineCommand.comm_nothing,)

def write_initial_values():
    '''Sets values in RAM and single-line ELF codes to allow Archipelago randomizers to work'''

    #increase PickupPlaced limit to 20 (0x14)
    pcsx2.write_int32(0x379534,0x2A230014)

    #write pickup redirection code (this will be replaced with a mod file once functionality is verified)
    pcsx2.write_int32(0x37BBA4, 0x0C7EBB38)
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_code, 0x3C0201FB)
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_code+0x4, 0x2442ECD0)
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_code+0x8, 0xAC440000)
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_code+0xC, 0x03E00008)
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_code+0x10, 0x0080882D)

    #This line stops the SetEpisodeCompleted function from unlocking the next episode
    #all of the code from 0x351B10 to 0x351B9C is free to use, since the code in this range is ignored by us.
    #pcsx2.write_int32(0x00351B0C, 0x10000024) #single-line mod to just skip the unlock of the next episode
    #write the index of the current episode to 0x0x1FAED00, then skip to the next part of the function
    pcsx2.write_int32(GameAddress.gameadd_episode_function, 0x3C0201FB)
    pcsx2.write_int32(GameAddress.gameadd_episode_function+0x4, 0x2442ED00)
    pcsx2.write_int32(GameAddress.gameadd_episode_function+0x8, 0xAC450000)
    pcsx2.write_int32(GameAddress.gameadd_episode_function+0xC, 0x10000021)
    pcsx2.write_int32(GameAddress.gameadd_episode_function+0x10, 0xAC830034)

def unlock_episode(episode_id: int):
    #using the ID, set the level to Available and the first warpgate to Unlocked
    if episode_id > 7 or episode_id < 0:
        #invalid episode ID. No can do
        print("Invalid episode ID " + str(episode_id) + " provided.")
    episode_offset = episode_id * 0x4C
    unlock_byte = pcsx2.read_int32(GameAddress.gameadd_level_unlocks + episode_offset)
    print("Unlock byte read as " + str(unlock_byte))
    if unlock_byte & 0x1:
        print("Level " + str(episode_id) + " is already unlocked.")
    else:
        unlock_byte ^= 0x1
        pcsx2.write_int32(GameAddress.gameadd_level_unlocks + episode_offset, unlock_byte)
        pcsx2.write_int32(GameAddress.gameadd_level_unlocks + episode_offset + 4, 0x2) #unlock the first warpgate

async def monitor_ram():
    print("Starting PCSX2 RAM monitor.")
    pcsx2.connect()
    write_initial_values()
    while True:
        mode = 'Auto' #'Manual' #
        if mode == 'Manual':
            command = get_user_command()
        else:
            command = read_target_addresses()

        if command[0] == PineCommand.comm_get_health:
            address: int = 0x00716FB4
            health_raw = pcsx2.read_int32(address)
            print(raw_bytes_to_float(health_raw))

        if command[0] == PineCommand.comm_get_game_id:
            print(pcsx2.get_game_id())

        if command[0] == PineCommand.comm_status:
            print(pcsx2.is_connected())

        if command[0] == PineCommand.comm_exit:
            pcsx2.disconnect()
            break

        '''The following commands take arguements, we should probably have verification checks on them that the tuple is as long as we expect.
        '''
        if command[0] == PineCommand.comm_set_health:
            if len(command) != 2:
                continue
            address: int = 0x00716FB4
            value: float = float(command[1])

            pcsx2.write_float(address, value)

            print(f'Set health to {command[1]}')

        if command[0] == PineCommand.comm_unlock_minicon:
            add_minicon(command[1])

        if command[0] == PineCommand.comm_read_location:
            read_values = []
            #first arg should be the address of the taPickupPlaced instance. The orientation is at 0x50 from it
            read_values.append(pcsx2.read_int32(command[1]+0x5C))
            read_values.append(pcsx2.read_int32(command[1]+0x50))
            read_values.append(pcsx2.read_int32(command[1]+0x54))
            read_values.append(pcsx2.read_int32(command[1]+0x58))
            location = get_location_id(read_values)
            print("Location ID read as: " + str(location) + ". Send to Archipelago.")

#asyncio.run(monitor_ram()) #used for testing