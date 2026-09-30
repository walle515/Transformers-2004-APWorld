import struct

from .pine import Pine, pcsx2
from ..data.tf_data import minicon_ids
from enum import IntEnum
from .mips_mods import MipsMod
import asyncio
#from ..client.tf04_client import Transformers04Context as TFContext
from ..database import game_codes
from .. import database

'''Most of this file should be self-contained. If everything is set up correctly, the only things that 
should be needed from outside are:
The PineCommand enum
execute_command(tuple[PineCommand, params,])
monitor_ram()
the checked_locations list, just to populate its values.'''

#The checked_locations list should be populated from Archipelago on connection to the server to keep our
# local checks in sync. TODO: Populate this list on connection
checked_locations: list[int] = []


pine_is_connected = False
player_in_HQ = False
# list of unhandled locations. Kept out of context incase there is some issue when someone leaves
# the game and returns later to a lost save or something.
unhandled_locations: list[int] = []

'''-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
This section defines enum values that can be easilly passed around functions instead of having to 
refer to values directly
'''

class GameAddress(IntEnum):
    gameadd_minicon_unlocks = 0x7173C0 #64-bit integer
    gameadd_datacon_unlocks = 0x7170E0 #64-bit integer
    gameadd_level_unlocks = 0x717114 #episode length = 0x4C #717110 is the radio transmission byte. bit 0 unlocks the sidekick
    gameadd_episode_function = 0x351B0C
    gameadd_pickup_spawn_check = 0x379EF8
    gameadd_cheats = 0x8F0480
    gameadd_mission_status = 0x0716FA8
    gameadd_player_health = 0x00716FB4
    gameadd_player_max_health = 0x00716FB4 + 8
    gameadd_HQ_check = 0x7160EC #technically a count of loaded music files. HQ only has one, all other areas have more

class CleanAddress(IntEnum):
    cleanadd_pickup_code = 0x1FAECE0
    cleanadd_level_unlocked = 0x1FAED00
    cleanadd_pickup_spawn_replacement = 0x1FAEE00 #leaving plenty of space for the previous section

class PineCommand(IntEnum):
    comm_nothing = 0
    comm_get_health = 1
    comm_set_health = 2 #one arg, float, health value
    comm_get_game_id = 3
    comm_status = 4
    comm_exit = 5
    comm_unlock_minicon = 6 #one arg, string, minicon name (refer to Data.tf_data.py)
    comm_apply_mod = 7
    comm_read_location = 8 #one arg, int, address of taPickupPlaced instance
    comm_check_spawn = 9 #one arg, int, address of taPickupPlaced instance
    comm_unlock_episode = 10 #one arg, int, episode ID
    comm_set_max_health = 11
    comm_unlock_sidekick = 12
    comm_complete_episode = 13

class CheatIndex(IntEnum):
    cheat_reset = 0
    cheat_tractor = 0x15
    cheat_powerlink = 0x16
    cheat_immortal = 0x19
    cheat_oneshot = 0x1A
    cheat_enemystealth = 0x1B
    cheat_bighead = 0x1C
    cheat_turbo = 0x1D

class MissionStatus(IntEnum):
    status_normal = 0
    status_stasis_lock = 2
    status_HQ_warp = 3
    status_freeze = 5

'''-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
End Enums
-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~'''
def send_location(location_id: int):
    if location_id in database.Linked_Locations:
        location_id = database.Linked_Locations[location_id]
        
    unhandled_locations.append(location_id)     # adds location ID to list


def raw_bytes_to_float(read_output: int) -> float:
    #helper function for converting byte data from PCSX2's RAM to a float value
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
        if float_value >= 1:
            #this accounts for the scalar value, which needs to be approximately 1.
            #in an ideal world, we would subtract the modified ID from this instead of adding it
            float_value -= 1
        rounded_float = round(float_value*factor, rounding_place)
        location_value += int(rounded_float)
        factor /= 10
        rounding_place += 1
    return location_value


