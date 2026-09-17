from ..scripts.pine import pcsx2

INVENTORY_MEMORY_OFFSET = 0x007173C0

minicon_ids = {
    "Blaster": 1,
    "Skirmish": 2,
    "Firefight": 3,
    "Aftershock": 4,
    "Sparkjump": 5,
    "Jumpstart": 6,
    "Overwatch": 7,
    "Aurora": 8,
    "Corona": 9,
    "UltimatePrimary": 10,
    "Flashbang": 11,
    "Hailstorm": 12,
    "Knockdown": 15,
    "Airburst": 16,
    "Slapshot": 17,
    "Lock-on": 18,
    "Watchdog": 19,
    "Claymore": 20,
    "Lookout": 21,
    "Twister": 22,
    "UltimateR1": 23,
    "Shockpunch": 24,
    "Slipstream": 25,
    "UltimateGlide": 26,
    "Discord": 27,
    "Safeguard": 28,
    "Bulletproof": 29,
    "Stronghold": 30,
    "Highgear": 31,
    "Smackdown": 33,
    "Shieldwall": 34,
    "Hawkeye": 35,
    "Deflector": 36,
    "Fullspeed": 37,
    "Pressurepoint": 38,
    "Shepherd": 39,
    "Rangefinder": 40,
    "Kickback": 41,
    "Covert": 42,
    "Tractor": 43,
    "UltimateShield": 44,
    "Buildup": 45,
    "Comeback": 46,
    "Highjump": 47,
    "Failsafe": 48
}

def add_minicon(name: str):
    try:
        minicon_id = minicon_ids[name]
    except:
        print("Couldn't find minicon")
        return -1

    bit = 0x1 << (minicon_id - 1)

    old_inventory = pcsx2.read_int64(INVENTORY_MEMORY_OFFSET)

    new_inventory = old_inventory | bit

    pcsx2.write_int64(INVENTORY_MEMORY_OFFSET, new_inventory)

    print("Success")

    return 0

"""
Free memory region
start : 0x01FAECD0 end : 0x01FBEC90
"""
