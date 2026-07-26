from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule


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
    mid_atlantic_rule = Has("Mid Atlantic Level Unlock") & Has("Rangefinder")
    world.set_rule(mid_atlantic_entrance, mid_atlantic_rule)
    
    unicron_entrance = world.get_entrance("Unicron Unlocked")
    
    def minicons_collected(state: CollectionState) -> int:
        numMini = 0
        from .database import Minicons
        for mini in Minicons[]:
            if Has(mini):
                numMini += 1
        return numMini
    
    unicron_entrance_rule = lambda state: (minicons_collected(state) >= world.options.minicon_count.value
                                            and state.has("Unicron Level Unlock", self.player)
                                            and (state.has("All Bosses Beaten", self.player) | (world.options.goal_option.value != 1))
    


def set_all_location_rules(world: Transformers04World) -> None:
    rule_slipstream = Has("Slipstream")
    rule_highjump = Has("Highjump")
    rule_slip_high = rule_slipstream | rule_highjump
    rule_explosive = (Has("Claymore") | Has("Failsafe") | Has("Flashbang") | Has("Hailstorm")
                     | Has("Lock-on") | Has("Watchdog") | Has("Slapshot"))
    rule_slip_explosive = rule_slipstream & rule_explosive
    
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
    
    
    
def set_completion_condition(world: Transformers04World) -> None:
    world.set_completion_rule(Has("Victory"))