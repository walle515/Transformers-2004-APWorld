import filedialpy
from .pine import pcsx2
import os

class ModLine:
    type: int
    data: int

    def __init__(self):
        self.type = 0
        self.data = 0

    def parse_line(self, line: str):
        line_data = line.split(":")
        self.type = int(line_data[0])
        self.data = int(line_data[1].strip(), 16)

class ModSection:
    starting_address: int
    line_count: int
    lines: list[ModLine]
    def __init__(self):
        self.starting_address = 0
        self.line_count = 0
        self.lines = []

class MipsMod:
    version: int
    name: str
    description: str
    type: int
    section_count: int
    sections: list[ModSection]
    def __init__(self):
        self.version = 0
        self.name = 'Default'
        self.description = 'No description'
        self.type = 0
        self.section_count = 0
        self.sections = []

    def parse_mod_data(self, file_data):
        line_num = 0
        for section_num in range(self.section_count):
            section = ModSection()
            line_data = file_data[line_num].split(":")
            section.starting_address = int(line_data[1].strip(), 16)
            line_num += 1
            line_data = file_data[line_num].split(":")
            section.line_count = int(line_data[1].strip())
            line_num +=1
            for mod in range(section.line_count):
                mod_data = ModLine()
                mod_data.parse_line(file_data[line_num])
                section.lines.append(mod_data)
                line_num +=1
            self.sections.append(section)
    def parse_file(self, file_path):
        file = open(file_path, 'r')
        file_data = file.readlines()
        file.close()
        for line_num in range(len(file_data)):
            contents = file_data[line_num].split(':')
            if contents[0] == 'Version':
                self.version = int(contents[1].strip())
            if contents[0] == 'Mod Name':
                self.name = contents[1]
            if contents[0] == 'Description':
                self.description = contents[1]
            if contents[0] == 'Mod type':
                self.type = int(contents[1].strip())
            if contents[0] == 'Mod sections':
                self.section_count = int(contents[1].strip())
                remaining_lines = len(file_data) - line_num - 1
                file_data = file_data[-remaining_lines:]
                break
        self.parse_mod_data(file_data)


def insert_mod_lines(start_address: int, end_address:int, stored_lines: list[int]) -> list[int]:
    current_address = start_address
    while current_address < end_address:
        target_instruction = pcsx2.read_int32(current_address)
        stored_lines.append(target_instruction)
        pcsx2.write_int32(current_address, stored_lines[0])
        stored_lines = stored_lines[1:]
        current_address += 4
    return stored_lines

def remove_mod_lines(start_address: int, end_address:int, amount: int):
    current_address = start_address
    while current_address < end_address:
        target_instruction = pcsx2.read_int32(current_address + (amount*4))
        pcsx2.write_int32(current_address, target_instruction)

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
    file.parse_file(file_path)
    #there should never be both inserts and deletes waiting, they cancel each other out
    hanging_inserts = 0
    hanging_deletes = 0
    stored_lines = []
    #using the i's and j's separate from the loop also seems wrong
    i = 0
    for section in file.sections:
        print("section " + str(i) + " address: " + str(section.starting_address))
        j = 0
        for line in section.lines:
            print("line " + str(j) + " is type " + str(line.type) + " with data " + str(line.data))
            '''Iterates through a section, handling the different types of mod lines. Since all lines in a section
            are consecutive, we don't have to worry about missing one with this algorithm
            Essentially, Inserts and Deletes build up a balance of unhandled lines. These will need to be pulled
            forward or pushed back, depending on the balance. When lines of the other type are encountered, they 
            cancel out and the outstanding balance is reduced. Any active balance's effects are handled at the start
            of each loop.'''
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
        '''If we have any extra deletes or inserts after a section, those need to be bridged over into the next one
        otherwise, we'll have code that's not supposed to be there or miss code that is supposed to be there
        '''
        if hanging_deletes > 0:
            next_section = file.sections[i] #this feels gross, but we need to know the next section to correct the imbalance
            remove_mod_lines(section.starting_address + (4*j), next_section.starting_address, hanging_deletes)
        if hanging_inserts > 0:
            next_section = file.sections[i] #this feels gross, but we need to know the next section to correct the imbalance
            insert_mod_lines(section.starting_address + (4*j), next_section.starting_address, stored_lines)

        i+=1
