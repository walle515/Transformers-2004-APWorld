from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import Transformers04World

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).


def create_and_connect_regions(world: Transformers04World) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: Transformers04World) -> None:
    # Creating a region is as simple as calling the constructor of the Region class.
    amazon = Region("Amazon", world.player, world.multiworld)
    antartica = Region("Antartica", world.player, world.multiworld)
    deepAmazon = Region("Deep Amazon", world.player, world.multiworld)
    midAtlantic = Region("Mid Atlantic", world.player, world.multiworld)
    alaska = Region("Alaska", world.player, world.multiworld)
    starship = Region("Starship", world.player, world.multiworld)
    pacificIsland = Region("Pacific Island", world.player, world.multiworld)
    unicron = Region("Unicron", world.player, world.multiworld)
    menu = Region("Menu", world.player, world.multiworld)
    
    regions = [menu, amazon, antartica, deepAmazon, midAtlantic, alaska, starship, pacificIsland, unicron]
    
    world.multiworld.regions += regions
    
    
def connect_regions(world: Transformers04World) -> None:
    amazon = world.get_region("Amazon")
    antartica = world.get_region("Antartica")
    deep_amazon = world.get_region("Deep Amazon")
    mid_atlantic = world.get_region("Mid Atlantic")
    alaska = world.get_region("Alaska")
    starship = world.get_region("Starship")
    pacific_island = world.get_region("Pacific Island")
    unicron = world.get_region("Unicron")
    menu = world.get_region("Menu")
    
    
    menu.connect(amazon, "Amazon Unlocked", lambda state: state.has("Amazon Level Unlock", world.player))
    menu.connect(antartica, "Antartica Unlocked", lambda state: state.has("Antartica Level Unlock", world.player))
    menu.connect(deep_amazon, "Deep Amazon Unlocked", lambda state: state.has("Deep Amazon Level Unlock", world.player))
    menu.connect(mid_atlantic, "Mid Atlantic Unlocked") #need to add rule for rangefinder and level unlock
    menu.connect(alaska, "Alaska Unlocked", lambda state: state.has("Alaska Level Unlock", world.player))
    menu.connect(starship, "Starship Unlocked", lambda state: state.has("Starship Level Unlock", world.player))
    menu.connect(pacific_island, "Pacific Island Unlocked", lambda state: state.has("Pacific Island Level Unlock", world.player))
    menu.connect(unicron, "Unicron Unlocked") #Unlocked by level unlock and number of minicons