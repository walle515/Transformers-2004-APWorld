from worlds.Files import APPatch
import zipfile


class Transformers04Patch(APPatch):
    game = "Transformers (2004)"
    patch_file_ending = ".aptf"
    contents = ""
    filename = ""
    
    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super().write_contents(opened_zipfile)
        
        opened_zipfile.writestr(
            self.filename,
            self.contents
        )