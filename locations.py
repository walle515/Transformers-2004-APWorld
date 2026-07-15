from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import Transformers04World
    
# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.

#location ids are ID+1
LOCATION_NAME_TO_ID = {
        "Amazon-Claymore Cave": 1,
    "Amazon-Spire": 3,
    "Amazon-Neighboring Mountain": 5,
    "Amazon-Ravine Cliff Cave": 6,
    "Amazon-Pressurepoint's Corner": 7,
    "Amazon-Foot of the Mountain": 8,
    "Amazon-Mountain Ruins": 9,
    "Amazon-Before the Waterfall Bridge": 10,
    "Amazon-Spidertank Triplets": 12,
    "Amazon-Ruined Temple Alcove": 13,
    "Amazon-Forest before the Bridge": 14,
    "Amazon-Ruined Temple Ledge": 16,
    "Amazon-Forest before Firefight": 17,
    "Amazon-Tutorial Minicon": 18,
    "Amazon-Ruined Temple Courtyard": 19,
    "Amazon-Light Unit Party": 20,
    "Amazon-Hidden Cave": 21,
    "Amazon-Riverside Ledge": 22,
    "Amazon-Waterfall Base": 23,
    "Amazon-Forest after the Bridge": 24,
    "Amazon-Surprise": 25,
    "Amazon-Forgettable Location": 26,
    "Amazon-Medium Unit Party": 27,
    "Amazon-Forest Across from the Basin 1": 28,
    "Amazon-Forest Across from the Basin 2": 29,
    "Antartica-Rock of Power": 31,
    "Antartica-Research Base Office 1": 35,
    "Antartica-Midfield Beacon": 38,
    "Antartica-Hide-and-Seek Champion": 39,
    "Antartica-Research Base Containers 1": 40,
    "Antartica-Research Base Containers 2": 41,
    "Antartica-Research Base Office 3": 42,
    "Antartica-Crashed Icebreaker": 45,
    "Antartica-Research Center Hangar": 46,
    "Antartica-Beachfront Property": 47,
    "Antartica-Crashed Plane": 48,
    "Antartica-Research Base Office 4": 49,
    "Antartica-Crevasse Field Overlook": 50,
    "Antartica-Lonely Island": 51,
    "Antartica-Research Base Office 2": 52,
    "Antartica-Across the Field": 53,
    "Deep Amazon-Island Altar": 54,
    "Deep Amazon-Top of the Temple": 56,
    "Deep Amazon-Spawn Ledge": 58,
    "Deep Amazon-Waterfall Rock": 59,
    "Deep Amazon-Jungle Ruins": 60,
    "Deep Amazon-Patrolling Dropship": 61,
    "Deep Amazon-Jungle Village Outskirts": 62,
    "Deep Amazon-Field before the Bridge": 63,
    "Deep Amazon-Temple Climb": 65,
    "Deep Amazon-Mid-Jungle Ditch": 66,
    "Deep Amazon-Village at the Foot of the Hill": 67,
    "Deep Amazon-Jungle Village Warpgate": 68,
    "Deep Amazon-Temple Dead End": 69,
    "Deep Amazon-Temple Pool": 70,
    "Deep Amazon-Temple Side-Path": 71,
    "Deep Amazon-Forest before the Bridge": 72,
    "Deep Amazon-Antechamber": 73,
    "Deep Amazon-Antechamber Alcove": 74,
    "Deep Amazon-Behind the Temple": 75,
    "Mid Atlantic Tidal-Vanilla Progression": 76,
    "Mid Atlantic Tidal-Distant Island": 77,
    "Mid Atlantic Tidal-Pinnacle Rock": 78,
    "Mid Atlantic Tidal-Atoll": 79,
    "Mid Atlantic Empty-Vanilla Progression": 80,
    "Mid Atlantic Empty-Distant Island": 81,
    "Mid Atlantic Empty-Atoll": 82,
    "Mid Atlantic Empty-Pinnacle Rock": 83,
    "Alaska-Mountaintop": 84,
    "Alaska-Small Forest": 85,
    "Alaska-Cave's Far Ledge": 87,
    "Alaska-Cave's Right Fork": 88,
    "Alaska-Cave's Left Fork": 89,
    "Alaska-Cave's Pool": 90,
    "Alaska-Along the Canyon": 91,
    "Alaska-Ocean Overlook": 92,
    "Alaska-Hidden Hill": 94,
    "Alaska-Canyon Clearing Ledge 1": 95,
    "Alaska-Battlefield": 96,
    "Alaska-Canyon Clearing Ledge 2": 97,
    "Alaska-Dropship Island": 98,
    "Alaska-Peninsula": 99,
    "Alaska-Escape": 100,
    "Alaska-Hillside": 101,
    "Starship-Start of the Climb": 102,
    "Starship-First Steps": 103,
    "Starship-Main Elevator": 104,
    "Starship-Sideways Elevator": 105,
    "Starship-Lower Dropship": 106,
    "Starship-Bait": 107,
    "Starship-Free Space": 108,
    "Starship-Across the Gap": 109,
    "Starship-Early Gift": 110,
    "Starship-Pristine Bridge": 111,
    "Starship-Crashed Bridge": 112,
    "Starship-Top of the Crashed Ship": 113,
    "Starship-Dropdown 1": 114,
    "Starship-Risky Jump": 115,
    "Starship-Rock 1": 116,
    "Starship-Middle Dropship": 117,
    "Starship-Dropdown 2": 118,
    "Starship-Rock 2": 119,
    "Starship-Rock 3": 120,
    "Starship-Rock 4": 121,
    "Pacific Island-Small Silo": 123,
    "Pacific Island-Moai": 124,
    "Pacific Island-Back of the Volcano": 125,
    "Pacific Island-Volcano Path": 126,
    "Pacific Island-Lighthouse": 128,
    "Pacific Island-Waterfall Climb": 129,
    "Pacific Island-Stronghold Ledge": 130,
    "Pacific Island-High Volcano Ledge": 132,
    "Pacific Island-Forest Basin": 133,
    "Pacific Island-Hidden Ledge": 134,
    "Pacific Island-Above the Waterfall": 135,
    "Pacific Island-Large Silo": 136,
    "Pacific Island-Small Island": 137,
    "Pacific Island-Bunker 1": 138,
    "Pacific Island-Bunker 4": 141,
    "Pacific Island-Bunker 5": 142,
    "Pacific Island-Bunker 6": 143,
    "Pacific Island-Bunker 7": 144,
    "Pacific Island-Bunker 8": 145,
    "Pacific Island-Bunker 9": 146,
    "Pacific Island-Bunker 2": 147,
    "Pacific Island-Bunker 3": 148,
    "Amazon-Beginner Weapon": 42069
}


class Transformers04Location(Location):
    game = "Transformers (2004)"
    
    # Let's make one more helper method before we begin actually creating locations.
    # Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
    # To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
    # let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
    # Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
    # so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
    def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
        return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}
    
    def create_all_locations(world: Transformers04World) -> None:
        create_regular_locations(world)
        create_events(world)
        
    def create_regular_locations(world: Transformers04World) -> None:
        # Finally, we need to put the Locations ("checks") into their regions.
        # Once again, before we do anything, we can grab our regions we created by using world.get_region()
        