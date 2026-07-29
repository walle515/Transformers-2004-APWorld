from worlds.Files import APContainer

class Transformers04Patch(APContainer):
    
    game = "Transformers (2004)"
    
    patch_file_ending = ".txt"
    procedure = "transformers04"
    
    contents = ""
    
    def __init__(self, player, player_name):
        super().__init__()
        self.player = player
        self.player_name = player_name
    
    def write(self, file):
        with open(file, "w") as f:
            f.write(self.contents)