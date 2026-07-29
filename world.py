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
            "trap_chance", "minicon_count", "start_with_random_weapon", "goal_option", "randomize_levels"
        )
    
    def generate_output(self, output_directory: str) -> None:
        file_name = self.multiworld.get_out_file_name_base(self.player)
        
        random_num = self.random.randint(0,65535)
        data = {
            location.name: location.item.name
            if location.item.player == self.player else "Remote"
            for location in self.multiworld.get_filled_locations(self.player)
        }
        
        
        contents = ""
        contents += str(random_num) + " \n"
        
        if self.options.start_with_random_weapon == False:
            contents += str(1) + " " + str(42069) + " " + str(4) + " \n"
        
        for location, item in data.items():
            if location in database.LOCATION_NAME_TO_ID:
                loc_id = database.LOCATION_NAME_TO_ID.get(location)
            else:
                continue
            if (loc_id >= 200):
                continue
            if item in database.ITEM_NAME_TO_ID:
                item_id = database.ITEM_NAME_TO_ID.get(item)
            else:
                item_id = database.Archipelago_Item_ID
            minicon_bool = 1
            
            if (item_id >= 50 and item_id < 150):
                item_id -= 50
                minicon_bool = 0
            if item_id >= 150:
                item_id = database.Archipelago_Item_ID
            
            if (item_id < 50 and minicon_bool==1):
                item_id += 3
            
            contents += str(minicon_bool) + " " + str(loc_id) + " " + str(item_id) + " \n"
            
            patch = Transformers04Patch(
                self.player,
                self.multiworld.player_name[self.player]
            )
            
            patch.contents = contents
            
            patch.write(os.path.join(output_directory, file_name + ".txt"))
        