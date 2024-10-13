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
    previous_state = "normal"
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        current_state = "failing" if cpu_usage > CPU_THRESHOLD else "normal"
        if current_state != previous_state:
            print(f"CPU usage: {cpu_usage}% - {current_state}")
            previous_state = current_state
        await asyncio.sleep(5)


async def monitor_memory_usage():
    previous_state = "normal"
    while True:
        memory_info = psutil.virtual_memory()
        print(f'Memory usage: {memory_info.percent}')
        current_state = (
            "failing" if memory_info.percent > MEMORY_THRESHOLD else "normal"
        )
        if current_state != previous_state:
            print(f"Memory usage: {memory_info.percent}% - {current_state}")
            previous_state = current_state
        await asyncio.sleep(5)


async def monitor_disk_activity():
    previous_state = "normal"
    while True:
        disk_io = psutil.disk_io_counters()
        current_state = (
            "failing" if disk_io.write_bytes > DISK_WRITE_THRESHOLD else "normal"
        )
        if current_state != previous_state:
            print(f"Disk write activity: {disk_io.write_bytes} bytes - {current_state}")
            previous_state = current_state
        await asyncio.sleep(5)


async def monitor_network_connections():
    previous_state = "normal"
    while True:
        connections = psutil.net_connections()
        current_state = (
            "failing" if len(connections) > CONNECTION_THRESHOLD else "normal"
        )
        if current_state != previous_state:
            print(f"Network connections: {len(connections)} - {current_state}")
            previous_state = current_state
        await asyncio.sleep(5)


async def monitor_cpu_temperature():
    previous_state = "normal"
    while True:
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:
            for entry in temps["coretemp"]:
                current_state = (
                    "failing" if entry.current > CPU_TEMP_THRESHOLD else "normal"
                )
                if current_state != previous_state:
                    print(f"CPU temperature: {entry.current}°C - {current_state}")
                    previous_state = current_state
        await asyncio.sleep(5)


async def monitor_disk_space():
    previous_state = "normal"
    while True:
        disk_usage = psutil.disk_usage("/")
        current_state = (
            "failing" if disk_usage.percent > (100 - DISK_SPACE_THRESHOLD) else "normal"
        )
        if current_state != previous_state:
            print(f"Disk space usage: {disk_usage.percent}% - {current_state}")
            previous_state = current_state
        await asyncio.sleep(5)


async def monitor_network_bandwidth():
    previous_state = "normal"
    while True:
        net_io = psutil.net_io_counters()
        current_state = (
            "failing"
            if net_io.bytes_sent + net_io.bytes_recv > NETWORK_BANDWIDTH_THRESHOLD
            else "normal"
        )
        if current_state != previous_state:
            print(
                f"Network bandwidth usage: {net_io.bytes_sent + net_io.bytes_recv} bytes - {current_state}"
            )
            previous_state = current_state
        await asyncio.sleep(5)


async def main():
    await asyncio.gather(
        monitor_memory_usage(),
        monitor_cpu_usage(),
        monitor_disk_activity(),
        monitor_network_connections(),
        monitor_cpu_temperature(),
        monitor_disk_space(),
        monitor_network_bandwidth(),
    )


asyncio.run(main())
