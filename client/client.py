import asyncio
import logging

from CommonClient import CommonContext, server_loop


class Transformers04Context(CommonContext):
    """
    Archipelago client context for Transformers (2004).
    """

    game = "Transformers (2004)"

    def __init__(self, server_address, password):
        super().__init__(server_address, password)

        self.pine = None    #will become pine client

        # Used later to keep track of the game state.
        self.game_connected = False


async def game_watcher(ctx: Transformers04Context):
    """
    Watches the game and communicates with PCSX2.

    This will eventually:
        - Connect to PINE
        - Read game memory
        - Detect completed locations
        - Detect the game being beaten
        - Process received items
    """

    while not ctx.exit_event.is_set():

        # PINE connection will eventually go here.
        #
        # Example:
        # if ctx.pine is None:
        #     ctx.pine = PineClient()
        #
        # ctx.pine.connect()

        if not ctx.game_connected:
            logging.info("Waiting for Transformers / PCSX2...")
        else:
            logging.info("Transformers is connected.")

        await asyncio.sleep(1)
    
    # read game data
    
    # handle location checks
    
    # Give received items
    
    # check goal completion


async def main(args):
    """
    Main entry point for the Transformers client.
    """

    # Create the Archipelago context.
    ctx = Transformers04Context(
        args.connect,
        args.password
    )

    # Start the game watcher.
    asyncio.create_task(game_watcher(ctx))

    # Start the Archipelago network connection.
    await server_loop(ctx)


if __name__ == "__main__":
    # This normally isn't used when launched through launch.py,
    # but is useful if you run client.py directly while testing.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("connect", nargs="?", default=None)
    parser.add_argument("--password", default=None)

    args = parser.parse_args()

    asyncio.run(main(args))