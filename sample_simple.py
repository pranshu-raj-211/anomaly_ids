import psutil
import time
import logging

logging.basicConfig(filename='usage.log', filemode='a', level=logging.INFO, format='%(asctime)s,%(message)s')

while True:
    # cpu_usage = psutil.cpu_percent(interval=1)
    mem_usage = psutil.virtual_memory().percent
    disk_io = psutil.disk_io_counters()
    net_io = psutil.net_io_counters()

    log_message = f"{mem_usage},{disk_io.read_bytes},{disk_io.write_bytes},{net_io.bytes_sent},{net_io.bytes_recv}"
    
    logging.info(log_message)
    time.sleep(1)