import os
import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

SYSTEM_INFO_BASE_URL = os.environ.get("SYSTEM_INFO_BASE_URL")

@router.get("/info")
def get_system_info():
    if not SYSTEM_INFO_BASE_URL:
        raise HTTPException(status_code=500, detail="SYSTEM_INFO_BASE_URL not configured")

    try:
        result = requests.get(f"{SYSTEM_INFO_BASE_URL}/info", timeout=3)
        result.raise_for_status()
        data = result.json()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System info fetch failed: {e}")