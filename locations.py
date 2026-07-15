from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import Transformers04World
    
# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.
LOCATION_NAME_TO_ID = {
    "Amazon-Claymore Cave": 1,
    "Amazon-Spire": 2,
    "Amazon-Neighboring Mountain": 3,
    "Amazon-Ravine Cliff Cave": 4,
    "Amazon-Pressurepoint's Corner": 5,
    "Amazon-Foot of the Mountain": 6,
    "Amazon-Mountain Ruins": 7,
    "Amazon-Before the Waterfall Bridge": 8,
    "Amazon-Spidertank Triplets": 9,
    "Amazon-Ruined Temple Alcove": 10,
    "Amazon-Forest before the Bridge": 11,
    "Amazon-Ruined Temple Ledge": 12,
    "Amazon-Forest before Firefight": 13,
    "Amazon-Tutorial Minicon": 14,
    "Amazon-Ruined Temple Courtyard": 15,
    "Amazon-Light Unit Party": 16,
    "Amazon-Hidden Cave": 17,
    "Amazon-Riverside Ledge": 18,
    "Amazon-Waterfall Base": 19,
    "Amazon-Forest after the Bridge": 20,
    "Amazon-Surprise": 21,
    "Amazon-Forgettable Location": 22,
    "Amazon-Medium Unit Party": 23,
    "Amazon-Forest Across from the Basin 1": 24,
    "Amazon-Forest Across from the Basin 2": 25,
    "Antartica-Rock of Power": 26,
    "Antartica-Research Base Office 1": 27,
    "Antartica-Midfield Beacon": 28,
    "Antartica-Hide-and-Seek Champion": 29,
    "Antartica-Research Base Containers 1": 30,
    "Antartica-Research Base Containers 2": 31,
    "Antartica-Research Base Office 3": 32,
    "Antartica-Crashed Icebreaker": 33,
    "Antartica-Research Center Hangar": 34,
    "Antartica-Beachfront Property": 35,
    "Antartica-Crashed Plane": 36,
    "Antartica-Research Base Office 4": 37,
    "Antartica-Crevasse Field Overlook": 38,
    "Antartica-Lonely Island": 39,
    "Antartica-Research Base Office 2": 40,
    "Antartica-Across the Field": 41,
    "Deep Amazon-Island Altar": 42,
    "Deep Amazon-Top of the Temple": 43,
    "Deep Amazon-Spawn Ledge": 44,
    "Deep Amazon-Waterfall Rock": 45,
    "Deep Amazon-Jungle Ruins": 46,
    "Deep Amazon-Patrolling Dropship": 47,
    "Deep Amazon-Jungle Village Outskirts": 48,
    "Deep Amazon-Field before the Bridge": 49,
    "Deep Amazon-Temple Climb": 50,
    "Deep Amazon-Mid-Jungle Ditch": 51,
    "Deep Amazon-Village at the Foot of the Hill": 52,
    "Deep Amazon-Jungle Village Warpgate": 53,
    "Deep Amazon-Temple Dead End": 54,
    "Deep Amazon-Temple Pool": 55,
    "Deep Amazon-Temple Side-Path": 56,
    "Deep Amazon-Forest before the Bridge": 57,
    "Deep Amazon-Antechamber": 58,
    "Deep Amazon-Antechamber Alcove": 59,
    "Deep Amazon-Behind the Temple": 60,
    "Mid Atlantic Tidal-Vanilla Progression": 61,
    "Mid Atlantic Tidal-Distant Island": 62,
    "Mid Atlantic Tidal-Pinnacle Rock": 63,
    "Mid Atlantic Tidal-Atoll": 64,
    "Mid Atlantic Empty-Vanilla Progression": 65,
    "Mid Atlantic Empty-Distant Island": 66,
    "Mid Atlantic Empty-Atoll": 67,
    "Mid Atlantic Empty-Pinnacle Rock": 68,
    "Alaska-Mountaintop": 69,
    "Alaska-Small Forest": 70,
    "Alaska-Cave's Far Ledge": 71,
    "Alaska-Cave's Right Fork": 72,
    "Alaska-Cave's Left Fork": 73,
    "Alaska-Cave's Pool": 74,
    "Alaska-Along the Canyon": 75,
    "Alaska-Ocean Overlook": 76,
    "Alaska-Hidden Hill": 77,
    "Alaska-Canyon Clearing Ledge 1": 78,
    "Alaska-Battlefield": 79,
    "Alaska-Canyon Clearing Ledge 2": 80,
    "Alaska-Dropship Island": 81,
    "Alaska-Peninsula": 82,
    "Alaska-Escape": 83,
    "Alaska-Hillside": 84,
    "Starship-Start of the Climb": 85,
    "Starship-First Steps": 86,
    "Starship-Main Elevator": 87,
    "Starship-Sideways Elevator": 88,
    "Starship-Lower Dropship": 89,
    "Starship-Bait": 90,
    "Starship-Free Space": 91,
    "Starship-Across the Gap": 92,
    "Starship-Early Gift": 93,
    "Starship-Pristine Bridge": 94,
    "Starship-Crashed Bridge": 95,
    "Starship-Top of the Crashed Ship": 96,
    "Starship-Dropdown 1": 97,
    "Starship-Risky Jump": 98,
    "Starship-Rock 1": 99,
    "Starship-Middle Dropship": 100,
    "Starship-Dropdown 2": 101,
    "Starship-Rock 2": 102,
    "Starship-Rock 3": 103,
    "Starship-Rock 4": 104,
    "Pacific Island-Small Silo": 105,
    "Pacific Island-Moai": 106,
    "Pacific Island-Back of the Volcano": 107,
    "Pacific Island-Volcano Path": 108,
    "Pacific Island-Lighthouse": 109,
    "Pacific Island-Waterfall Climb": 110,
    "Pacific Island-Stronghold Ledge": 111,
    "Pacific Island-High Volcano Ledge": 112,
    "Pacific Island-Forest Basin": 113,
    "Pacific Island-Hidden Ledge": 114,
    "Pacific Island-Above the Waterfall": 115,
    "Pacific Island-Large Silo": 116,
    "Pacific Island-Small Island": 117,
    "Pacific Island-Bunker 1": 118,
    "Pacific Island-Bunker 4": 119,
    "Pacific Island-Bunker 5": 120,
    "Pacific Island-Bunker 6": 121,
    "Pacific Island-Bunker 7": 122,
    "Pacific Island-Bunker 8": 123,
    "Pacific Island-Bunker 9": 124,
    "Pacific Island-Bunker 2": 125,
    "Pacific Island-Bunker 3": 126,
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
        