def read_pickup_location(target_address: int, context):
    # Using the modified code from write_initial_values, the game will write the pickup's unique ID to the
    # clean region in RAM. This then reads that data, processes it, and returns the location
    # ID as an int value
    read_values = []
    # first arg should be the address of the taPickupPlaced instance. The orientation is at 0x50 from it
    read_values.append(pcsx2.read_int32(target_address + 0x5C))
    read_values.append(pcsx2.read_int32(target_address + 0x50))
    read_values.append(pcsx2.read_int32(target_address + 0x54))
    read_values.append(pcsx2.read_int32(target_address + 0x58))
    pcsx2.write_int32(target_address+0x5C, 0)
    pcsx2.write_int32(target_address+0x50, 0x3F800000)
    pcsx2.write_int32(target_address+0x54, 0)
    pcsx2.write_int32(target_address+0x58, 0)
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_code - 0x8, 0x1) #write process complete
    location = get_location_id(read_values)
    checked_locations.append(location)
    print("Location ID read as: " + str(location) + ". Send to Archipelago.")
    context.output("Location ID read as: " + str(location) + ". Send to Archipelago.")
    send_location(location)
    return location


def cheat_toggle(cheat_index: int, cheat_state: bool):
    #Used by effects.py to directly toggle a cheat's bit value to active or inactive
    if cheat_index == 0:
        #reset all valid cheat indecies. Since I have this set up as an enum, there's not a clean way to do this (that I know of)
        #an arguement could be made that a dict would be better here.
        pcsx2.write_int8(GameAddress.gameadd_cheats + CheatIndex.cheat_tractor, 0)
        pcsx2.write_int8(GameAddress.gameadd_cheats + CheatIndex.cheat_powerlink, 0)
        pcsx2.write_int8(GameAddress.gameadd_cheats + CheatIndex.cheat_immortal, 0)
        pcsx2.write_int8(GameAddress.gameadd_cheats + CheatIndex.cheat_oneshot, 0)
        pcsx2.write_int8(GameAddress.gameadd_cheats + CheatIndex.cheat_enemystealth, 0)
        pcsx2.write_int8(GameAddress.gameadd_cheats + CheatIndex.cheat_bighead, 0)
        pcsx2.write_int8(GameAddress.gameadd_cheats + CheatIndex.cheat_turbo, 0)
    else:
        pcsx2.write_int8(GameAddress.gameadd_cheats + cheat_index + 0x34, cheat_state)


def set_mission_status(status_index: int):
    #Used by effects.py to directly set the mission status bit
    pcsx2.write_int32(GameAddress.gameadd_mission_status, status_index)


