import asyncio
from collections.abc import Sequence

import colorama

from CommonClient import get_base_parser, handle_url_arg



def launch_tf04_client(*args: Sequence[str]) -> None:
    