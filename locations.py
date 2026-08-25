from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items
from . import database

if TYPE_CHECKING:
    from .world import Transformers04World
    



class Transformers04Location(Location):
    game = "Transformers (2004)"
    
    # Let's make one more helper method before we begin actually creating locations.
    # Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
    # To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
    # let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
    # Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
    # so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: database.LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def create_all_locations(world: Transformers04World) -> None:
    create_regular_locations(world)
    create_events(world)
    
def create_regular_locations(world: Transformers04World) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    amazon = world.get_region("Amazon")
    antartica = world.get_region("Antarctica")
    deep_amazon = world.get_region("Deep Amazon")
    mid_atlantic = world.get_region("Mid Atlantic")
    alaska = world.get_region("Alaska")
    starship = world.get_region("Starship")
    pacific_island = world.get_region("Pacific Island")
    menu = world.get_region("Menu")
    
    amazon_locations = get_location_names_with_ids(
        [k for k in database.LOCATION_NAME_TO_ID if k.startswith("Amazon-")]
    )
    amazon.add_locations(amazon_locations, Transformers04Location)
    if(world.options.add_starting_location):
        menu.add_locations(get_location_names_with_ids(["Beginner Location"]), Transformers04Location)
    #if(world.options.randomize_levels):
    amazon.add_locations(get_location_names_with_ids(["Amazon Boss"]), Transformers04Location)
    
    
    antartica_locations = get_location_names_with_ids(
        [k for k in database.LOCATION_NAME_TO_ID if k.startswith("Antarctica-")]
    )
    antartica.add_locations(antartica_locations, Transformers04Location)
    #if(world.options.randomize_levels):
    antartica.add_locations(get_location_names_with_ids(["Antarctica Boss"]), Transformers04Location)
    
    
    deep_amazon_locations = get_location_names_with_ids(
        [k for k in database.LOCATION_NAME_TO_ID if k.startswith("Deep Amazon-")]
    )
    deep_amazon.add_locations(deep_amazon_locations, Transformers04Location)
    #if(world.options.randomize_levels):
    deep_amazon.add_locations(get_location_names_with_ids(["Deep Amazon Boss"]), Transformers04Location)
    
    
    mid_atlantic_locations = get_location_names_with_ids(
        [k for k in database.LOCATION_NAME_TO_ID if k.startswith("Mid Atlantic-")]
    )
    mid_atlantic.add_locations(mid_atlantic_locations, Transformers04Location)
    #if(world.options.randomize_levels):
    mid_atlantic.add_locations(get_location_names_with_ids(["Mid Atlantic Boss"]), Transformers04Location)
    
    
    alaska_locations = get_location_names_with_ids(
        [k for k in database.LOCATION_NAME_TO_ID if k.startswith("Alaska-")]
    )
    alaska.add_locations(alaska_locations, Transformers04Location)
    #if(world.options.randomize_levels):
    alaska.add_locations(get_location_names_with_ids(["Alaska Complete"]), Transformers04Location)
    
    
    starship_locations = get_location_names_with_ids(
        [k for k in database.LOCATION_NAME_TO_ID if k.startswith("Starship-")]
    )
    starship.add_locations(starship_locations, Transformers04Location)
    #if(world.options.randomize_levels):
    starship.add_locations(get_location_names_with_ids(["Starship Boss"]), Transformers04Location)
    
    
    pacific_island_locations = get_location_names_with_ids(
        [k for k in database.LOCATION_NAME_TO_ID if k.startswith("Pacific Island-")]
    )
    pacific_island.add_locations(pacific_island_locations, Transformers04Location)
    #if(world.options.randomize_levels):
    pacific_island.add_locations(get_location_names_with_ids(["Pacific Island Boss"]), Transformers04Location)
    
    
    
# events are for locations that are tied to an item, so we can check them for logic, but 
# not put a random item in it. This will be used to handle bosses unlocking levels when
# random level order is not selected. 
def create_events(world: Transformers04World) -> None:
    menu = world.get_region("Menu")
    amazon = world.get_region("Amazon")
    antartica = world.get_region("Antarctica")
    deep_amazon = world.get_region("Deep Amazon")
    mid_atlantic = world.get_region("Mid Atlantic")
    alaska = world.get_region("Alaska")
    starship = world.get_region("Starship")
    pacific_island = world.get_region("Pacific Island")
    unicron = world.get_region("Unicron")
    
    
    # amazon_boss = Transformers04Location(world.player, "Amazon Boss", None, amazon)
    # antartica_boss = Transformers04Location(world.player, "Antarctica Boss", None, antartica)
    # deep_amazon_boss = Transformers04Location(world.player, "Deep Amazon Boss", None, deep_amazon)
    # mid_atlantic_boss = Transformers04Location(world.player, "Mid Atlantic Boss", None, mid_atlantic)
    # alaska_complete = Transformers04Location(world.player, "Alaska Complete", None, alaska)
    # starship_boss = Transformers04Location(world.player, "Starship Boss", None, starship)
    # pacific_island_boss = Transformers04Location(world.player, "Pacific Island Boss", None, pacific_island)
    # all_bosses_location = Transformers04Location(world.player, "Defeat All Bosses", None, menu)
    
    
    # antartica_unlock = items.Transformers04Item("Antarctica Level Unlock", ItemClassification.progression, None, world.player)
    # deep_amazon_unlock = items.Transformers04Item("Deep Amazon Level Unlock", ItemClassification.progression, None, world.player)
    # mid_atlantic_unlock = items.Transformers04Item("Mid Atlantic Level Unlock", ItemClassification.progression, None, world.player)
    # alaska_unlock = items.Transformers04Item("Alaska Level Unlock", ItemClassification.progression, None, world.player)
    # starship_unlock = items.Transformers04Item("Starship Level Unlock", ItemClassification.progression, None, world.player)
    # pacific_island_unlock = items.Transformers04Item("Pacific Island Level Unlock", ItemClassification.progression, None, world.player)
    # unicron_unlock = items.Transformers04Item("Unicron Level Unlock", ItemClassification.progression, None, world.player)
    # all_bosses_beaten = items.Transformers04Item("All Bosses Beaten", ItemClassification.progression, None, world.player)
    
    
    # if not (world.options.randomize_levels):
        # amazon.locations.append(amazon_boss)
        # amazon_boss.place_locked_item(antartica_unlock)
        
        # antartica.locations.append(antartica_boss)
        # antartica_boss.place_locked_item(deep_amazon_unlock)
        
        # deep_amazon.locations.append(deep_amazon_boss)
        # deep_amazon_boss.place_locked_item(mid_atlantic_unlock)
        
        # mid_atlantic.locations.append(mid_atlantic_boss)
        # mid_atlantic_boss.place_locked_item(alaska_unlock)
        
        # alaska.locations.append(alaska_complete)
        # alaska_complete.place_locked_item(starship_unlock)
        
        # starship.locations.append(starship_boss)
        # starship_boss.place_locked_item(pacific_island_unlock)
        
        # pacific_island.locations.append(pacific_island_boss)
        # pacific_island_boss.place_locked_item(unicron_unlock)
        
    unicron.add_event(
        "Unicron Defeated", "Victory", location_type=Transformers04Location, item_type=items.Transformers04Item
    )
    
    menu.locations.append(all_bosses_location)
    all_bosses_location.place_locked_item(all_bosses_beaten)