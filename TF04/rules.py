from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule
from . import database
from . import options
from worlds.generic.Rules import add_item_rule


if TYPE_CHECKING:
    from .world import Transformers04World
    

#make numData and numMini
# HAS_DATACONS = numData > world.options.datacon_count
# HAS_MINICONS = numMini > world.options.minicon_count

def set_all_rules(world: Transformers04World) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)
    
    
def set_all_entrance_rules(world: Transformers04World) -> None:
    mid_atlantic_entrance = world.get_entrance("Mid Atlantic Unlocked")
    mid_atlantic_rule = Has("Mid Atlantic Level Unlock")# & Has("Rangefinder")
    
    world.set_rule(mid_atlantic_entrance, mid_atlantic_rule)
    
    unicron_entrance = world.get_entrance("Unicron Unlocked")
    
    number_minicons = lambda state: sum(state.has(minicon, world.player) for minicon in database.Minicons) >= world.options.minicon_count.value
    
    unicron_entrance_rule = lambda state: (number_minicons(state) 
                                            and state.has("Unicron Level Unlock", world.player)
                                            and (state.has("All Bosses Beaten", world.player) or (world.options.goal_option != options.GoalOption.option_Bosses)))
    world.set_rule(unicron_entrance, unicron_entrance_rule)
    


def set_all_location_rules(world: Transformers04World) -> None:
    rule_slipstream = Has("Slipstream")
    rule_highjump = Has("Highjump")
    rule_slip_high = rule_slipstream & rule_highjump
    rule_dash = Has("Highgear") | Has("Fullspeed")
    rule_starship_tall_rock = rule_slip_high & rule_dash
    rule_explosive = (Has("Claymore") | Has("Failsafe") | Has("Flashbang") | Has("Hailstorm")
                     | Has("Lock-on") | Has("Watchdog") | Has("Slapshot"))
    rule_slip_explosive = rule_slipstream & rule_explosive
    mid_atlantic_boss_rule = (Has("Rangefinder") | Has("Lookout"))& rule_slipstream
    rule_all_levels = (Has("Amazon Level Unlock") &
                        Has ("Antarctica Level Unlock") &
                        Has ("Deep Amazon Level Unlock") & 
                        Has ("Mid Atlantic Level Unlock") &
                        Has ("Alaska Level Unlock") &
                        Has ("Starship Level Unlock") &
                        Has ("Pacific Island Level Unlock") &
                        rule_slip_high)
    rule_slip_or_high = rule_slipstream | rule_highjump
    rule_damage_boost = Has("Flashbang") | Has("Hailstorm")
    rule_dash_or_hail = rule_dash | Has("Hailstorm")
    rule_dash_and_high = rule_dash & rule_highjump
    rule_dash_or_damageboost = rule_dash | rule_damage_boost
    
    world.set_rule(world.get_location("Defeat All Bosses"), rule_all_levels)
    
    if world.options.logic_difficulty == options.LogicDifficulty.option_Default:
        world.set_rule(world.get_location("Amazon-Spidertank Triplets"), rule_slip_or_high)
        world.set_rule(world.get_location("Mid Atlantic Boss"), mid_atlantic_boss_rule)
        
        for location in database.Explosive_Locations:
            world.set_rule(world.get_location(location), rule_explosive)
        
        for location in database.Slipstream_Locations:
            world.set_rule(world.get_location(location), rule_slipstream)
        
        for location in database.Slipstream_Explosive:
            world.set_rule(world.get_location(location), rule_slip_explosive)
        
        for location in database.Highjump_Locations:
            world.set_rule(world.get_location(location), rule_highjump)
        
        for location in database.Slipstream_Highjump:
            world.set_rule(world.get_location(location), rule_slip_high)
            
        for location in database.Starship_Tall_Rocks:
            world.set_rule(world.get_location(location), rule_starship_tall_rock)
    
    
    
    elif world.options.logic_difficulty == options.LogicDifficulty.option_Easy_Skips:
        world.set_rule(world.get_location("Mid Atlantic Boss"), mid_atlantic_boss_rule)
        for location in database.Slipstream_Easy_Hailstorm_Skips:
            world.set_rule(world.get_location(location), Has("Hailstorm") | rule_slipstream)
        
        for location in database.Slipstream_Easy_Dash_Skips:
            world.set_rule(world.get_location(location), rule_dash | rule_slipstream)
         
        for location in database.Slipstream_Easy_Dash_or_Hailstorm_Skips:
            world.set_rule(world.get_location(location), rule_dash_or_hail | rule_slipstream)
        
        for location in database.Slipstream_Easy_Dash_and_Highjump_Skips:
            world.set_rule(world.get_location(location), rule_dash_and_high | rule_slipstream)
        
        for location in database.Slipstream_Easy_Skips:
            world.set_rule(world.get_location(location), rule_slipstream)
        
        for location in database.Highjump_Easy_Skips:
            world.set_rule(world.get_location(location), rule_highjump)
        
        for location in database.Starship_Tall_Rocks:
            world.set_rule(world.get_location(location), rule_starship_tall_rock)
        
        for location in database.Explosive_Locations:
            world.set_rule(world.get_location(location), rule_explosive)
        
        for location in database.Slipstream_Explosive:
            world.set_rule(world.get_location(location), rule_slip_explosive)
    
    
    
    elif world.options.logic_difficulty == options.LogicDifficulty.option_Hard_Skips:
        world.set_rule(world.get_location("Mid Atlantic Boss"), rule_slipstream)
        for location in database.Slipstream_Hard_Dash_Skips:
            world.set_rule(world.get_location(location), rule_dash | rule_slipstream)
        
        for location in database.Slipstream_Hard_Dash_or_Flashbang_Skips:
            world.set_rule(world.get_location(location), rule_dash_or_damageboost | rule_slipstream)
        
        for location in database.Slipstream_Hard_Hailstorm_Skips:
            world.set_rule(world.get_location(location), Has("Hailstorm") | rule_slipstream)
        
        for location in database.Slipstream_Hard_Hailstorm_or_Dash_Skips:
            world.set_rule(world.get_location(location), rule_dash_or_hail | rule_slipstream)
        
        for location in database.Slipstream_Hard_Flashbang_Skips:
            world.set_rule(world.get_location(location), rule_damage_boost | rule_slipstream)
        
        for location in database.Highjump_Hard_Slipstream_Skips:
            world.set_rule(world.get_location(location), rule_slipstream | rule_highjump)
        
        for location in database.Starship_Tall_Rocks:
            world.set_rule(world.get_location(location), rule_slipstream)
        
        for location in database.Slipstream_Hard_Skips:
            world.set_rule(world.get_location(location), rule_slipstream)
        
        for location in database.Explosive_Hard_Skips:
            world.set_rule(world.get_location(location), rule_explosive)
    
    
def set_completion_condition(world: Transformers04World) -> None:
    world.set_completion_rule(Has("Victory"))