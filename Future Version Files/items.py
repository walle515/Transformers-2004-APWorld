from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from . import database

if TYPE_CHECKING:
    from .world import Transformers04World



DEFAULT_ITEM_CLASSIFICATIONS = {
    #"Blaster": ItemClassification.useful,
    "Skirmish": ItemClassification.progression,
    "Firefight": ItemClassification.progression,
    "Aftershock": ItemClassification.progression,
    "Sparkjump": ItemClassification.progression,
    "Jumpstart": ItemClassification.progression,
    "Overwatch": ItemClassification.progression,
    "Aurora": ItemClassification.progression,
    "Corona": ItemClassification.progression,
    
    #marking this as filler cause I dont know what it is
    #"UltimatePrimary": ItemClassification.filler,
    
    "Flashbang": ItemClassification.progression,
    "Hailstorm": ItemClassification.progression,
    "Knockdown": ItemClassification.progression,
    "Airburst": ItemClassification.progression,
    "Slapshot": ItemClassification.progression,
    "Lock-on": ItemClassification.progression,
    "Watchdog": ItemClassification.progression,
    "Claymore": ItemClassification.progression,
    "Lookout": ItemClassification.progression,
    "Twister": ItemClassification.progression,
    
    #marking this as filler cause I dont know what it is
    #"UltimateR1": ItemClassification.filler,
    
    "Shockpunch": ItemClassification.progression,
    "Slipstream": ItemClassification.progression,
    
    #marking this as filler cause I dont know what it is
    #"UltimateGlide": ItemClassification.filler,
    
    "Discord": ItemClassification.progression,
    "Safeguard": ItemClassification.progression,
    "Bulletproof": ItemClassification.progression,
    "Stronghold": ItemClassification.progression,
    "Highgear": ItemClassification.progression,
    "Smackdown": ItemClassification.progression,
    "Shieldwall": ItemClassification.progression,
    "Hawkeye": ItemClassification.progression,
    "Deflector": ItemClassification.progression,
    "Fullspeed": ItemClassification.progression,
    "Pressurepoint": ItemClassification.progression,
    "Shepherd": ItemClassification.progression,
    "Rangefinder": ItemClassification.progression,
    "Kickback": ItemClassification.progression,
    "Covert": ItemClassification.progression,
    "Tractor": ItemClassification.progression,
    
    #marking this as filler cause I dont know what it is
    #"UltimateShield": ItemClassification.filler,
    
    "Buildup": ItemClassification.progression,
    "Comeback": ItemClassification.progression,
    "Highjump": ItemClassification.progression,
    "Failsafe": ItemClassification.progression,
    
    #Adding 50 for the Datacons, not sure if this order is correct or not, but what I am doing for now
    #"Datacon (None)": ItemClassification.filler,
    "Datacon (CharacterEnergon)": ItemClassification.filler,
    "Datacon (RendersAutobots2)": ItemClassification.filler,
    "Datacon (CardArtwork)": ItemClassification.filler,
    "Datacon (DecepticloneSubmission)": ItemClassification.filler,
    "Datacon (LeClezio1)": ItemClassification.filler,
    "Datacon (RendersDecepticons2)": ItemClassification.filler,
    "Datacon (ConceptArtDecepticlone)": ItemClassification.filler,
    "Datacon (LeClezio2)": ItemClassification.filler,
    "Datacon (TVSeriesThemeMusic)": ItemClassification.filler,
    "Datacon (LevelStoryboardsAmazon)": ItemClassification.filler,
    "Datacon (ArtPostcards)": ItemClassification.filler,
    "Datacon (InstructionSheetOptimus)": ItemClassification.filler,
    "Datacon (ConceptArtAutobots)": ItemClassification.filler,
    "Datacon (MovieStills6)": ItemClassification.filler,
    #"Datacon (MovieStills7)": ItemClassification.filler,
    "Datacon (RendersDecepticon)": ItemClassification.filler,
    "Datacon (ThemeRegurgitator)": ItemClassification.filler,
    "Datacon (MiniComic1)": ItemClassification.filler,
    "Datacon (MiniComic2)": ItemClassification.filler,
    "Datacon (MiniComic3)": ItemClassification.filler,
    "Datacon (MiniComic4)": ItemClassification.filler,
    "Datacon (ProductionArtAmazon)": ItemClassification.filler,
    "Datacon (ProductionArtAntarctica)": ItemClassification.filler,
    "Datacon (ProductionArtDeepAmazon)": ItemClassification.filler,
    "Datacon (ProductionArtMidAtlantic)": ItemClassification.filler,
    "Datacon (ProductionArtAlaska)": ItemClassification.filler,
    "Datacon (ProductionArtStarship)": ItemClassification.filler,
    "Datacon (ProdcutionArtPacificIsland)": ItemClassification.filler,
    "Datacon (ProductionArtAutobotHQ)": ItemClassification.filler,
    "Datacon (RendersAutobots)": ItemClassification.filler,
    "Datacon (RendersDecepticlone)": ItemClassification.filler,
    "Datacon (RendersMiniCons)": ItemClassification.filler,
    "Datacon (ToyProductionHotShot)": ItemClassification.filler,
    "Datacon (ToyProductionOptimus)": ItemClassification.filler,
    "Datacon (ToyProductionRedAlert)": ItemClassification.filler,
    "Datacon (ToyProductionMinicons)": ItemClassification.filler,
    "Datacon (ToyProductionCyclonus)": ItemClassification.filler,
    "Datacon (ToyProductionStarscream)": ItemClassification.filler,
    "Datacon (ToyProductionTidalWave)": ItemClassification.filler,
    "Datacon (ToyProductionMegatron)": ItemClassification.filler,
    "Datacon (RendersAutobots3)": ItemClassification.filler,
    "Datacon (CGProductionSequence2)": ItemClassification.filler,
    "Datacon (CGProductionSequence)": ItemClassification.filler,
    "Datacon (InstructionSheetMegatron)": ItemClassification.filler,
    "Datacon (InstructionSheetHotShot)": ItemClassification.filler,
    "Datacon (RendersDecepticlone2)": ItemClassification.filler,
    "Datacon (RendersDecepticlone3)": ItemClassification.filler,
    "Datacon (RendersDecepticlone4)": ItemClassification.filler,
    "Datacon (TVSpot1)": ItemClassification.filler,
    "Datacon (TVSpot2)": ItemClassification.filler,
    "Datacon (TVSpot3)": ItemClassification.filler,
    "Datacon (TVSpot4)": ItemClassification.filler,
    "Datacon (TVSpot5)": ItemClassification.filler,
    "Datacon (InstructionSheetRedAlert)": ItemClassification.filler,
    "Datacon (MovieStills1)": ItemClassification.filler,
    "Datacon (MovieStills2)": ItemClassification.filler,
    "Datacon (MovieStills3)": ItemClassification.filler,
    "Datacon (MovieStills4)": ItemClassification.filler,
    "Datacon (MovieStills5)": ItemClassification.filler,
    "Datacon (Dropbox_Wishbone)": ItemClassification.filler,
    "Datacon (ThemeDropbox)": ItemClassification.filler,
    "Datacon (LaunchPhotos)": ItemClassification.filler,
    "Datacon (ThemeOrchestral)": ItemClassification.filler,
    
    #Possibly powerlink, not sure
    #"Melee Damage Enhance": ItemClassification.useful,
    
    #per requirement in world.py
    "Health Refill": ItemClassification.filler,
    "Big Head (Next Level)": ItemClassification.filler,
    "Stealth Trap": ItemClassification.trap,
    "Freeze Trap" : ItemClassification.trap,
    #"Warp Trap": ItemClassification.trap,
    
    #Level Unlocks
    "Amazon Level Unlock": ItemClassification.progression,
    "Antarctica Level Unlock": ItemClassification.progression,
    "Deep Amazon Level Unlock": ItemClassification.progression,
    "Mid Atlantic Level Unlock": ItemClassification.progression,
    "Alaska Level Unlock": ItemClassification.progression,
    "Starship Level Unlock": ItemClassification.progression,
    "Pacific Island Level Unlock": ItemClassification.progression,
    "Unicron Level Unlock": ItemClassification.progression,
    
}

