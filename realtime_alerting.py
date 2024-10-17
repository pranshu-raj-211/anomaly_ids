import logging
import time
import psutil


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def detect_anomalies(change, lower_percentile, upper_percentile):
    """
    Classify an event as an anomaly or normal event based on the historical thresholds.

    Params:
    - change (float): Change in the parameter, or last recorded value.
    - lower_percentile (float): Lower threshold.
    - upper_percentile (float): Upper threshold.
    """
    lower_threshold = lower_percentile
    upper_threshold = upper_percentile
    if change < lower_threshold or change > upper_threshold:
        return True
    return False


def print_alerts(change, metric_name):
    """
    Log alerts based on their severity."""
    if change >= 99:
        logging.warning(f"Severe anomaly detected in {metric_name}: {change}")
    elif change >= 95:
        logging.info(f"Important anomaly detected in {metric_name}: {change}")
    elif change >= 90:
        logging.info(f"Low priority anomaly detected in {metric_name}: {change}")


def monitor_system():
    """
    Run real time monitoring for the current system for the system metrics:
    - memory usage
    - disk read bytes
    - disk write bytes
    - net receive bytes
    - net send bytes
    """
    previous_disk_write_bytes = psutil.disk_io_counters().write_bytes
    previous_net_bytes_sent = psutil.net_io_counters().bytes_sent
    previous_net_bytes_recv = psutil.net_io_counters().bytes_recv

    while True:
        mem_usage = psutil.virtual_memory().percent
        disk_read_bytes = psutil.disk_io_counters().read_bytes
        disk_write_bytes = psutil.disk_io_counters().write_bytes
        net_bytes_sent = psutil.net_io_counters().bytes_sent
        net_bytes_recv = psutil.net_io_counters().bytes_recv

        disk_write_bytes_change = disk_write_bytes - previous_disk_write_bytes
        net_bytes_sent_change = net_bytes_sent - previous_net_bytes_sent
        net_bytes_recv_change = net_bytes_recv - previous_net_bytes_recv

        if detect_anomalies(disk_read_bytes, 73, 90_000_000_000):
            print_alerts(disk_read_bytes, "disk_read_bytes")
        if detect_anomalies(disk_write_bytes_change, 10, 140_000_000):
            print_alerts(disk_write_bytes_change, "disk_write_bytes_change")
        if detect_anomalies(net_bytes_sent_change, 1, 7_000_000):
            print_alerts(net_bytes_sent_change, "net_bytes_sent_change")
        if detect_anomalies(net_bytes_recv_change, 1, 1_500_000):
            print_alerts(net_bytes_recv_change, "net_bytes_recv_change")
        if detect_anomalies(mem_usage, 0, 11.1):
            print_alerts(mem_usage, "mem_usage")

        previous_disk_write_bytes = disk_write_bytes
        previous_net_bytes_sent = net_bytes_sent
        previous_net_bytes_recv = net_bytes_recv

        time.sleep(1)


if __name__ == "__main__":
    monitor_system()
