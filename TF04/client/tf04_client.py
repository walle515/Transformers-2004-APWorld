import asyncio
import logging

from CommonClient import CommonContext, server_loop, ClientStatus
from .. import database
from ..scripts import memory_manager
from ..scripts.memory_manager import PineCommand as PineCommand
from ..scripts.memory_manager import CheatIndex as CheatIndex
from enum import IntEnum
from ..scripts import effects as Effects
from Utils import gui_enabled


# list of unhandled locations. Kept out of context incase there is some issue when someone leaves
# the game and returns later to a lost save or something.
# unhandled_locations: list[int] = []

# int to store the index of the list of received items. Same as list, leaving out of context incase
# there is a save issue and data is lost, it will try to unlock all items that were previously unlocked.





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
    items_handling = 0b111

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        
        self.game_completion = False
        
        self.logger = logging.getLogger("Client")
        self.archi_connected = asyncio.Event()
        self.debug_mode = False
        
        self.deathlink_pending = False
        self.sent_death = False
        self.deathlink_enabled = False
        
        self.bosses_killed = False
        self.cybertron_unlocked = False
        self.bosses_mode = False
        self.bosses_goal_done = False
        
        self.in_HQ = False
        self.first_HQ_visit = True
        self.previous_HQ = False
        
        self.big_head = False
        self.big_head_status = False
        
        self.random_level_enabled = False
        self.powerlink_enabled = False
        
        # Variables to store stats of autobots to display in client
        # Attack, Defense, Speed, Power
        self.Optimus_Stats = [0,0,0,0]
        self.Hot_Shot_Stats = [0,0,0,0]
        self.Red_Alert_Stats = [0,0,0,0]
        
        
    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Transformers (2004) Client"
        
        return ui
        
    
    def on_deathlink(self, data):
        self.deathlink_pending = True
        super().on_deathlink(data)
    
    def on_package(self, cmd, args):
        #self.output(f"on_package received: {cmd}")
        if cmd == "Connected":
            slot_data = args.get("slot_data", {})
            death_link_status = slot_data.get("death_link", False)
            
            self.deathlink_enabled = death_link_status
            asyncio.create_task(self.update_death_link(death_link_status))
            
            if slot_data.get("goal_option",0) == 1:
                self.bosses_mode = True
            else:
                self.bosses_mode = False
            
            self.debug_mode = slot_data.get("debug_mode", False)
            self.random_level_enabled = slot_data.get("randomize_levels", False)
            
            self.archi_connected.set()
            self.output("Connected to Server, waiting for HQ")
    
    def output(self, text: str):
        if self.debug_mode:
            self.logger.info(text)
        
    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()
        
    async def connection_closed(self):
        self.archi_connected.clear()
        await super().connection_closed()
    

# This function takes the location ID from Memory Manager and stores it in a list for the client to
# handle. It also changes the ID if it was a linked location to the location's original ID
# Needs to receive 2 arguments, the location ID and the context (already imported on MemMan as TFContext)
# def send_location(location_id: int):
    # if location_id in database.Linked_Locations:
        # location_id = database.Linked_Locations[location_id]
        
    # unhandled_locations.append(location_id)     # adds location ID to list
    # memory_manager.checked_locations.append(location_id)   # adds location ID to MemMan list
    

