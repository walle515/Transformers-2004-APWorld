rom dataclasses import dataclass

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
    How many minicons are needed for the goal or to unlock the Unicron Fight
    """
    display_name = "Minicon Count"
    
    range_start = 20
    range_end = 40
    default = 30
    
    
class StartWithRandomWeapon(Toggle):
    """
    The starting minicon will be a random minicon instead of the default blaster
    """
    display_name = "Start with Random Weapon"
    
    
class RandomizeLevels(Toggle):
    """
    Randomize the order of the levels
    """
    display_name = "Randomize Levels"
    
    
class DataconCount(Range):
    """
    How many datacons are needed for the goal
    """
    display_name = "Datacon Count"
    
    range_start = 30
    range_end = 64
    default = 50
    
    
class GoalOption(Choice):
    """
    Can choose between Minicon Count, Bosses Killed, or Unicron Killed
    """
    display_name = "Goal Option"
    
    option_Minicon = 0
    option_Bosses = 1
    option_Unicron = 2
    option_Datacon = 3
    
    default = option_Unicron
    
    
# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class Transformers04Options(PerGameCommonOptions):
    trap_chance: TrapChance
    minicon_count: MiniconCount
    start_with_random_weapon: StartWithRandomWeapon
    datacon_count: DataconCount
    goal_option: GoalOption
    randomize_levels: RandomizeLevels
    
    # If we want to group our options by similar type, we can do so as well. This looks nice on the website.
    option_groups = [
        OptionGroup(
            "Goal Options",
            [GoalOption, MiniconCount, DataconCount],
        ),
        OptionGroup(
            "Gameplay Options",
            [RandomizeLevels, StartWithRandomWeapon, TrapChance],
        ),
    ]
    
    # Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
    option_presets = {
        "Standard":{
            "goal_option": GoalOption.option_Unicron,
            "minicon_count": 30,
            "start_with_random_weapon": False,
            "datacon_count": 50,                    #unused for this goal
            "trap_chance": 0,
            "randomize_levels": False,
        },
        "Rando":{
            "goal_option": GoalOption.option_Unicron,
            "minicon_count": 30,
            "start_with_random_weapon": True,
            "datacon_count": 50,                    #unused for this goal
            "trap_chance": 25,
            "randomize_levels": True,
        },
        "Hard Mode":{
            "goal_option": GoalOption.option_Unicron,
            "minicon_count": 40,
            "start_with_random_weapon": True,
            "datacon_count": 50,                    #unused for this goal
            "trap_chance": 75,
            "randomize_levels": True,
        },
        "Boss Fighter":{
            "goal_option": GoalOption.option_Bosses,
            "minicon_count": 30,                    #would be unused for this goal
            "start_with_random_weapon": True,
            "datacon_count": 50,                    #unused for this goal
            "trap_chance": 0,
            "randomize_levels": False,
        },
        "Scardy Cat":{
            "goal_option": GoalOption.option_Minicon,
            "minicon_count": 25,
            "start_with_random_weapon": False,
            "datacon_count": 50,                    #unused for this goal
            "trap_chance": 0,
            "randomize_levels": False,
        },
        "The Grind":{
            "goal_option": GoalOption.option_Datacon,
            "minicon_count": 30,                    #unused for this goal
            "start_with_random_weapon": False,
            "datacon_count": 64,
            "trap_chance": 0,
            "randomize_levels": True,
        }
    }