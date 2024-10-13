import subprocess
import time

def simulate_cpu_usage():
    subprocess.Popen(["yes", ">", "/dev/null"])

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

simulate_cpu_usage()
time.sleep(15)
simulate_memory_usage()
time.sleep(15)
simulate_disk_write_activity()
time.sleep(15)
simulate_network_connections()
time.sleep(15)
simulate_disk_space()
time.sleep(15)
simulate_network_bandwidth()