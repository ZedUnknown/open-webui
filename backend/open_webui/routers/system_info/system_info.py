import asyncio
import logging
import asyncio
from .workers.sysinfo import getSystemInfo
from open_webui.env import SRC_LOG_LEVELS
from fastapi import APIRouter, WebSocket

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["DB"])

router = APIRouter()

@router.websocket("/ws/info")
async def system_info(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(getSystemInfo())
            await asyncio.sleep(1)
    except Exception as e:
        log.error(f"Error in system_info: {e}")
    finally:
        if not websocket.client_state.name != "DISCONNECTED": # only close if still open.
            await websocket.close()