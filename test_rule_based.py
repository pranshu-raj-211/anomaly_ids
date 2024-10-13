import psutil
import subprocess
import time
from multiprocessing import Process

def simulate_cpu_usage():
    subprocess.Popen(["yes"], stdout=subprocess.DEVNULL)

def simulate_memory_usage():
    a = [0] * (10**8)

def simulate_disk_write_activity():
    subprocess.Popen(["dd", "if=/dev/zero", "of=largefile", "bs=1M", "count=1024", "oflag=direct"])

def simulate_network_connections():
    subprocess.Popen(["ab", "-n", "1000", "-c", "100", "http://localhost/"])

def simulate_disk_space():
    subprocess.Popen(["dd", "if=/dev/zero", "of=largefile", "bs=1M", "count=10240"])

def simulate_network_bandwidth():
    subprocess.Popen(["wget", "http://speedtest.tele2.net/10GB.zip"])

def monitor_memory_usage():
    while True:
        memory_info = psutil.virtual_memory()
        print(f"Memory usage: {memory_info.percent}%")
        time.sleep(5)

def run_simulations():
    simulate_cpu_usage()
    time.sleep(10)
    simulate_memory_usage()
    time.sleep(10)
    simulate_disk_write_activity()
    time.sleep(10)
    simulate_network_connections()
    time.sleep(10)
    simulate_disk_space()
    time.sleep(10)
    simulate_network_bandwidth()

if __name__ == "__main__":
    memory_monitor_process = Process(target=monitor_memory_usage)
    memory_monitor_process.start()

    run_simulations()

    memory_monitor_process.terminate()
    memory_monitor_process.join()