def write_initial_values():
    '''Sets values in RAM and single-line ELF codes to allow Archipelago randomizers to work
    this can be replaced with mod files once their functionality is verified. For now I haven't done that,
    since this is already reliable'''

    #increase PickupPlaced limit to 20 (0x14)
    pcsx2.write_int32(0x379534,0x2A230014)

    #Fix Slipstream pickup (remove check for special camera script)
    pcsx2.write_int32(0x37BC3C, 0x10000014) 

    #write pickup redirection code
    pcsx2.write_int32(0x37DCC0, 0x0C7EBB38)
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_code, 0x3C0201FB) #lui v0,0x01FB
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_code+0x4, 0x2442ECD0) #addiu v0,v0,-0x1330
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_code+0x8, 0xAC440000) #sw a0,0x0(v0) <- loop to here
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_code+0xC, 0x8C510008) #lw s1,0x8(v0)
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_code+0x10, 0x1220FFFD) # beqz s1 
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_code+0x14, 0) # NOP 
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_code+0x18, 0x03E00008) #jr ra
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_code+0x1C, 0x0080882D) #daddu s1,a0,zero

    #This line stops the SetEpisodeCompleted function from unlocking the next episode
    #all of the code from 0x351B10 to 0x351B9C is free to use, since the code in this range is ignored by us.
    #pcsx2.write_int32(0x00351B0C, 0x10000024) #single-line mod to just skip the unlock of the next episode
    #write the index of the current episode to 0x0x1FAED00, then skip to the next part of the function
    pcsx2.write_int32(GameAddress.gameadd_episode_function, 0x3C0201FB) #lui v0,0x01FB
    pcsx2.write_int32(GameAddress.gameadd_episode_function+0x4, 0x2442ED00) #addiu v0,v0,-0x1300
    pcsx2.write_int32(GameAddress.gameadd_episode_function+0xC, 0xAC420000) #sw v0,0x0(v0)
    pcsx2.write_int32(GameAddress.gameadd_episode_function+0x8, 0xAC450004) #sw a1,0x4(v0)
    pcsx2.write_int32(GameAddress.gameadd_episode_function+0x10, 0x10000021) #beq zero,zero,0x00351BA0
    pcsx2.write_int32(GameAddress.gameadd_episode_function+0x14, 0xAC830034) #sw v1,0x34(a0)

    #During the taPickupPlaced::Spawn function, there is a check to see if the pickup has already been unlocked
    #OLD CODE: (since we use the same minicon for multiple pickups, we need to adjust this function to also check if
    #the minicon was an Archipelago pickup. This means the game will have to wait on a response from Archi)
    #NEW CODE: Since Archipelago should be our sole arbiter of what has and hasn't been collected, we remove this check
    #entirely and replace it with our own. The game will still need to wait on a response from Archi.

    #These replace the check for Minicon locations
    pcsx2.write_int32(GameAddress.gameadd_pickup_spawn_check, 0x0C7EBB80) #jal 0x1FAEE00
    pcsx2.write_int32(GameAddress.gameadd_pickup_spawn_check+0x4, 0x0) 

    #These replace the check for Datacon locations
    pcsx2.write_int32(GameAddress.gameadd_pickup_spawn_check+0xB0, 0x0C7EBB80) #jal 0x1FAEE00
    pcsx2.write_int32(GameAddress.gameadd_pickup_spawn_check+0xB4, 0x0)
    # s2 = pointer to current pickupplaced object
    # v0 is safe
    # s0 = current minicon ID, or current datacon

    pcsx2.write_int32(CleanAddress.cleanadd_pickup_spawn_replacement, 0x0000802D) # daddu s0, zero, zero #at this point, s0 is safe. we can use it to load the current location
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_spawn_replacement+0x4, 0x3C0201FB) # lui v0, 1FB 
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_spawn_replacement+0x8, 0x2442EDF4) # addiu v0, EDF4 #Set target read location to 1FAEDE0
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_spawn_replacement+0xC, 0xAC400004) # sw zero, 4(v0) #reset the process complete
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_spawn_replacement+0x10, 0xAC520000) # sw s2, 0(v0) <- loop to here #store the current pickup pointer for Archi to grab
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_spawn_replacement+0x14, 0x8C500004) # lw s0 4(v0) #when the client processes the s2 value, write the pass/fail at v0+8 and the process complete at v0+4
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_spawn_replacement+0x18, 0x1200FFFD) # beqz s0 <- loop from here
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_spawn_replacement+0x1C, 0x8C430008) # lw v1 8(v0) #read the result into v1
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_spawn_replacement+0x20, 0x03E00008) # jr ra
    # NOP (don't need to write this, it's already there)
    
    #set amazon locked at start, Archipelago will unlock start level
    pcsx2.write_int32(GameAddress.gameadd_level_unlocks,0x0)
    pcsx2.write_int32(GameAddress.gameadd_level_unlocks + 4, 0x0)

def unlock_episode(episode_id: int, context):
    #using the ID, set the level to Available and the first warpgate to Unlocked
    if episode_id > 7 or episode_id < 0:
        #invalid episode ID. No can do
        print("Invalid episode ID " + str(episode_id) + " provided.")
        context.output("Invalid episode ID " + str(episode_id) + " provided.")
        return
    episode_offset = episode_id * 0x4C
    unlock_byte = pcsx2.read_int32(GameAddress.gameadd_level_unlocks + episode_offset)
    print("Unlock byte read as " + hex(unlock_byte) + " at address " + hex(GameAddress.gameadd_level_unlocks + episode_offset))
    context.output("Unlock byte read as " + hex(unlock_byte) + " at address " + hex(GameAddress.gameadd_level_unlocks + episode_offset))
    if unlock_byte & 0x1:
        print("Level " + str(episode_id) + " is already unlocked.")
        context.output("Level " + str(episode_id) + " is already unlocked.")
    else:
        unlock_byte |= 0x1
        pcsx2.write_int32(GameAddress.gameadd_level_unlocks + episode_offset, unlock_byte)
        pcsx2.write_int32(GameAddress.gameadd_level_unlocks + episode_offset + 4, 0x2) #unlock the first warpgate

