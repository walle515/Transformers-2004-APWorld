from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule
from . import database
from . import options


if TYPE_CHECKING:
    from .world import Transformers04World
    
HAS_SLIPSTREAM = Has("Slipstream")
HAS_HIGHJUMP = Has("Highjump")

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
    rule_explosive = (Has("Claymore") | Has("Failsafe") | Has("Flashbang") | Has("Hailstorm")
                     | Has("Lock-on") | Has("Watchdog") | Has("Slapshot"))
    rule_slip_explosive = rule_slipstream & rule_explosive
    mid_atlantic_boss_rule = Has("Rangefinder") & rule_slipstream
    rule_all_levels = (Has("Amazon Level Unlock") &
                        Has ("Antartica Level Unlock") &
                        Has ("Deep Amazon Level Unlock") & 
                        Has ("Mid Atlantic Level Unlock") &
                        Has ("Alaska Level Unlock") &
                        Has ("Starship Level Unlock") &
                        Has ("Pacific Island Level Unlock") &
                        rule_slip_high)
    
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
    
    world.set_rule(world.get_location("Defeat All Bosses"), rule_all_levels)
    
    
def set_completion_condition(world: Transformers04World) -> None:
    world.set_completion_rule(Has("Victory"))