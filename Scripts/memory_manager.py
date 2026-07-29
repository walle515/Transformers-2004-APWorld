import struct
from Scripts.pine import Pine, pcsx2
from Data.tf_data import add_minicon
from enum import Enum
from Scripts.mips_mods import MipsMod
import filedialpy
import os
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

def raw_bytes_to_float(read_output: int) -> float:
    return struct.unpack("<f", struct.pack("<I", read_output))[0]

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
    if minicon_unlocks & 0x20000: #0x1000: #0x1000 is Endgame, 0x20000 should be Lock-on
        #since this doesn't reset the minicon unlock value, you'll get in an infinite loop here. But for testing, it works.
        return (PineCommand.comm_set_health, 1,)
    return (PineCommand.comm_nothing,)

def write_mod_lines(target_address: int, lines_to_write: list[int]):
    for line in range(len(lines_to_write)):
        pcsx2.write_int32(target_address + 4*line, lines_to_write[line])
def apply_mod(file_name):
    #check if mod file exists in Data folder
    #iterate through mod sections, write data to RAM
    if file_name == "":
        file_path = filedialpy.openFile()
    else:
        #there's gotta be a better way to do this, right? Not super familiar with Python
        script_dir = os.path.realpath(__file__)
        #there has to be. This line will need to change based on which file we have as the launch file
        data_dir = "{}/../Data/".format(script_dir)
        file_path = os.path.join(data_dir, file_name)
    if not os.path.exists(file_path):
        print("Invalid mod file provided. Target path: " + file_path)
        return
    file = MipsMod()
    file.prase_file(file_path)
    #using the i's and j's separate from the loop also seems wrong
    i = 0
    for section in file.sections:
        print("section " + str(i) + " address: " + str(section.starting_address))
        j = 0
        #there should never be both inserts and deletes waiting, they cancel each other out
        hanging_inserts = 0
        hanging_deletes = 0
        stored_lines = []
        stored_addresses = []
        for line in section.lines:
            print("line " + str(j) + " is type " + str(line.type) + " with data " + str(line.data))
            #here we run into an issue. The different line types work differently, and some of them are gonna be annoying here
            #replacements are fine, no problem. But inserts and deletes are an issue.
            if hanging_deletes > 0:
                #currently shifting lines back - take the next line, copy it to the current address
                next_line = pcsx2.read_int32(section.starting_address + (4*j+hanging_deletes))
                pcsx2.write_int32(section.starting_address + (4 * j), next_line)
            if hanging_inserts > 0:
                stored_lines.append(pcsx2.read_int32(section.starting_address + (4 * j)))
                pcsx2.write_int32(section.starting_address + (4 * j), stored_lines[0])
                stored_lines = stored_lines[1:]
            match line.type:
                case 0: #insert
                    if hanging_deletes > 0:
                        pcsx2.write_int32(section.starting_address + (4*j), line.data)
                        hanging_deletes -= 1
                    else:
                        #store the current line, then replace it
                        hanging_inserts += 1
                        stored_lines.append(pcsx2.read_int32(section.starting_address + (4*j)))
                        pcsx2.write_int32(section.starting_address + (4 * j), line.data)
                    print("The logic for inserted instructions isn't handled yet")
                case 1: #delete
                    #first, verify that the line we're looking to delete matches the data in the mod file
                    target_instruction = pcsx2.read_int32(section.starting_address + (4*j))
                    if target_instruction != line.data:
                        #if they don't match, we've gotten desynced somewhere. Stop applying the mod, we've probably already broken the game
                        print("Mod desync in section " + str(i) + ", line " + str(j))
                        break
                    if hanging_inserts > 0:
                        #reduce the remaining inserts, then restore the current line from storage
                        hanging_inserts -= 1
                        pcsx2.write_int32(section.starting_address + (4 * j), stored_lines[0])
                        stored_lines = stored_lines[1:]
                    else:
                        hanging_deletes += 1
                        next_line = pcsx2.read_int32(section.starting_address + (4 * j + hanging_deletes))
                        pcsx2.write_int32(section.starting_address + (4 * j), next_line)
                    #then we'll have to pull lines forward until the next insert. That sucks.
                case 2: #replace
                    #ezpz
                    pcsx2.write_int32(section.starting_address + (4*j), line.data)
            j+=1
        if hanging_deletes > 0 or hanging_inserts > 0:
            #TODO: add logic to handle shifting lines between sections (see Glide Always mod for example, sections 3 & 4)
            print("Mod file has unhandled deletions and insertions. This will currently lead to unexpected game behavior.")
        i+=1

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