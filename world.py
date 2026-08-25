# Using APQuest as a tutorial, as it is written as a tutorial
from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import items, locations, regions, rules
from . import web_world
from . import options as tf04_options
from . import database
import os
from .patch import Transformers04Patch
from BaseClasses import ItemClassification

class Transformers04World(World):
    game = "Transformers (2004)"
    
    web = web_world.Transformers04WebWorld()
    
    options_dataclass = tf04_options.Transformers04Options
    options: tf04_options.Transformers04Options
    
    location_name_to_id = database.LOCATION_NAME_TO_ID
    item_name_to_id = database.ITEM_NAME_TO_ID
    
    #This is the start region that should always be accessible
    origin_region_name = "Menu"
    
    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)
        
    def set_rules(self) -> None:
        rules.set_all_rules(self)
    
    def create_items(self) -> None:
        items.create_all_items(self)
    
    def create_item(self, name: str) -> items.Transformers04Item:
        return items.create_item_with_correct_classification(self, name)
    
    # For features such as item links and panic-method start inventory, AP may ask your world to create extra filler.
    # The way it does this is by calling get_filler_item_name.
    # For this purpose, your world *must* have at least one infinitely repeatable item (usually filler).
    # You must override this function and return this infinitely repeatable item's name.
    # In our case, we defined a function called get_random_filler_item_name for this purpose in our items.py.
    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)
    
    # There may be data that the game client will need to modify the behavior of the game.
    # This is what slot_data exists for. Upon every client connection, the slot's slot_data is sent to the client.
    # slot_data is just a dictionary using basic types, that will be converted to json when sent to the client.
    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        return self.options.as_dict(
            "trap_chance", 
            "minicon_count", 
            "add_starting_location", 
            "goal_option", 
            "randomize_levels", 
            "randomize_stats",
            "randomize_mini_power",
            "randomize_mini_color"
        )
    
    def generate_output(self, output_directory: str) -> None:
        file_name = self.multiworld.get_out_file_name_base(self.player)
        visible_progression = self.options.visible_progression_items
        
        random_num = self.random.randint(0,65535)
        data = {
            location.name: location.item
            if location.item.player == self.player else "Remote"
            for location in self.multiworld.get_filled_locations(self.player)
        }
        
        
        contents = ""
        
        contents += str(int(self.options.randomize_stats)) + " "
        contents += str(int(self.options.randomize_mini_power)) + " "
        contents += str(int(self.options.randomize_mini_color)) + " \r\n"
        
        contents += str(random_num) + " \r\n"
        
        
        for location, item in data.items():
            if location in database.LOCATION_NAME_TO_ID:
                loc_id = database.LOCATION_NAME_TO_ID.get(location)
            else:
                continue
            if (loc_id >= 7000 and loc_id <10000):
                continue
                
            if visible_progression:
                if item.name in database.ITEM_NAME_TO_ID:
                    item_id = database.ITEM_NAME_TO_ID.get(item.name)
                    if item_id >= 150:
                        item_id = database.Archipelago_Minicon_ID
                    if (item_id >= 50 and item_id < 150):
                        item_id -= 50
                    if ((item.classification & ItemClassification.progression) or (item.classification & ItemClassification.trap)):
                        minicon_bool = 1
                    else:
                        minicon_bool = 0
                else:
                    if ((item.classification & ItemClassification.progression) or (item.classification & ItemClassification.trap)):
                        item_id = database.Archipelago_Minicon_ID
                        minicon_bool = 1
                    else:
                        item_id = database.Archipelago_Datacon_ID
                        minicon_bool = 0
            else:
                if item.name in database.ITEM_NAME_TO_ID:
                    item_id = database.ITEM_NAME_TO_ID.get(item.name)
                else:
                    item_id = database.Archipelago_Datacon_ID
                minicon_bool = 1
                
                if (item_id >= 50 and item_id < 150):
                    item_id -= 50
                    minicon_bool = 0
                if item_id >= 150:
                    item_id = database.Archipelago_Minicon_ID
                
            if (item_id < 50 and minicon_bool==1):
                item_id += 3
            
            contents += str(minicon_bool) + " " + str(loc_id) + " " + str(item_id) + " \r\n"
            
        # with open(os.path.join(output_directory, file_name + ".txt"), "w") as f:
            # f.write(contents)
        
        patch_path = os.path.join(output_directory, file_name + ".aptf")
        patch = Transformers04Patch(
            player = self.player,
            player_name = self.player_name
        )
        patch.filename = "Exodus.txt"
        patch.contents = contents
        patch.write(patch_path)
        #self.output_file = patch_path