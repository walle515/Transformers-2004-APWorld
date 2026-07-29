from worlds.Files import APContainer

class Transformers04Patch(APContainer):
    
    game = "Transformers (2004)"
    
    patch_file_ending = ".aptf"
    
    contents = ""
    
    def __init__(self, player: int, player_name: str):
        super().__init__(player, player_name)
    
    def write_contents(self, opened_zipfile):
        opened_zipfile.writestr(
            f"{self.player_name}{self.patch_file_ending}",
            self.contents
        )