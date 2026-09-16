import asyncio
import logging

from CommonClient import CommonContext, server_loop, ClientStatus
from .. import database
import ..scripts.memory_manager
from ..scripts.memory_manager import PineCommand as PineCommand
from ..scripts.memory_manager import CheatIndex as CheatIndex
from enum import IntEnum
import ..scripts.effects as Effects


# list of unhandled locations. Kept out of context incase there is some issue when someone leaves
# the game and returns later to a lost save or something.
unhandled_locations: list[int] = []

# int to store the index of the list of received items. Same as list, leaving out of context incase
# there is a save issue and data is lost, it will try to unlock all items that were previously unlocked.
item_index = 0


#Enum for what type of item is received
class ItemType(IntEnum):
    minicon = 0
    datacon = 1
    level_unlock = 2
    special = 3

# Context is how Archipelago stores data for the game, like slot number, name, server connections, etc.
# It also can hold variables we want persistant, so if we need to save some data and lose connection, we will still
#   have it when we reconnect. Some other data might be data we need to make poptracker more interactive, like in some
#   games where it follows what level you currently are in.
class Transformers04Context(CommonContext):
    game = "Transformers (2004)"

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        
        self.pine = None    #will change from none to pine client once we have it setup

        # Variable for setting if the pcsx2 is connected. Set in MemMan
        self.pine_connected = False
        
        self.game_completion = False
        
        #self.item_last_index = 0


# This function takes the location ID from Memory Manager and stores it in a list for the client to
# handle. It also changes the ID if it was a linked location to the location's original ID
# Needs to receive 2 arguments, the location ID and the context (already imported on MemMan as TFContext)
def send_location(location_id: int, context: Transformers04Context):
    if location_id in database.Linked_Locations:
        location_id = database.Linked_Locations[location_id]
        
    unhandled_locations.append(location_id)     # adds location ID to list
    memory_manager.checked_locations.append(location_id)   # adds location ID to MemMan list
    

# Function to tell Archipelago that the game has been completed upon goal completion (typically killing Unicron)
async def Archipelago_Completed(context: Transformers04Context):
    if not context.game_completion:
        context.game_completion = True
        await context.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])



async def game_loop(context: Transformers04Context):
    """
    This is the function that communicates between the game and the archipelago server.
    It is continuously called and run asyncronous to the archipelago server stuff.
    """
    
    #item = ""
    item_id = 0
    item_type = ItemType.minicon

    while not context.exit_event.is_set():

        # make sure Pine is connected and the game is not complete
        if context.pine_connected and not context.game_completion:
            
            #check if new location was checked and if so, send the ID to Archipelago
            if len(unhandled_locations) > 0:
                context.check_location({unhandled_locations[0]})
                del unhandled_locations[0]
                
                
            # Give received items
            # context.items_received is a list of all items our game should have received from Archipelago. This helps if
            #   the game had to reconnect and get all items given while gone, or if the game had to restart from a crash
            #   or something like that. 
            
            # check if the length of received items is bigger than the index, meaning there is an item to receive
            if len(context.items_received) > item_index:
                item_id = context.items_received(item_index).item   # get the item ID
                item_index += 1     #increase the index
                
                #if the ID is less than 50, then the item is a minicon
                if item_id < 50:
                    item_type = ItemType.minicon
                    
                #if the item is somewhere between 50 and 150, its a datacon, so we need to subtract 50 from the ID
                elif item_id < 150:
                    item_type = ItemType.datacon
                    item_id -= 50
                    
                #if its between 150 and 160, its a special item, like a trap or health drop, so subtract 150
                elif item_id < 160:
                    item_type = ItemType.special
                    item_id -= 150
                    
                # if its 160 or higher, its a level unlock, so subtract 160 (level ids range from 0-7)
                else:
                    item_type = Item_Type.level_unlock
                    item_id -= 160
                
                #give the item based on the type of item
                match item_type:
                    
                    case ItemType.minicon:
                        memory_manager.execute_command((PineCommand.comm_unlock_minicon,item_id))
                    
                    case ItemType.datacon:
                        memory_manager.unlock_datacon(item_id)
                        continue
                    
                    case ItemType.level_unlock:
                        memory_manager.execute_command((PineCommand.comm_unlock_episode,item_id))
                    
                    case ItemType.special:
                        if item_id == 0:    #Health Drop
                            memory_manager.execute_command((PineCommand.comm_set_max_health,))
                        elif item_id == 1:   #big head
                            asyncio.create_task(Effects.apply_effect(Effects.get_effect("BuffBigHead")))
                        elif item_id == 2:   #Stealth Trap
                            asyncio.create_task(Effects.apply_effect(Effects.get_effect("TrapEnemyStealth")))
                        elif item_id == 3:   #Freeze Trap
                            asyncio.create_task(Effects.apply_effect(Effects.get_effect("TrapFreeze")))
                        elif item_id == 4:   #warp trap
                            asyncio.create_task(Effects.apply_effect(Effects.get_effect("TrapWarpToHQ")))

        await asyncio.sleep(0.1)
    
    
    memory_manager.execute_command((PineCommand.comm_exit,))
    





async def main(args):
    context = Transformers04Context(
        args.connect,
        args.password
    )
    
    #Setup the game loop to handle items and locations from the game
    asyncio.create_task(game_loop(context))
    asyncio.create_task(memory_manager())

    # Start the Archipelago network connection.
    await server_loop(context)







# This is only if we want to test the client without using the APLauncher.
# I personally plan to use the launcher, so I will comment it out.
"""
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("connect", nargs="?", default=None)
    parser.add_argument("--password", default=None)

    args = parser.parse_args()

    asyncio.run(main(args))
"""