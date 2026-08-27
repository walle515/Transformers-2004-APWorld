from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.
# (Note: Options can also be made invisible from either of these places by overriding Option.visibility.
#  APQuest doesn't have an example of this, but this can be used for secret / hidden / advanced options.)

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md


class TrapChance(Range):
    """
    Percentage change to have a trap instead of a random filler
    """
    display_name = "Trap Chance"
    
    range_start = 0
    range_end = 99
    default = 0
    

class MiniconCount(Range):
    """
    How many minicons are needed to unlock the Unicron Fight
    """
    display_name = "Minicon Count"
    
    range_start = 20
    range_end = 40
    default = 30
    
    
class AddStartingLocation(Toggle):
    """
    Adds a location at spawn of the first level (including randomized)
    """
    display_name = "Add Starting Location"
    
    
class RandomizeLevels(Toggle):
    """
    Randomize the order of the levels.
    This creates level unlock items and adds boss fights as checks
    """
    display_name = "Randomize Levels"
    
    
class GoalOption(Choice):
    """
    Can choose between Unicron Killed or All Bosses Killed
    """
    display_name = "Goal Option"
    
    option_Unicron = 0
    option_Bosses = 1
    
    default = option_Unicron
    
    
class RandomizeStats(Toggle):
    """
    Randomize the stats of the Autobots
    """
    display_name = "Randomize Stats"
    
    
class RandomizeMiniconLevels(Toggle):
    """
    Randomize the power level of each minicon
    """
    display_name = "Randomize Minicon Power Levels"


class BalanceMiniconLevels(Toggle):
    """
    If checked, the minicon's power level will be 
    within 1 of its original level (wont go higher than 4).
    Only used with Randomize Minicon Power Levels
    """
    display_name = "Balance Minicon Power Levels"
    
    
class RandomizeMiniconColors(Toggle):
    """
    Randomize the team color for each minicon
    """
    display_name = "Randomize Minicon Team Colors"


class BalanceMiniconColors(Toggle):
    """
    Balances the number of minicons in each team color.
    Only used with Randomized Minicon Team Colors
    """
    display_name = "Balance Minicon Team Colors"
    
    
class VisibleProgressionItems(Toggle):
    """
    Changes how items appear in the game
    Off: Items for other games show as datacons only
    On: Items for other games can be minicons if they are progression or trap
    """
    display_name = "Visible Progression Items"
    
    
# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class Transformers04Options(PerGameCommonOptions):
    trap_chance: TrapChance
    minicon_count: MiniconCount
    add_starting_location: AddStartingLocation
    goal_option: GoalOption
    randomize_levels: RandomizeLevels
    randomize_stats: RandomizeStats
    randomize_mini_power: RandomizeMiniconLevels
    randomize_mini_color: RandomizeMiniconColors
    visible_progression_items: VisibleProgressionItems
    balance_minicon_levels: BalanceMiniconLevels
    balance_minicon_colors: BalanceMiniconColors
    
# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    OptionGroup(
        "Goal Options",
        [GoalOption, MiniconCount],
    ),
    OptionGroup(
        "Gameplay Options",
        [   RandomizeLevels, 
            AddStartingLocation, 
            TrapChance, 
            RandomizeStats, 
            RandomizeMiniconLevels, 
            BalanceMiniconLevels,
            RandomizeMiniconColors,
            BalanceMiniconColors,
            VisibleProgressionItems
        ],
    ),
]

# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {
    "Standard":{
        "goal_option": GoalOption.option_Unicron,
        "minicon_count": 30,
        "add_starting_location": False,
        "trap_chance": 0,
        "randomize_levels": False,
        "randomize_stats": False,
        "randomize_mini_power": False,
        "balance_minicon_levels": False,
        "randomize_mini_color": False,
        "balance_minicon_colors": False,
        "visible_progression_items": True,
    },
    "Rando":{
        "goal_option": GoalOption.option_Unicron,
        "minicon_count": 30,
        "add_starting_location": True,
        "trap_chance": 25,
        "randomize_levels": True,
        "randomize_stats": True,
        "randomize_mini_power": True,
        "balance_minicon_levels": False,
        "randomize_mini_color": True,
        "balance_minicon_colors": False,
        "visible_progression_items": False,
    },
    "Hard Mode":{
        "goal_option": GoalOption.option_Bosses,
        "minicon_count": 40,
        "add_starting_location": True,
        "trap_chance": 75,
        "randomize_levels": True,
        "randomize_stats": False,
        "randomize_mini_power": False,
        "balance_minicon_levels": False,
        "randomize_mini_color": False,
        "balance_minicon_colors": False,
        "visible_progression_items": False,
    },
    "Boss Fighter":{
        "goal_option": GoalOption.option_Bosses,
        "minicon_count": 30,
        "add_starting_location": True,
        "trap_chance": 0,
        "randomize_levels": False,
        "randomize_stats": False,
        "randomize_mini_power": False,
        "balance_minicon_levels": False,
        "randomize_mini_color": False,
        "balance_minicon_colors": False,
        "visible_progression_items": True,
    },
    
}