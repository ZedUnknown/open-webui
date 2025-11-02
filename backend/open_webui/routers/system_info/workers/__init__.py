from .sysinfo import *
import asyncio

# init async workers
asyncio.gather(sysinfo(), uptime())