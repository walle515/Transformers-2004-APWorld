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
    midAtlanticTidal = Region("Mid Atlantic", world.player, world.multiworld)
    midAtlanticEmpty = Region("Mid Atlantic Empty", world.player, world.multiworld)
    alaska = Region("Alaska", world.player, world.multiworld)
    starship = Region("Starship", world.player, world.multiworld)
    pacificIsland = Region("Pacific Island", world.player, world.multiworld)
    
    regions = [amazon, antartica, deepAmazon, midAtlanticTidal, midAtlanticEmpty, alaska, starship, pacificIsland]
    
    world.multiworld.regions += regions
    
    
