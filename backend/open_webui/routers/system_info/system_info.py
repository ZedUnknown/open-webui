import asyncio
import logging
import asyncio
from .workers.sysinfo import sysinfo, uptime, getSystemInfo
from open_webui.env import SRC_LOG_LEVELS
from fastapi import APIRouter, WebSocket

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["DB"])

router = APIRouter()

# init async workers
@router.on_event("startup")
async def startup_event():
    asyncio.gather(sysinfo(), uptime())

@router.websocket("/ws/info")
async def system_info(websocket: WebSocket):
    # front end is doing the closing
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(getSystemInfo())
            await asyncio.sleep(1)
    except Exception as e:
        log.error(f"Error in system_info: {e}")