import os
import asyncio
from fastapi import APIRouter, WebSocket, HTTPException
from .workers.sysinfo import getSystemInfo

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
        raise HTTPException(status_code=500, detail=str(e))