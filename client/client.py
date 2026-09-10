import asyncio
import logging

from CommonClient import CommonContext, server_loop, ClientStatus
from .. import database
import ..scripts.memory_manager


unhandled_locations: list[int] = []

# Context is how Archipelago stores data for the game, like slot number, name, server connections, etc.
# It also can hold variables we want persistant, so if we need to save some data and lose connection, we will still
#   have it when we reconnect. Some other data might be data we need to make poptracker more interactive, like in some
#   games where it follows what level you currently are in.
class Transformers04Context(CommonContext):
    game = "Transformers (2004)"

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        
        self.pine = None    #will change from none to pine client once we have it setup

        # Variable for setting if the pcsx2 is connected. 
        self.pine_connected = False
        
        self.game_completion = False



def send_location(location_id: int, context: Transformers04Context):
    if location_id in database.Linked_Locations:
        location_id = database.Linked_Locations[location_id]
    unhandled_locations.append(location_id)
    memory_manager.checked_locations.append(location_id)



async def game_loop(context: Transformers04Context):
    """
    This is the function that communicates between the game and the archipelago server.
    It is continuously called and run asyncronous to the archipelago server stuff.
    """

    while not context.exit_event.is_set():

        if context.pine_connected and not context.game_completion:
            
            #check if new location was checked and check it
            if unhandled_locations.len() > 0:
                context.check_location({unhandled_locations[0]})
                del unhandled_locations[0]
            # Give received items
            # context.items_received is a list of all items our game should have received from Archipelago. This helps if
            #   the game had to reconnect and get all items given while gone, or if the game had to restart from a crash
            #   or something like that. 
            
            # check goal completion
            if "Victory" in context.items_received:
                context.game_completion = True
                await context.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            

        await asyncio.sleep(0.1)
    
    





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