from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

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
        antartica = world.get_region("Antartica")
        deep_amazon = world.get_region("Deep Amazon")
        mid_atlantic = world.get_region("Mid Atlantic")
        alaska = world.get_region("Alaska")
        starhsip = world.get_region("Starship")
        pacific_island = world.get_region("Pacific Island")
        
        amazon_locations = get_location_names_with_ids(
            [k for k in database.LOCATION_NAME_TO_ID if k.startswith("Amazon")]
        )
        amazon.add_locations(amazon_locations, Transformers04Location)
        
        #event items and locations (level unlocks and killing bosses) are handled differently than regular items and locations