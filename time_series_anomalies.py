import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = np.genfromtxt('usage.log', delimiter=',', skip_header=1, dtype=float, usecols=(1, 2, 3, 4, 5, 6))

mem_usage = data[:, 1]
disk_read_bytes = data[:, 2]
disk_write_bytes = data[:, 3]
net_bytes_sent = data[:, 4]
net_bytes_recv = data[:, 5]

def print_statistics(name, data):
    print(f"\n{name}:")
    print(f"  Mean: {np.mean(data)}")
    print(f"  Max: {np.max(data)}")
    print(f"  Min: {np.min(data)}")
    print(f"  Variance: {np.var(data)}")
    print(f"  Standard Deviation: {np.std(data)}")
    print(f"  90th Percentile: {np.percentile(data, 90)}")
    print(f"  95th Percentile: {np.percentile(data, 95)}")

def plot_kde(name, data):
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data, fill=True)
    plt.title(f'KDE Plot for {name}')
    plt.xlabel(name)
    plt.ylabel('Density')
    plt.show()

def detect_anomalies_percentile(name, data, lower_percentile=5, upper_percentile=95):
    lower_bound = np.percentile(data, lower_percentile)
    upper_bound = np.percentile(data, upper_percentile)
    anomalies = np.where((data < lower_bound) | (data > upper_bound))
    print(f"\nAnomalies in {name}:")
    for index in anomalies[0]:
        print(f"  Index: {index}, Value: {data[index]}")
    return anomalies[0]

def calculate_change(data):
    return np.diff(data, prepend=data[0])

def plot_data_with_anomalies(name, data, anomalies):
    percentile_90 = np.percentile(data, 90)
    percentile_95 = np.percentile(data, 95)
    percentile_99 = np.percentile(data, 99)
    percentile_1 = np.percentile(data, 1)
    percentile_5 = np.percentile(data, 5)

    plt.figure(figsize=(10, 6))
    plt.plot(data, label='Data')
    plt.scatter(anomalies, data[anomalies], color='red', label='Anomalies')
    plt.axhline(percentile_90, color='purple', linestyle='--', label='90th Percentile')
    plt.axhline(percentile_95, color='orange', linestyle='--', label='95th Percentile')
    plt.axhline(percentile_99, label='99th percentile', linestyle='--')
    plt.axhline(percentile_1, color='purple', linestyle='--', label='1st Percentile')
    plt.axhline(percentile_5, color='orange', linestyle='--', label='5th Percentile')
    plt.title(f'{name} with Anomalies')
    plt.xlabel('Index')
    plt.ylabel(name)
    plt.legend()
    plt.show()

print_statistics("Memory Usage (%)", mem_usage)
plot_kde("Memory Usage (%)", mem_usage)
mem_anomalies = detect_anomalies_percentile("Memory Usage (%)", mem_usage)
plot_data_with_anomalies("Memory Usage (%)", mem_usage, mem_anomalies)

print_statistics("Disk Read Bytes", disk_read_bytes)
plot_kde("Disk Read Bytes", disk_read_bytes)
disk_read_anomalies = detect_anomalies_percentile("Disk Read Bytes", disk_read_bytes)
plot_data_with_anomalies("Disk Read Bytes", disk_read_bytes, disk_read_anomalies)

disk_write_changes = calculate_change(disk_write_bytes)
print_statistics("Disk Write Bytes Change", disk_write_changes)
plot_kde("Disk Write Bytes Change", disk_write_changes)
disk_write_anomalies = detect_anomalies_percentile("Disk Write Bytes Change", disk_write_changes)
plot_data_with_anomalies("Disk Write Bytes Change", disk_write_changes, disk_write_anomalies)

net_bytes_sent_changes = calculate_change(net_bytes_sent)
print_statistics("Network Bytes Sent Change", net_bytes_sent_changes)
plot_kde("Network Bytes Sent Change", net_bytes_sent_changes)
net_sent_anomalies = detect_anomalies_percentile("Network Bytes Sent Change", net_bytes_sent_changes)
plot_data_with_anomalies("Network Bytes Sent Change", net_bytes_sent_changes, net_sent_anomalies)

net_bytes_recv_changes = calculate_change(net_bytes_recv)
print_statistics("Network Bytes Received Change", net_bytes_recv_changes)
plot_kde("Network Bytes Received Change", net_bytes_recv_changes)
net_recv_anomalies = detect_anomalies_percentile("Network Bytes Received Change", net_bytes_recv_changes)
plot_data_with_anomalies("Network Bytes Received Change", net_bytes_recv_changes, net_recv_anomalies)