def complete_episode(episode_id: int, context):
    #using the episode's ID, mark it as completed. At time of writing, we only mark episodes as unlocked, but not complete
    if episode_id > 7 or episode_id < 0:
        #invalid episode ID. No can do
        print("Invalid episode ID " + str(episode_id) + " provided.")
        context.output("Invalid episode ID " + str(episode_id) + " provided.")
        return
    episode_offset = episode_id * 0x4C
    unlock_byte = pcsx2.read_int32(GameAddress.gameadd_level_unlocks + episode_offset)
    print("Complete byte read as " + hex(unlock_byte) + " at address " + hex(GameAddress.gameadd_level_unlocks + episode_offset))
    context.output("Complete byte read as " + hex(unlock_byte) + " at address " + hex(GameAddress.gameadd_level_unlocks + episode_offset))
    if unlock_byte & 0x2:
        print("Level " + str(episode_id) + " is already completed.")
        context.output("Level " + str(episode_id) + " is already completed.")
    else:
        if episode_id != 3 and episode_id != 5:
            unlock_byte |= 0b1000010
        else:
            unlock_byte |= 0b1001010
        pcsx2.write_int32(GameAddress.gameadd_level_unlocks + episode_offset, unlock_byte)

def unlock_minicon(minicon_id: int):
    # try:
        # minicon_id = minicon_ids[minicon_name]
    # except:
        # print("Couldn't find minicon")
        # return -1
    if not minicon_id < 50:
        print("Minicon ID out of bounds")
        return -1

    bit = 0x1 << (minicon_id - 1)
    old_inventory = pcsx2.read_int64(GameAddress.gameadd_minicon_unlocks)
    new_inventory = old_inventory | bit
    pcsx2.write_int64(GameAddress.gameadd_minicon_unlocks, new_inventory)
    return 0


def unlock_datacon(datacon_id: int):
    # try:
        # minicon_id = minicon_ids[minicon_name]
    # except:
        # print("Couldn't find minicon")
        # return -1
    if not datacon_id < 64:
        print("Minicon ID out of bounds")
        return -1

    bit = 0x1 << (datacon_id - 1)
    old_inventory = pcsx2.read_int64(GameAddress.gameadd_datacon_unlocks)
    new_inventory = old_inventory | bit
    pcsx2.write_int64(GameAddress.gameadd_datacon_unlocks, new_inventory)
    return 0


def check_valid_spawn(target_address: int):
    # When loading a level, the game will check if a minicon/datacon is unlocked or not to see if it needs to be placed.
    # Using the modified code from write_initial_values, read the location ID of the currently checked location
    # and compare it to the locations in checked_locations. If it's present in our list, it doesn't need to be
    # spawned. The value from this decision is written to RAM, along with a "process complete" value
    # that tells the game it's safe to proceed.
    read_values = []
    read_values.append(pcsx2.read_int32(target_address + 0xBC))
    read_values.append(pcsx2.read_int32(target_address + 0xB0))
    read_values.append(pcsx2.read_int32(target_address + 0xB4))
    read_values.append(pcsx2.read_int32(target_address + 0xB8))
    location = get_location_id(read_values)
    print("Location ID read as: " + str(location) + ". Check against Archipelago unlock list.")

    # write the check value for the game to read
    #if the location's value is 0, that means it's been wiped before during a pickup activation
    #this will prevent double-collections caused by cached reloads
    if location in checked_locations or location == 0:
        pcsx2.write_int32(CleanAddress.cleanadd_pickup_spawn_replacement - 0x4, 1)
    else:
        pcsx2.write_int32(CleanAddress.cleanadd_pickup_spawn_replacement - 0x4, 0)
    # write the process complete so the game breaks out of the loop
    # keep an eye on this, we may need the game to reset this value before entering the loop
    pcsx2.write_int32(CleanAddress.cleanadd_pickup_spawn_replacement - 0x8, 1)


