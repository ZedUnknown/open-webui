import time
import psutil
import asyncio
import logging
import subprocess
from open_webui.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["DB"])

system_info = {}

def getSystemInfo():
    return system_info

# system info
# cache system info (every 6 seconds)
async def sysinfo():
    while True:
        await asyncio.to_thread(collectSystemInfo)
        await asyncio.sleep(6)

# runs in a separate thread to prevent blocking
def collectSystemInfo():
    global system_info
    gpus_info = {}
    
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=index,name,memory.total,memory.used,utilization.gpu', '--format=csv,noheader,nounits'], 
            creationflags=subprocess.CREATE_NO_WINDOW,
            capture_output=True,
            text=True
        )
        
        result = result.stdout.strip().split('\n')
        
        for raw in result:
            gpu_details = raw.split(',')
            index = int(gpu_details[0])
            name = gpu_details[1]
            memory_total = int(gpu_details[2])
            memory_used = int(gpu_details[3])
            utilization = float(gpu_details[4])
            
            gpus_info[index] = {
                'name': name,
                'memory_total': round(memory_total / 1024, 1),
                'memory_free': round((memory_total - memory_used) / 1024, 1),
                'memory_used': round(memory_used / 1024, 1),
                'utilization': round(utilization, 1)
            }
            
            # sim
            memory_total = 24 * 1024 # MB
            sim_usage = min(memory_used * 0.6, memory_total)
            memory_free = round(min(memory_total - sim_usage, memory_total) / 1024, 1)
            memory_used = round(min(sim_usage, memory_total) / 1024, 1)
            utilization = round(min(sim_usage/memory_total*100, 100), 1)
            memory_total = 24
            gpus_info[1] = {
                'name': 'NVIDIA GeForce RTX 4090',
                'memory_total': memory_total,
                'memory_free': memory_free,
                'memory_used': memory_used,
                'utilization': utilization
            }
            
    except Exception as e:
        log.error(f"Failed to get system info: {e}")
        
    try:
        cpu_usage = psutil.cpu_percent()
        ram_usage = round(psutil.virtual_memory().percent, 0)
    except Exception as e:
        log.error(f"Failed to get system info: {e}")
        return

    system_info.update({
        'cpu_usage': cpu_usage,
        'ram_usage': ram_usage,
        'gpus': gpus_info
    })
        
# uptime
init_time = time.time()

async def uptime():
    global system_info
    while True:
        current_time = time.time()
        duration = int(current_time - init_time)

        seconds = duration % 60
        minutes = (duration // 60) % 60
        hours = (duration // 3600) % 24
        days_total = duration // 86400

        years = days_total // 365
        months = (days_total % 365) // 30
        days = (days_total % 365) % 30

        uptime_str = (
            (f"{years}y:" if years > 0 else "") +
            (f"{months}m:" if months > 0 else "") +
            (f"{days}d:" if days > 0 else "") +
            (f"{hours}h:" if hours > 0 else "") +
            (f"{minutes}m:" if minutes > 0 else "") +
            (f"{seconds}s")
        )
        system_info["uptime"] = uptime_str
        await asyncio.sleep(1)