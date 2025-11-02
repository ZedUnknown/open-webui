import psutil
import GPUtil
import time
import asyncio

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
        gpus = GPUtil.getGPUs()
        
        for gpu in gpus:
            # real
            gpus_info[gpu.id] = {
                'name': gpu.name,
                'memory_total': round(gpu.memoryTotal / 1024, 1),
                'memory_free': round(gpu.memoryFree / 1024, 1),
                'memory_used': round(gpu.memoryUsed / 1024, 1),
                'utilization': round(gpu.load, 1)
            }
            
            # sim
            sim_usage = gpu.memoryUsed*0.6
            memory_total = round(24 * 1024 / 1024, 1)
            memory_free = round(min(memory_total - sim_usage, memory_total) / 1024, 1)
            memory_used = round(min(sim_usage, memory_total) / 1024, 1)
            utilization = round(min(sim_usage/memory_total*100, 100), 1)
            gpus_info[1] = {
                'name': 'NVIDIA GeForce RTX 4090',
                'memory_total': memory_total,
                'memory_free': memory_free,
                'memory_used': memory_used,
                'utilization': utilization
            }
            
    except Exception as e:
        print(e)
        
    cpu_usage = psutil.cpu_percent()
    ram_usage = round(psutil.virtual_memory().percent, 0)
    
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