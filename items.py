from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from . import database

if TYPE_CHECKING:
    from .world import Transformers04World



DEFAULT_ITEM_CLASSIFICATIONS = {
    "Blaster": ItemClassification.useful,
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
    "Datacon (None)": ItemClassification.filler,
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
    "Datacon (MovieStills7)": ItemClassification.filler,
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
    "Health Drop": ItemClassification.filler,
    "Big Head (2min)": ItemClassification.filler,
    "Stealth Trap": ItemClassification.trap,
    
    #Level Unlocks
    "Amazon Level Unlock": ItemClassification.progression,
    "Antartica Level Unlock": ItemClassification.progression,
    "Deep Amazon Level Unlock": ItemClassification.progression,
    "Mid Atlantic Level Unlock": ItemClassification.progression,
    "Alaska Level Unlock": ItemClassification.progression,
    "Starship Level Unlock": ItemClassification.progression,
    "Pacific Island Level Unlock": ItemClassification.progression,
    "Unicron Unlock": ItemClassification.progression,
    
}

class Transformers04Item(Item):
    game = "Transformers (2004)"
    
def get_random_filler_item_name(world: Transformers04World) -> str:
    if world.random.randint(0,99) < world.options.trap_chance:
        world.create_item("Stealth Trap")
        return "Stealth Trap"
    if world.random.randint(0,1) == 1:
        world.create_item("Health Drop")
        return "Health Drop"
    world.create_item("Big Head (2min)")
    return "Big Head (2min)"
    
def create_item_with_correct_classification(world: Transformers04World, name: str) -> Transformers04Item:
    # Our world class must have a create_item() function that can create any of our items by name at any time.
    # So, we make this helper function that creates the item by name with the correct classification.
    # Note: This function's content could just be the contents of world.create_item in world.py directly,
    # but it seemed nicer to have it in its own function over here in items.py.
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    
    return Transformers04Item(name, classification, database.ITEM_NAME_TO_ID[name], world.player)
    