def execute_command(command, context):
    #This function handles all the commands listed in the PineCommand enum. Commands are taken as a tuple
    #of values. The first value is the PineCommand option, while any following values are parameters/arguments passed
    #to the command itself.
    #Some of these should be rewritten as their own functions which this then calls
    #See comments under each case for more information
    if command[0] == PineCommand.comm_get_health:
        #Returns the player's current health as a float value
        health_raw = pcsx2.read_int32(GameAddress.gameadd_player_health)
        return raw_bytes_to_float(health_raw)

    if command[0] == PineCommand.comm_get_game_id:
        #Returns the current game ID as a string
        return pcsx2.get_game_id()

    if command[0] == PineCommand.comm_status:
        #Checks the connection status. Currently this is redundant, since PINE errors if we lose connection
        return pcsx2.is_connected()

    if command[0] == PineCommand.comm_exit:
        #Disconnects the PINE client from PCSX2. We currently do not have a way to reconnect from this state without restarting the client.
        pcsx2.disconnect()
        pine_is_connected = False    #Tell client pine was disconnected
        return

    if command[0] == PineCommand.comm_unlock_sidekick:
        radio_value = pcsx2.read_int32(GameAddress.gameadd_level_unlocks-4)
        unlocked_sidekick = radio_value | 0x1
        pcsx2.write_int32(GameAddress.gameadd_level_unlocks-4, unlocked_sidekick)

    '''The following commands take arguements, we should probably have verification checks on them that the tuple is as long as we expect.
    '''
    if command[0] == PineCommand.comm_set_health:
        #Sets the player's health to the value of the first parameter
        if len(command) != 2:
            return
        value: float = float(command[1])

        pcsx2.write_float(GameAddress.gameadd_player_health, value)

        print(f'Set health to {command[1]}')

    if command[0] == PineCommand.comm_unlock_minicon:
        #Unlocks the minicon indicated by the name in the first parameter
        unlock_minicon(command[1])

    if command[0] == PineCommand.comm_unlock_episode:
        unlock_episode(command[1], context)

    if command[0] == PineCommand.comm_complete_episode:
        complete_episode(command[1], context)

    if command[0] == PineCommand.comm_read_location:
        return read_pickup_location(command[1], context)

    if command[0] == PineCommand.comm_check_spawn:
        check_valid_spawn(command[1])
    
    if command[0] == PineCommand.comm_set_max_health:
        #Sets player health to the maximum for the character
        max_health_raw = pcsx2.read_int32(GameAddress.gameadd_player_max_health)
        max_health: float = raw_bytes_to_float(max_health_raw)
        
        pcsx2.write_float(GameAddress.gameadd_player_health, max_health)
        
        print(f'Set health to {max_health} (Max)')


async def monitor_ram(context):
    global pine_is_connected
    global checked_locations
    global unhandled_locations
    init_values_written = False
    
    #This should be called from the main client to begin tracking unlocks and other information from PCSX2
    print("Starting PCSX2 RAM monitor.")
    pcsx2.connect() #if PCSX2 is not open, this will throw an error. TODO: handle this error in a way that's less disruptive
    
    #Created a loop to try to connect to the game
    while not (pcsx2.is_connected() and pcsx2.get_game_id() in game_codes):
        print("PCSX2 Failed to connect, trying again in 5 seconds")
        context.output("PCSX2 Failed to connect, trying again in 5 seconds")
        await asyncio.sleep(5)
        pcsx2.connect()
    
    #write_initial_values()
    
    #await asyncio.sleep(1)
    #pine_is_connected = True #tell client pine is connected
    
    #checked_locations.extend(TFContext.checked_locations) #fill list of checked locations from Archipelago
    while True:
        if context.in_HQ and not init_values_written:
            write_initial_values()
            init_values_written = True
            await asyncio.sleep(1)
            pine_is_connected = True #tell client pine is connected
        
        mode = 'Auto' #'Manual' #
        if mode == 'Manual':
            command = get_user_command()
        else:
            command = read_target_addresses(context)
        if command[0] != PineCommand.comm_nothing:
            execute_command(command,context)
        
        if not pcsx2.is_connected():
            print("PINE Disconnected, attempting reconnect")
            context.output("PINE Disconnected, attempting reconnect")
            pcsx2.connect()
            await asyncio.sleep(1)
        
        await asyncio.sleep(0.02)


