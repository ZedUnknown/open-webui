import asyncio
from .sysinfo import *

# init async workers
asyncio.gather(sysinfo(), uptime())