def create_all_items(world: Transformers04World) -> None:
    rand_num = world.random.randint(0,6)
    print("TF04 World Random Num: " + str(rand_num))
    itempool: list[Item] = [
        world.create_item("Skirmish"),
        world.create_item("Firefight"),
        world.create_item("Aftershock"),
        world.create_item("Sparkjump"),
        world.create_item("Jumpstart"),
        world.create_item("Overwatch"),
        world.create_item("Aurora"),
        world.create_item("Corona"),
        #world.create_item("UltimatePrimary"),
        world.create_item("Flashbang"),
        world.create_item("Hailstorm"),
        world.create_item("Knockdown"),
        world.create_item("Airburst"),
        world.create_item("Slapshot"),
        world.create_item("Lock-on"),
        world.create_item("Watchdog"),
        world.create_item("Claymore"),
        world.create_item("Lookout"),
        world.create_item("Twister"),
        #world.create_item("UltimateR1"),
        world.create_item("Shockpunch"),
        world.create_item("Slipstream"),
        #world.create_item("UltimateGlide"),
        world.create_item("Discord"),
        world.create_item("Safeguard"),
        world.create_item("Bulletproof"),
        world.create_item("Stronghold"),
        world.create_item("Highgear"),
        world.create_item("Smackdown"),
        world.create_item("Shieldwall"),
        world.create_item("Hawkeye"),
        world.create_item("Deflector"),
        world.create_item("Fullspeed"),
        world.create_item("Pressurepoint"),
        world.create_item("Shepherd"),
        world.create_item("Rangefinder"),
        world.create_item("Kickback"),
        world.create_item("Covert"),
        world.create_item("Tractor"),
        #world.create_item("UltimateShield"),
        world.create_item("Buildup"),
        world.create_item("Comeback"),
        world.create_item("Highjump"),
        world.create_item("Failsafe"),
        world.create_item("Datacon (None)"),
        world.create_item("Datacon (CharacterEnergon)"),
        world.create_item("Datacon (RendersAutobots2)"),
        world.create_item("Datacon (CardArtwork)"),
        world.create_item("Datacon (DecepticloneSubmission)"),
        world.create_item("Datacon (LeClezio1)"),
        world.create_item("Datacon (RendersDecepticons2)"),
        world.create_item("Datacon (ConceptArtDecepticlone)"),
        world.create_item("Datacon (LeClezio2)"),
        world.create_item("Datacon (TVSeriesThemeMusic)"),
        world.create_item("Datacon (LevelStoryboardsAmazon)"),
        world.create_item("Datacon (ArtPostcards)"),
        world.create_item("Datacon (InstructionSheetOptimus)"),
        world.create_item("Datacon (ConceptArtAutobots)"),
        world.create_item("Datacon (MovieStills6)"),
        world.create_item("Datacon (MovieStills7)"),
        world.create_item("Datacon (RendersDecepticon)"),
        world.create_item("Datacon (ThemeRegurgitator)"),
        world.create_item("Datacon (MiniComic1)"),
        world.create_item("Datacon (MiniComic2)"),
        world.create_item("Datacon (MiniComic3)"),
        world.create_item("Datacon (MiniComic4)"),
        world.create_item("Datacon (ProductionArtAmazon)"),
        world.create_item("Datacon (ProductionArtAntarctica)"),
        world.create_item("Datacon (ProductionArtDeepAmazon)"),
        world.create_item("Datacon (ProductionArtMidAtlantic)"),
        world.create_item("Datacon (ProductionArtAlaska)"),
        world.create_item("Datacon (ProductionArtStarship)"),
        world.create_item("Datacon (ProdcutionArtPacificIsland)"),
        world.create_item("Datacon (ProductionArtAutobotHQ)"),
        world.create_item("Datacon (RendersAutobots)"),
        world.create_item("Datacon (RendersDecepticlone)"),
        world.create_item("Datacon (RendersMiniCons)"),
        world.create_item("Datacon (ToyProductionHotShot)"),
        world.create_item("Datacon (ToyProductionOptimus)"),
        world.create_item("Datacon (ToyProductionRedAlert)"),
        world.create_item("Datacon (ToyProductionMinicons)"),
        world.create_item("Datacon (ToyProductionCyclonus)"),
        world.create_item("Datacon (ToyProductionStarscream)"),
        world.create_item("Datacon (ToyProductionTidalWave)"),
        world.create_item("Datacon (ToyProductionMegatron)"),
        world.create_item("Datacon (RendersAutobots3)"),
        world.create_item("Datacon (CGProductionSequence2)"),
        world.create_item("Datacon (CGProductionSequence)"),
        world.create_item("Datacon (InstructionSheetMegatron)"),
        world.create_item("Datacon (InstructionSheetHotShot)"),
        world.create_item("Datacon (RendersDecepticlone2)"),
        world.create_item("Datacon (RendersDecepticlone3)"),
        world.create_item("Datacon (RendersDecepticlone4)"),
        world.create_item("Datacon (TVSpot1)"),
        world.create_item("Datacon (TVSpot2)"),
        world.create_item("Datacon (TVSpot3)"),
        world.create_item("Datacon (TVSpot4)"),
        world.create_item("Datacon (TVSpot5)"),
        world.create_item("Datacon (InstructionSheetRedAlert)"),
        world.create_item("Datacon (MovieStills1)"),
        world.create_item("Datacon (MovieStills2)"),
        world.create_item("Datacon (MovieStills3)"),
        world.create_item("Datacon (MovieStills4)"),
        world.create_item("Datacon (MovieStills5)"),
        world.create_item("Datacon (Dropbox_Wishbone)"),
        world.create_item("Datacon (ThemeDropbox)"),
        world.create_item("Datacon (LaunchPhotos)"),
        world.create_item("Datacon (ThemeOrchestral)"),
    ]
    
    if world.options.start_with_random_weapon:
        itempool.append(world.create_item("Blaster"))
    
    if world.options.randomize_levels:
        if rand_num != 0:
            itempool.append(world.create_item("Amazon Level Unlock"))
        if rand_num != 1:
            itempool.append(world.create_item("Antartica Level Unlock"))
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
        itempool.append(world.create_item("Unicron Unlock"))
    
    
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
        if rand_num == 0:
            world.push_precollected(world.create_item("Amazon Level Unlock"))
        if rand_num == 1:
            world.push_precollected(world.create_item("Antartica Level Unlock"))
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
        world.push_precollected(world.create_item("Amazon Level Unlock"))