class Transformers04Item(Item):
    game = "Transformers (2004)"
    


def create_item_not_starting(world,item_name):
    starting_items = world.options.start_inventory.value
    if starting_items.get(item_name, 0) == 0:
        return world.create_item(item_name)
    return None


def get_random_filler_item_name(world: Transformers04World) -> str:
    if world.random.randint(0,99) < world.options.trap_chance:
        num = world.random.randint(0,1)
        if num == 0:
            world.create_item("Stealth Trap")
            return "Stealth Trap"
        else:
            world.create_item("Freeze Trap")
            return "Freeze Trap"
        # else:
            # world.create_item ("Warp Trap")
            # return "Warp Trap"
    if world.random.randint(0,1) == 1:
        world.create_item("Health Refill")
        return "Health Refill"
    world.create_item("Big Head (Next Level)")
    return "Big Head (Next Level)"
    
def create_item_with_correct_classification(world: Transformers04World, name: str) -> Transformers04Item:
    # Our world class must have a create_item() function that can create any of our items by name at any time.
    # So, we make this helper function that creates the item by name with the correct classification.
    # Note: This function's content could just be the contents of world.create_item in world.py directly,
    # but it seemed nicer to have it in its own function over here in items.py.
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    
    return Transformers04Item(name, classification, database.ITEM_NAME_TO_ID[name], world.player)
    
