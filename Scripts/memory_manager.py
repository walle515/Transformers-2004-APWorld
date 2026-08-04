import struct
from pwd import struct_passwd

from Scripts.pine import Pine, pcsx2
from Data.tf_data import add_minicon
from enum import Enum
from Scripts.mips_mods import MipsMod
import asyncio

class PineCommand(Enum):
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
    for value in read_values:
        float_value = raw_bytes_to_float(value)
        if float_value > 1:
            #this accounts for the scalar value, which needs to be approximately 1.
            #in an ideal world, we would subtract the modified ID from this instead of adding it
            float_value -= 1
        location_value += int(float_value*factor)
        factor /= 10
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
    minicon_unlocks = pcsx2.read_int32(0x007173C0)
    if minicon_unlocks & 0x1000: #0x1000 is Endgame
        print("Archipelago item pickup detected.")
        pcsx2.write_int32(0x007173C0, minicon_unlocks ^ 0x1000)
        pickup_instance = pcsx2.read_int32(0x01FAECD0)
        return (PineCommand.comm_read_location, pickup_instance,)
    return (PineCommand.comm_nothing,)

async def monitor_ram():
    print("Starting PCSX2 RAM monitor.")
    pcsx2.connect()
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
            read_values.append(pcsx2.read_int32(command[1]+80))
            read_values.append(pcsx2.read_int32(command[1]+84))
            read_values.append(pcsx2.read_int32(command[1]+88))
            read_values.append(pcsx2.read_int32(command[1]+92))
            location = get_location_id(read_values)
            print("Location ID read as: " + str(location) + ". Send to Archipelago.")