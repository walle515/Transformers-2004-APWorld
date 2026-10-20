from enum import IntEnum
from .pine import Pine, pcsx2

class CodeAddress(IntEnum):
    codeadd_episode_complete = 0x351B0C
    codeadd_pickup_spawn_check = 0x379EF8
    codeadd_pickup_collected = 0x1FAECE0
    cleanadd_pickup_spawn_custom = 0x1FAEF00

def remove_pickup_limit():
    # increase PickupPlaced limit from 13 to 32 (0x14)
    pcsx2.write_int32(0x379534, 0x2A230020)

def remove_slipstream_cutscene():
    # Fix Slipstream pickup (remove check for special camera script)
    pcsx2.write_int32(0x37BC3C, 0x10000014)

def redirect_pickup_collection():
    # write pickup redirection code
    pcsx2.write_int32(0x37DCC0, 0x0C7EBB38)
    pcsx2.write_int32(CodeAddress.codeadd_pickup_collected, 0x3C0201FB)  # lui v0,0x01FB
    pcsx2.write_int32(CodeAddress.codeadd_pickup_collected + 0x4, 0x2442ECD0)  # addiu v0,v0,-0x1330
    pcsx2.write_int32(CodeAddress.codeadd_pickup_collected + 0x8, 0xAC400008)  # sw zero,0x8(v0)
    pcsx2.write_int32(CodeAddress.codeadd_pickup_collected + 0xC, 0xAC440000)  # sw a0,0x0(v0) <- loop to here
    pcsx2.write_int32(CodeAddress.codeadd_pickup_collected + 0x10, 0x8C510008)  # lw s1,0x8(v0)
    pcsx2.write_int32(CodeAddress.codeadd_pickup_collected + 0x14, 0x1220FFFD)  # beqz s1
    pcsx2.write_int32(CodeAddress.codeadd_pickup_collected + 0x18, 0)  # NOP
    pcsx2.write_int32(CodeAddress.codeadd_pickup_collected + 0x1C, 0x03E00008)  # jr ra
    pcsx2.write_int32(CodeAddress.codeadd_pickup_collected + 0x20, 0x0080882D)  # daddu s1,a0,zero

def redirect_episode_unlock():
    # This line stops the SetEpisodeCompleted function from unlocking the next episode
    # all of the code from 0x351B10 to 0x351B9C is free to use, since the code in this range is ignored by us.
    # pcsx2.write_int32(0x00351B0C, 0x10000024) #single-line mod to just skip the unlock of the next episode
    # write the index of the current episode to 0x0x1FAEE00, then skip to the next part of the function
    pcsx2.write_int32(CodeAddress.codeadd_episode_complete, 0x3C0201FB)  # lui v0,0x01FB
    pcsx2.write_int32(CodeAddress.codeadd_episode_complete + 0x4, 0x2442EE00)  # addiu v0,v0,-0x1300
    pcsx2.write_int32(CodeAddress.codeadd_episode_complete + 0xC, 0xAC420000)  # sw v0,0x0(v0)
    pcsx2.write_int32(CodeAddress.codeadd_episode_complete + 0x8, 0xAC450004)  # sw a1,0x4(v0)
    pcsx2.write_int32(CodeAddress.codeadd_episode_complete + 0x10, 0x10000020)  # beq zero,zero,0x00351BA0
    pcsx2.write_int32(CodeAddress.codeadd_episode_complete + 0x14, 0xAC830034)  # sw v1,0x34(a0)

def redirect_pickup_spawn():
    # During the taPickupPlaced::Spawn function, there is a check to see if the pickup has already been unlocked
    # OLD CODE: (since we use the same minicon for multiple pickups, we need to adjust this function to also check if
    # the minicon was an Archipelago pickup. This means the game will have to wait on a response from Archi)
    # NEW CODE: Since Archipelago should be our sole arbiter of what has and hasn't been collected, we remove this check
    # entirely and replace it with our own. The game will still need to wait on a response from Archi.

    # These replace the check for Minicon locations
    pcsx2.write_int32(CodeAddress.codeadd_pickup_spawn_check, 0x0C7EBBC0)  # jal 0x1FAEF00
    pcsx2.write_int32(CodeAddress.codeadd_pickup_spawn_check + 0x4, 0x0)

    # These replace the check for Datacon locations
    pcsx2.write_int32(CodeAddress.codeadd_pickup_spawn_check + 0xB0, 0x0C7EBBC0)  # jal 0x1FAEF00
    pcsx2.write_int32(CodeAddress.codeadd_pickup_spawn_check + 0xB4, 0x0)
    # s2 = pointer to current pickupplaced object
    # v0 is safe
    # s0 = current minicon ID, or current datacon

    pcsx2.write_int32(CodeAddress.cleanadd_pickup_spawn_custom, 0x0000802D)  # daddu s0, zero, zero #at this point, s0 is safe. we can use it to load the current location
    pcsx2.write_int32(CodeAddress.cleanadd_pickup_spawn_custom + 0x4, 0x3C0201FB)  # lui v0, 1FB
    pcsx2.write_int32(CodeAddress.cleanadd_pickup_spawn_custom + 0x8, 0x2442EEF4)  # addiu v0, EEF4 #Set target read location to 1FAEEF4
    pcsx2.write_int32(CodeAddress.cleanadd_pickup_spawn_custom + 0xC, 0xAC400004)  # sw zero, 4(v0) #reset the process complete
    pcsx2.write_int32(CodeAddress.cleanadd_pickup_spawn_custom + 0x10, 0xAC520000)  # sw s2, 0(v0) <- loop to here #store the current pickup pointer for Archi to grab
    pcsx2.write_int32(CodeAddress.cleanadd_pickup_spawn_custom + 0x14, 0x8C500004)  # lw s0 4(v0) #when the client processes the s2 value, write the pass/fail at v0+8 and the process complete at v0+4
    pcsx2.write_int32(CodeAddress.cleanadd_pickup_spawn_custom + 0x18, 0x1200FFFD)  # beqz s0 <- loop from here
    pcsx2.write_int32(CodeAddress.cleanadd_pickup_spawn_custom + 0x1C, 0x8C430008)  # lw v1 8(v0) #read the result into v1
    pcsx2.write_int32(CodeAddress.cleanadd_pickup_spawn_custom + 0x20, 0x03E00008)  # jr ra
    # NOP (don't need to write this, it's already there)

def write_code_mods():
    '''Writes single-line ELF codes to allow Archipelago randomizers to work'''

    remove_pickup_limit()

    remove_slipstream_cutscene()

    redirect_pickup_collection()

    redirect_episode_unlock()

    redirect_pickup_spawn()