def create_all_items(world: Transformers04World) -> None:
    rand_num = world.random.randint(0,6)
    rand_num_2 = world.random.randint(0,5)
    num_players = world.multiworld.players
    
    starting_items = world.options.start_inventory.value
    start_levels = [False for _ in range(len(database.Level_Unlocks))]
    start_inventory_level = False
    for x in range(len(database.Level_Unlocks)):
        if starting_items.get(database.Level_Unlocks[x], 0) > 0:
            print(f"Starting Inventory Level Detected: {database.Level_Name[x]}")
            start_levels[x] = True
            start_inventory_level = True
    add_amazon = False
    
    
    itempool: list[Item] = [
        item for item in [
            create_item_not_starting(world, "Skirmish"),
            create_item_not_starting(world, "Firefight"),
            create_item_not_starting(world, "Aftershock"),
            create_item_not_starting(world, "Sparkjump"),
            create_item_not_starting(world, "Jumpstart"),
            create_item_not_starting(world, "Overwatch"),
            create_item_not_starting(world, "Aurora"),
            create_item_not_starting(world, "Corona"),
            #create_item_not_starting(world, "UltimatePrimary"),
            create_item_not_starting(world, "Flashbang"),
            create_item_not_starting(world, "Hailstorm"),
            create_item_not_starting(world, "Knockdown"),
            create_item_not_starting(world, "Airburst"),
            create_item_not_starting(world, "Slapshot"),
            create_item_not_starting(world, "Lock-on"),
            create_item_not_starting(world, "Watchdog"),
            create_item_not_starting(world, "Claymore"),
            create_item_not_starting(world, "Lookout"),
            create_item_not_starting(world, "Twister"),
            #create_item_not_starting(world, "UltimateR1"),
            create_item_not_starting(world, "Shockpunch"),
            create_item_not_starting(world, "Slipstream"),
            #create_item_not_starting(world, "UltimateGlide"),
            create_item_not_starting(world, "Discord"),
            create_item_not_starting(world, "Safeguard"),
            create_item_not_starting(world, "Bulletproof"),
            create_item_not_starting(world, "Stronghold"),
            create_item_not_starting(world, "Highgear"),
            create_item_not_starting(world, "Smackdown"),
            create_item_not_starting(world, "Shieldwall"),
            create_item_not_starting(world, "Hawkeye"),
            create_item_not_starting(world, "Deflector"),
            create_item_not_starting(world, "Fullspeed"),
            create_item_not_starting(world, "Pressurepoint"),
            create_item_not_starting(world, "Shepherd"),
            create_item_not_starting(world, "Rangefinder"),
            create_item_not_starting(world, "Kickback"),
            create_item_not_starting(world, "Covert"),
            create_item_not_starting(world, "Tractor"),
            #create_item_not_starting(world, "UltimateShield"),
            create_item_not_starting(world, "Buildup"),
            create_item_not_starting(world, "Comeback"),
            create_item_not_starting(world, "Highjump"),
            create_item_not_starting(world, "Failsafe"),
            #create_item_not_starting(world, "Datacon (None)"),
            create_item_not_starting(world, "Datacon (CharacterEnergon)"),
            create_item_not_starting(world, "Datacon (RendersAutobots2)"),
            create_item_not_starting(world, "Datacon (CardArtwork)"),
            create_item_not_starting(world, "Datacon (DecepticloneSubmission)"),
            create_item_not_starting(world, "Datacon (LeClezio1)"),
            create_item_not_starting(world, "Datacon (RendersDecepticons2)"),
            create_item_not_starting(world, "Datacon (ConceptArtDecepticlone)"),
            create_item_not_starting(world, "Datacon (LeClezio2)"),
            create_item_not_starting(world, "Datacon (TVSeriesThemeMusic)"),
            create_item_not_starting(world, "Datacon (LevelStoryboardsAmazon)"),
            create_item_not_starting(world, "Datacon (ArtPostcards)"),
            create_item_not_starting(world, "Datacon (InstructionSheetOptimus)"),
            create_item_not_starting(world, "Datacon (ConceptArtAutobots)"),
            create_item_not_starting(world, "Datacon (MovieStills6)"),
            #create_item_not_starting(world, "Datacon (MovieStills7)"),
            create_item_not_starting(world, "Datacon (RendersDecepticon)"),
            create_item_not_starting(world, "Datacon (ThemeRegurgitator)"),
            create_item_not_starting(world, "Datacon (MiniComic1)"),
            create_item_not_starting(world, "Datacon (MiniComic2)"),
            create_item_not_starting(world, "Datacon (MiniComic3)"),
            create_item_not_starting(world, "Datacon (MiniComic4)"),
            create_item_not_starting(world, "Datacon (ProductionArtAmazon)"),
            create_item_not_starting(world, "Datacon (ProductionArtAntarctica)"),
            create_item_not_starting(world, "Datacon (ProductionArtDeepAmazon)"),
            create_item_not_starting(world, "Datacon (ProductionArtMidAtlantic)"),
            create_item_not_starting(world, "Datacon (ProductionArtAlaska)"),
            create_item_not_starting(world, "Datacon (ProductionArtStarship)"),
            create_item_not_starting(world, "Datacon (ProdcutionArtPacificIsland)"),
            create_item_not_starting(world, "Datacon (ProductionArtAutobotHQ)"),
            create_item_not_starting(world, "Datacon (RendersAutobots)"),
            create_item_not_starting(world, "Datacon (RendersDecepticlone)"),
            create_item_not_starting(world, "Datacon (RendersMiniCons)"),
            create_item_not_starting(world, "Datacon (ToyProductionHotShot)"),
            create_item_not_starting(world, "Datacon (ToyProductionOptimus)"),
            create_item_not_starting(world, "Datacon (ToyProductionRedAlert)"),
            create_item_not_starting(world, "Datacon (ToyProductionMinicons)"),
            create_item_not_starting(world, "Datacon (ToyProductionCyclonus)"),
            create_item_not_starting(world, "Datacon (ToyProductionStarscream)"),
            create_item_not_starting(world, "Datacon (ToyProductionTidalWave)"),
            create_item_not_starting(world, "Datacon (ToyProductionMegatron)"),
            create_item_not_starting(world, "Datacon (RendersAutobots3)"),
            create_item_not_starting(world, "Datacon (CGProductionSequence2)"),
            create_item_not_starting(world, "Datacon (CGProductionSequence)"),
            create_item_not_starting(world, "Datacon (InstructionSheetMegatron)"),
            create_item_not_starting(world, "Datacon (InstructionSheetHotShot)"),
            create_item_not_starting(world, "Datacon (RendersDecepticlone2)"),
            create_item_not_starting(world, "Datacon (RendersDecepticlone3)"),
            create_item_not_starting(world, "Datacon (RendersDecepticlone4)"),
            create_item_not_starting(world, "Datacon (TVSpot1)"),
            create_item_not_starting(world, "Datacon (TVSpot2)"),
            create_item_not_starting(world, "Datacon (TVSpot3)"),
            create_item_not_starting(world, "Datacon (TVSpot4)"),
            create_item_not_starting(world, "Datacon (TVSpot5)"),
            create_item_not_starting(world, "Datacon (InstructionSheetRedAlert)"),
            create_item_not_starting(world, "Datacon (MovieStills1)"),
            create_item_not_starting(world, "Datacon (MovieStills2)"),
            create_item_not_starting(world, "Datacon (MovieStills3)"),
            create_item_not_starting(world, "Datacon (MovieStills4)"),
            create_item_not_starting(world, "Datacon (MovieStills5)"),
            create_item_not_starting(world, "Datacon (Dropbox_Wishbone)"),
            create_item_not_starting(world, "Datacon (ThemeDropbox)"),
            create_item_not_starting(world, "Datacon (LaunchPhotos)"),
            create_item_not_starting(world, "Datacon (ThemeOrchestral)")
        ]
        if item is not None
    ]
    
    # if world.options.start_with_random_weapon:
        # itempool.append(world.create_item("Blaster"))
        
    if world.options.randomize_levels:
        if start_inventory_level:
            levels = 0
            for x in range(len(database.Level_Unlocks)):
                if not start_levels[x] and x != database.Level_Unlocks.index("Amazon Level Unlock"):
                    itempool.append(world.create_item(database.Level_Unlocks[x]))
                else:
                    levels += 1
            if levels == 1 and starting_items.get("Unicron Level Unlock", 0) > 0:
                add_amazon = True
            else:
                itempool.append(world.create_item("Amazon Level Unlock"))
        else:
            if world.options.add_starting_location:
                print("TF04 World Random Num: " + str(rand_num))
                if rand_num != 0:
                    itempool.append(world.create_item("Amazon Level Unlock"))
                if rand_num != 1:
                    itempool.append(world.create_item("Antarctica Level Unlock"))
                if rand_num != 2:
                    itempool.append(world.create_item("Deep Amazon Level Unlock"))
                if rand_num != 3:
                    itempool.append(world.create_item("Mid Atlantic Level Unlock"))
                if rand_num != 4:
                    itempool.append(world.create_item("Alaska Level Unlock"))
                if rand_num != 5:
                    itempool.append(world.create_item("Starship Level Unlock"))
                if rand_num != 6:
                    itempool.append(world.create_item("Pacific Island Level Unlock"))
                itempool.append(world.create_item("Unicron Level Unlock"))
            else:
                print("TF04 World Random Num: " + str(rand_num_2))
                if rand_num_2 != 0:
                    itempool.append(world.create_item("Amazon Level Unlock"))
                if rand_num_2 != 1:
                    itempool.append(world.create_item("Antarctica Level Unlock"))
                if rand_num_2 != 2:
                    itempool.append(world.create_item("Deep Amazon Level Unlock"))
                if rand_num_2 != 3:
                    itempool.append(world.create_item("Mid Atlantic Level Unlock"))
                if rand_num_2 != 4:
                    itempool.append(world.create_item("Alaska Level Unlock"))
                if rand_num_2 != 5:
                    itempool.append(world.create_item("Pacific Island Level Unlock"))
                itempool.append(world.create_item("Starship Level Unlock"))
                itempool.append(world.create_item("Unicron Level Unlock"))
    else:
        amazon_boss = world.get_location("Amazon Boss")
        amazon_boss.place_locked_item(world.create_item("Antarctica Level Unlock"))
        antarctica_boss = world.get_location("Antarctica Boss")
        antarctica_boss.place_locked_item(world.create_item("Deep Amazon Level Unlock"))
        deep_amazon_boss = world.get_location("Deep Amazon Boss")
        deep_amazon_boss.place_locked_item(world.create_item("Mid Atlantic Level Unlock"))
        mid_atlantic_boss = world.get_location("Mid Atlantic Boss")
        mid_atlantic_boss.place_locked_item(world.create_item("Alaska Level Unlock"))
        alaska_complete = world.get_location("Alaska Complete")
        alaska_complete.place_locked_item(world.create_item("Starship Level Unlock"))
        starship_boss = world.get_location("Starship Boss")
        starship_boss.place_locked_item(world.create_item("Pacific Island Level Unlock"))
        pacific_island_boss = world.get_location("Pacific Island Boss")
        pacific_island_boss.place_locked_item(world.create_item("Unicron Level Unlock"))
    
    
    
    number_of_items = len(itempool)
    
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    
    itempool+= [world.create_filler() for _ in range(needed_number_of_filler_items)]
    
    world.multiworld.itempool += itempool
    
    # Sometimes, you might want the player to start with certain items already in their inventory.
