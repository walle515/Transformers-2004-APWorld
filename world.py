# Using APQuest as a tutorial, as it is written as a tutorial
from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import items, locations, regions, rules
#from . import web_world
from . import options as tf04_options

class Transformers04World(World):
    game = "Transformers (2004)"
    
    #web = web_world.Transformers04WebWorld()
    
    options_dataclass = tf04_options.Transformers04Options
    options: tf04_options.Transformers04Options
    
    location_name_to_id = database.LOCATION_NAME_TO_ID
    item_name_to_id = database.ITEM_NAME_TO_ID
    
    #This is the start region that should always be accessible. Amazon1 (named just Amazon here) is likely the start
    origin_region_name = "Amazon"
    
    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)
        
    def set_rules(self) -> None:
        rules.set_all_items(self)
    
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
            "hard_mode", "hammer", "extra_starting_chest", "confetti_explosiveness", "player_sprite"
        )
    
    def generate_output(self, output_directory: str) -> None:
        file_name = self.multiworld.get_out_file_name_base(self.player)
        out_file = os.path.join(output_directory, file_name + ".txt")
        
        random_num = world.random.randint(0,65535)
        data = {
            location.name: location.item.name
            if location.item.player == self.player else "Remote"
            for location in self.multiworld.get_filled_locations(self.player)
        }
        
        
        with open(out_file, "w") as f:
            f.write(str(random_num) + " \n")
            
            for location, item in data.items():
                loc_id = database.LOCATION_NAME_TO_ID.get(location)
                loc_id -= 1
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
                
                f.write(str(minicon_bool) + " " + str(loc_id) + " " + str(item_id) + " \n")
                
                for loc,link in database.Linked_Locations.items():
                    if loc == location:
                        loc_id = link - 1
                        f.write(str(minicon_bool) + " " + str(loc_id) + " " + str(item_id) + " \n")
        