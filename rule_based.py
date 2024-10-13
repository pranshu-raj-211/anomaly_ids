import psutil
import asyncio

CPU_THRESHOLD = 60.0
MEMORY_THRESHOLD = 90.0
DISK_WRITE_THRESHOLD = 10_000_000
CONNECTION_THRESHOLD = 50
CPU_TEMP_THRESHOLD = 75.0
DISK_SPACE_THRESHOLD = 10.0
NETWORK_BANDWIDTH_THRESHOLD = 10_000_000

async def monitor_cpu_usage():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > CPU_THRESHOLD:
            print(f"ALERT: High CPU usage detected! {cpu_usage}%")
        await asyncio.sleep(5)

async def monitor_memory_usage():
    while True:
        memory_info = psutil.virtual_memory()
        if memory_info.percent > MEMORY_THRESHOLD:
            print(f"ALERT: High memory usage detected! {memory_info.percent}%")
        await asyncio.sleep(5)

async def monitor_disk_activity():
    while True:
        disk_io = psutil.disk_io_counters()
        if disk_io.write_bytes > DISK_WRITE_THRESHOLD:
            print(f"ALERT: Unusual disk activity detected! {disk_io.write_bytes} bytes written")
        await asyncio.sleep(5)

async def monitor_network_connections():
    while True:
        connections = psutil.net_connections()
        if len(connections) > CONNECTION_THRESHOLD:
            print(f"ALERT: Unusually high number of network connections! {len(connections)}")
        await asyncio.sleep(5)

async def monitor_cpu_temperature():
    while True:
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            for entry in temps['coretemp']:
                if entry.current > CPU_TEMP_THRESHOLD:
                    print(f"ALERT: High CPU temperature detected! {entry.current}°C")
        await asyncio.sleep(5)

async def monitor_disk_space():
    while True:
        disk_usage = psutil.disk_usage('/')
        if disk_usage.percent > (100 - DISK_SPACE_THRESHOLD):
            print(f"ALERT: Low disk space available! {disk_usage.percent}% used")
        await asyncio.sleep(5)

async def monitor_network_bandwidth():
    while True:
        net_io = psutil.net_io_counters()
        if net_io.bytes_sent + net_io.bytes_recv > NETWORK_BANDWIDTH_THRESHOLD:
            print(f"ALERT: High network bandwidth usage detected! {net_io.bytes_sent + net_io.bytes_recv} bytes")
        await asyncio.sleep(5)

async def main():
    await asyncio.gather(
        monitor_cpu_usage(),
        monitor_memory_usage(),
        monitor_disk_activity(),
        monitor_network_connections(),
        monitor_cpu_temperature(),
        monitor_disk_space(),
        monitor_network_bandwidth()
    )

asyncio.run(main())