# These items are called "precollected items".
# They will be sent as soon as they connect for the first time (depending on your client's item handling flag).
# Players can add precollected items themselves via the generic "start_inventory" option.
# If you want to add your own precollected items, you can do so via world.push_precollected().
#if world.options.start_with_one_confetti_cannon:
    #starting_confetti_cannon = world.create_item("Confetti Cannon")
    #world.push_precollected(starting_confetti_cannon)
    
    if world.options.randomize_levels:
        if start_inventory_level:
            if add_amazon:
                world.push_precollected(world.create_item("Amazon Level Unlock"))
        else:
            if world.options.add_starting_location and num_players < 4:
                if rand_num == 0:
                    world.push_precollected(world.create_item("Amazon Level Unlock"))
                if rand_num == 1:
                    world.push_precollected(world.create_item("Antarctica Level Unlock"))
                if rand_num == 2:
                    world.push_precollected(world.create_item("Deep Amazon Level Unlock"))
                if rand_num == 3:
                    world.push_precollected(world.create_item("Mid Atlantic Level Unlock"))
                if rand_num == 4:
                    world.push_precollected(world.create_item("Alaska Level Unlock"))
                if rand_num == 5:
                    world.push_precollected(world.create_item("Starship Level Unlock"))
                if rand_num == 6:
                    world.push_precollected(world.create_item("Pacific Island Level Unlock"))
            else:
                if rand_num_2 == 0:
                    world.push_precollected(world.create_item("Amazon Level Unlock"))
                if rand_num_2 == 1:
                    world.push_precollected(world.create_item("Antarctica Level Unlock"))
                if rand_num_2 == 2:
                    world.push_precollected(world.create_item("Deep Amazon Level Unlock"))
                if rand_num_2 == 3:
                    world.push_precollected(world.create_item("Mid Atlantic Level Unlock"))
                if rand_num_2 == 4:
                    world.push_precollected(world.create_item("Alaska Level Unlock"))
                if rand_num_2 == 5:
                    world.push_precollected(world.create_item("Pacific Island Level Unlock"))
    else:
        world.push_precollected(world.create_item("Amazon Level Unlock"))