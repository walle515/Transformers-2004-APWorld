from . import memory_manager as memman
from asyncio import sleep
from enum import IntEnum
from .pine import pcsx2

'''Most of this file should be self-contained. If everything is set up correctly, the only things that 
should be needed from outside are:
get_effect(effect_name:str) (defined in __init__)
async apply_effect(effect: return value from get_effect)'''

class EffectStyle(IntEnum):
    style_invalid = -1
    style_cheat = 0
    style_mission_status = 1

class GameEffect:
    ID: int
    name: str
    is_trap: bool #either a trap or a buff. This is mainly for clarity, as far as I can imagine
    effect_style: int
    value: int #the CheatIndex for cheats, mission status for statuses
    duration: int #in seconds. Duration of 0 is an instant effect, duration of -1 is a permanent effect

    def __init__(self, name_str, is_trap_bool, effect_style_int, value_int, duration_int):
        self.name = name_str
        self.is_trap = is_trap_bool
        self.effect_style = effect_style_int
        self.value = value_int
        self.duration = duration_int


effect_list: list[GameEffect] = []

def __init__():
    #Create all effects here
    # These first two serve as resets, in case we ever need to ensure that no effects are active
    # The other effects should automatically reset themselves once their timers wear off
    effect_list.append(GameEffect("CheatReset", False, EffectStyle.style_cheat
                                  , memman.CheatIndex.cheat_reset, 0))
    effect_list.append(GameEffect("StatusReset", False, EffectStyle.style_mission_status
                                  , memman.MissionStatus.status_normal, -1))
    effect_list.append(GameEffect("TrapEnemyStealth", True, EffectStyle.style_cheat
                                  , memman.CheatIndex.cheat_enemystealth, 30))
    effect_list.append(GameEffect("TrapTrubo", True, EffectStyle.style_cheat
                                  , memman.CheatIndex.cheat_turbo, 60))
    effect_list.append(GameEffect("TrapFreeze", True, EffectStyle.style_mission_status
                                  , memman.MissionStatus.status_freeze, 10))
    effect_list.append(GameEffect("TrapWarpToHQ", True, EffectStyle.style_mission_status
                                  , memman.MissionStatus.status_HQ_warp, -1)) #the game will overwrite this one for us
    effect_list.append(GameEffect("BuffImmortality", False, EffectStyle.style_cheat
                                  , memman.CheatIndex.cheat_immortal, 10))
    effect_list.append(GameEffect("BuffTractor", False, EffectStyle.style_cheat
                                  , memman.CheatIndex.cheat_tractor, -1))
    effect_list.append(GameEffect("BuffBigHead", False, EffectStyle.style_cheat
                                  , memman.CheatIndex.cheat_bighead, -1))
    effect_list.append(GameEffect("StasisLock", True, EffectStyle.style_mission_status
                                  , memman.MissionStatus.status_stasis_lock, 0))

def get_effect(effect_name: str) -> GameEffect:
    for effect in effect_list:
        if effect.name == effect_name:
            return effect
    return GameEffect("NULL", False, EffectStyle.style_invalid, 0, 0)

async def apply_effect(effect: GameEffect, context):
    time_remaining = 0.0
    if effect.effect_style == EffectStyle.style_cheat:
        memman.cheat_toggle(effect.value, True)
    elif effect.effect_style == EffectStyle.style_mission_status:
        memman.set_mission_status(effect.value)

    if effect.duration > 0:
        time_remaining = effect.duration
        #await sleep(18)
        #await sleep(effect.duration)
        while (time_remaining > 0):
            if (not (pcsx2.read_int32(0x006CFB94) & 0x1)) and (not context.inHQ):
                time_remaining -= 0.1
            await asyncio.sleep(0.1)
    elif effect.duration < 0:
        return
    #skip over exactly 0, since that's handled below as an instant effect
    await asyncio.sleep(0.1) #we wait a fraction of a second so the game will have a chance to read the value we wrote

    if effect.effect_style == EffectStyle.style_cheat:
        memman.cheat_toggle(effect.value, False)
    elif effect.effect_style == EffectStyle.style_mission_status:
        memman.set_mission_status(memman.MissionStatus.status_normal)