def read_target_addresses(context) -> tuple[PineCommand, ...]:
    #Checks specific RAM addresses to see if PINE intervention is required
    global player_in_HQ
    hq_check = pcsx2.read_int32(GameAddress.gameadd_HQ_check)
    if(hq_check == 1):
        #while setting up levels and the main menu, this value increments by 1. So, we need to let it
        #run through a cycle
        if(player_in_HQ):
            #signal client that we're in HQ so it can update unlocks in-game
            #player_in_HQ = False
            context.in_HQ = True
        else:
            player_in_HQ = True
    else:
        player_in_HQ = False
        context.in_HQ = False

    pickup_check = pcsx2.read_int32(CleanAddress.cleanadd_pickup_code - 0x10)
    if pickup_check != 0:
        print("Item pickup detected")
        #context.output("Item pickup detected")
        interaction_instance = pcsx2.read_int32(CleanAddress.cleanadd_pickup_code-0x10)
        pickup_instance = pcsx2.read_int32(interaction_instance+0x4)
        pcsx2.write_int32(CleanAddress.cleanadd_pickup_code-0x10, 0)
        pickup_id = pcsx2.read_int32(pickup_instance+0x4)
        if pickup_id == 0x10: #0x10 is Endgame
            print("Archipelago Minicon pickup detected.")
            #context.output("Archipelago item pickup detected.")
            #TODO: decrease the minicon collection count for the current level
            #pcsx2.write_int32(GameAddress.gameadd_minicon_unlocks, minicon_unlocks ^ 0x1000) #we no longer overwrite the minicon unlocks, since minicons aren't unlocked until HQ
        elif pickup_id == 0x3: #is a datacon
            datacon_pickup = pcsx2.read_int64(pickup_instance + 0x240)
            if datacon_pickup == 0x4000: #not 100% sure that this is the right one. May be 0x8000 instead. Needs to be verified.:
                print("Archipelago Datacon pickup detected")
        return (PineCommand.comm_read_location, pickup_instance,)

    # minicon_unlocks = pcsx2.read_int32(GameAddress.gameadd_minicon_unlocks)
    # if minicon_unlocks & 0x1000: #0x1000 is Endgame
    #     print("Archipelago item pickup detected.")
    #     pcsx2.write_int32(GameAddress.gameadd_minicon_unlocks, minicon_unlocks ^ 0x1000)
    #     pickup_instance = pcsx2.read_int32(CleanAddress.cleanadd_pickup_code-0x10)
    #     #we also need to decrease the minicon collection count for the current level
    #     return (PineCommand.comm_read_location, pickup_instance,)

    level_unlocks = pcsx2.read_int32(CleanAddress.cleanadd_level_unlocked)
    if level_unlocks != 0:
        current_episode_index = pcsx2.read_int32(CleanAddress.cleanadd_level_unlocked+4)
        print("Episode " + str(current_episode_index) + " completed. Sending to Archipelago.")
        context.output("Episode " + str(current_episode_index + 1) + " completed. Sending to Archipelago.")
        send_location(9001+current_episode_index)
        #for now, just unlocking the next episode and reset the bit
        #unlock_episode(level_unlocks + 1)
        pcsx2.write_int32(CleanAddress.cleanadd_level_unlocked, 0)

    checking_spawn = pcsx2.read_int32(CleanAddress.cleanadd_pickup_spawn_replacement-0xC)
    if checking_spawn != 0:
        #checking_spawn is the memory address, get the location from offset 0xB from that address
        pcsx2.write_int32(CleanAddress.cleanadd_pickup_spawn_replacement-0xC, 0)
        return (PineCommand.comm_check_spawn, checking_spawn,)

    check_cheats = pcsx2.read_int32(GameAddress.gameadd_cheats)
    if check_cheats != 0xFFFFFFFF:
        #the game has put us on a valid cheat screen, we need to invalidate that
        pcsx2.write_int32(GameAddress.gameadd_cheats, 0xFFFFFFFF)
    return (PineCommand.comm_nothing,)


def get_user_command() -> tuple[PineCommand, ...]:
    #Can be used for manual command testing. Has not been kept up to date.
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


#asyncio.run(monitor_ram()) #used for testing