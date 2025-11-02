import asyncio
import logging
from .workers.sysinfo import getSystemInfo
from open_webui.env import SRC_LOG_LEVELS
from fastapi import APIRouter, WebSocket, HTTPException

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["DB"])

router = APIRouter()

@router.websocket("/ws/info")
async def system_info(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            system_info = getSystemInfo()
            await websocket.send_json(system_info)
            await asyncio.sleep(1)
    except Exception as e:
        log.error(f"Error in system_info: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await websocket.close()