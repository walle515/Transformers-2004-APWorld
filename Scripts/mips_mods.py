import filedialpy

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
    def prase_file(self, file_path):
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

# file = MipsMod()
# file.prase_file(filedialpy.openFile())
# i = 0
# for section in file.sections:
#     print("section " + str(i) + " address: " + str(section.starting_address))
#     j = 0
#     for line in section.lines:
#         print("line " + str(j) + " is type " + str(line.type) + " with data " + str(line.data))