# Function to tell Archipelago that the game has been completed upon goal completion (typically killing Unicron)
async def Archipelago_Completed(context: Transformers04Context):
    if not context.game_completion:
        context.output("Unicron Defeated")
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
    current_health = 1.0
    num_bosses_killed = 0
    
    pine_previous_connection = False
    item_index = 0
    loc_id = 0
    num_unlocked_levels = 0
    amazon_first = False
    
    
    #Game Loop
    while not context.exit_event.is_set():
        
        #if server disconnects, wait till reconnect
        if not context.archi_connected.is_set():
            await asyncio.sleep(0.1)
            item_index = 0
            continue
        
        #if we are in the HQ and its the first visit, output it for Debug purposes
        if context.in_HQ and context.first_HQ_visit and memory_manager.pine_is_connected:
            context.first_HQ_visit = False
            context.output("First HQ Visit")
            
            #print stats of Autobots for player
            context.logger.info("Optimus Prime Stats:")
            context.logger.info(f" Attack: {context.Optimus_Stats[0]}")
            context.logger.info(f"Defense: {context.Optimus_Stats[1]}")
            context.logger.info(f"  Speed: {context.Optimus_Stats[2]}")
            context.logger.info(f"  Power: {context.Optimus_Stats[3]}")
            context.logger.info("Hot Shot Stats:")
            context.logger.info(f" Attack: {context.Hot_Shot_Stats[0]}")
            context.logger.info(f"Defense: {context.Hot_Shot_Stats[1]}")
            context.logger.info(f"  Speed: {context.Hot_Shot_Stats[2]}")
            context.logger.info(f"  Power: {context.Hot_Shot_Stats[3]}")
            context.logger.info("Red Alert Stats:")
            context.logger.info(f" Attack: {context.Red_Alert_Stats[0]}")
            context.logger.info(f"Defense: {context.Red_Alert_Stats[1]}")
            context.logger.info(f"  Speed: {context.Red_Alert_Stats[2]}")
            context.logger.info(f"  Power: {context.Red_Alert_Stats[3]}")
            
        
        #the first time pine connects to the game, make sure the checked locations list matches the archipelago
        # list. This should only happen the first time and not if the game disconnects and reconnects.
        if memory_manager.pine_is_connected and not pine_previous_connection:
            memory_manager.checked_locations.extend(context.checked_locations)
            pine_previous_connection = True





        # make sure Pine is connected and the game is not complete. If that is true, do the rest of the client code
        if memory_manager.pine_is_connected and not context.game_completion:
            
            #Unlock power link if the levels are randomized and you dont start on amazon, otherwise when 2 levels
            # have been unlocked.
            num_unlocked_levels = 0
            for x in context.items_received:
                if x.item >= 160:
                    num_unlocked_levels += 1
                    if num_unlocked_levels == 1 and x.item == database.ITEM_NAME_TO_ID["Amazon Level Unlock"]:
                        amazon_first = True
                    elif num_unlocked_levels == 1 and x.item != database.ITEM_NAME_TO_ID["Amazon Level Unlock"]:
                        amazon_first = False
            if (context.random_level_enabled and not amazon_first) or num_unlocked_levels >= 2:
                #Unlock Power Link
                memory_manager.execute_command((PineCommand.comm_unlock_sidekick,), context)
            
            #If in HQ and were not previously, unlock all available levels, then handle Big Head Mode if needed
            if context.in_HQ and not context.previous_HQ:
                context.output("In HQ")
                for x in context.items_received:
                    if x.item >= 160:
                        level = x.item - 160
                        if level == 7 and context.bosses_mode:
                            context.cybertron_unlocked = True
                        else:
                            context.output(f"Unlocking Level {database.Level_Name[level]}")
                            memory_manager.execute_command((PineCommand.comm_unlock_episode,level), context)
                for x in context.checked_locations:
                    if x in database.Boss_Locations or x == 9008:
                        level = x - 9001
                        context.output(f"Marking Level {database.Level_Name[level]} Complete")
                        memory_manager.execute_command((PineCommand.comm_complete_episode,level), context)
                if context.big_head_status:
                    context.output("Disabling Big Head")
                    context.big_head_status = False
                    asyncio.create_task(Effects.apply_effect(Effects.get_effect("CheatReset")))
                if context.big_head:
                    context.output("Enabling Big Head")
                    context.big_head = False
                    context.big_head_status = True
                    asyncio.create_task(Effects.apply_effect(Effects.get_effect("BuffBigHead")))
            context.previous_HQ = context.in_HQ
            
            
            #if bosses mode is the goal
            if context.bosses_mode:
                #count how many bosses have been killed (or alaska completed)
                num_bosses_killed = 0
                for id in context.checked_locations:
                    if id in database.Boss_Locations:
                        num_bosses_killed += 1
                #if we reached the amount, set the state true
                if num_bosses_killed >= 7:
                    context.bosses_killed = True
                #if we picked up the unicron level unlock (cybertron unlocked), killed all bosses, and have not
                #   unlocked cybertron yet, then unlock cybertron
                if context.bosses_killed and context.cybertron_unlocked and not context.bosses_goal_done:
                    memory_manager.execute_command((PineCommand.comm_unlock_episode,7), context)
                    context.bosses_goal_done = True
            
            
            #check if new location was checked and if so, send the ID to Archipelago
            if len(memory_manager.unhandled_locations) > 0:
                context.output("Unhandled Location Detected")
                loc_id = memory_manager.unhandled_locations[0]
                if loc_id == 9008:
                    asyncio.create_task(Archipelago_Completed(context))
                else:
                    # if loc_id == 0:
                        # loc_id = 42069
                    #context.output("Location ID: " + str(loc_id))
                    result = await context.check_locations([loc_id])
                    text = ", ".join(str(item) for item in result)
                    context.output(f"check_locations returned: {text}, Should be {str(loc_id)}")
                del memory_manager.unhandled_locations[0]
                
                
            # Give received items
            # context.items_received is a list of all items our game should have received from Archipelago. This helps if
            #   the game had to reconnect and get all items given while gone, or if the game had to restart from a crash
            #   or something like that. 
            
            # check if the length of received items is bigger than the index, meaning there is an item to receive
            if len(context.items_received) > item_index:
                item_id = context.items_received[item_index].item   # get the item ID
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
                    item_type = ItemType.level_unlock
                    item_id -= 160
                
                #give the item based on the type of item
                match item_type:
                    
                    case ItemType.minicon:
                        memory_manager.execute_command((PineCommand.comm_unlock_minicon,item_id), context)
                    
                    case ItemType.datacon:
                        memory_manager.unlock_datacon(item_id)
                        continue
                    
                    # case ItemType.level_unlock:
                        # context.level_unlock_detected = True
                    
                    case ItemType.special:
                        if item_id == 0:    #Health Drop
                            memory_manager.execute_command((PineCommand.comm_set_max_health,), context)
                        elif item_id == 1:   #big head
                            #asyncio.create_task(Effects.apply_effect(Effects.get_effect("BuffBigHead")))
                            context.big_head = True
                        elif item_id == 2:   #Stealth Trap
                            asyncio.create_task(Effects.apply_effect(Effects.get_effect("TrapEnemyStealth")))
                        elif item_id == 3:   #Freeze Trap
                            asyncio.create_task(Effects.apply_effect(Effects.get_effect("TrapFreeze")))
                        elif item_id == 4:   #warp trap
                            asyncio.create_task(Effects.apply_effect(Effects.get_effect("TrapWarpToHQ")))
            
            
            #Deathlink Handling
            if context.deathlink_enabled:
                #If we have received a deathlink, kill the player, and set variables as needed.
                if context.deathlink_pending:
                    asyncio.create_task(Effects.apply_effect(Effects.get_effect("StasisLock")))
                    context.deathlink_pending = False
                    context.sent_death = True
                
                #Get the current player health
                current_health = memory_manager.execute_command((PineCommand.comm_get_health,), context)
                
                #If current health is 0 or less, and a death is not currently being sent_death
                #   (deathlink isnt triggering and it doesnt sent infinite while waiting on player
                #   to hit continue or something), then send the death
                if current_health <= 0 and not context.sent_death:
                    await context.send_death("Autobot has Stasis Locked")   #Death message can be changed later
                    context.sent_death = True
                    
                #Check to see if player is back above 0 health to reset the death state
                if context.sent_death and current_health > 0:
                    context.sent_death = False
            
            
        await asyncio.sleep(0.1)
    
    
    memory_manager.execute_command((PineCommand.comm_exit,), context)
    





async def main(args):
    context = Transformers04Context(
        args.connect,
        args.password
    )
    
    context.auth = args.name
    
    # Start the Archipelago Server connection.
    # If no address was supplied, the GUI will allow us to connect.
    context.server_task = asyncio.create_task(server_loop(context), name="ServerLoop")
    
    # start the Archipelago Client Window
    if gui_enabled:
        context.run_gui()
        
    # Enable normal command-line input when available. Used by other Archipelago Processes.
    context.run_cli()
    
    await context.archi_connected.wait()
    
    #Setup the game loop to handle items and locations from the game
    asyncio.create_task(game_loop(context))
    asyncio.create_task(memory_manager.monitor_ram(context))
    
    # keep the client alive until the user closes it
    await context.exit_event.wait()
    
    context.archi_connected.clear()
    
    context.server_address = None
    await context.shutdown()







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