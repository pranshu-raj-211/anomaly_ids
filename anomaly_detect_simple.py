import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the log file into a NumPy array
data = np.genfromtxt('usage.log', delimiter=',', skip_header=1, dtype=float, usecols=(1, 2, 3, 4, 5, 6))

# Separate the columns
cpu_usage = data[:, 0]
mem_usage = data[:, 1]
disk_read_bytes = data[:, 2]
disk_write_bytes = data[:, 3]
net_bytes_sent = data[:, 4]
net_bytes_recv = data[:, 5]

# Function to print statistics
def print_statistics(name, data):
    print(f"\n{name}:")
    print(f"  Mean: {np.mean(data)}")
    print(f"  Max: {np.max(data)}")
    print(f"  Min: {np.min(data)}")
    print(f"  Variance: {np.var(data)}")
    print(f"  Standard Deviation: {np.std(data)}")

# Function to plot KDE
def plot_kde(name, data):
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data, fill=True)
    plt.title(f'KDE Plot for {name}')
    plt.xlabel(name)
    plt.ylabel('Density')
    plt.savefig(f'{name}_kde.png')
    plt.show()

# Function to detect anomalies using Z-score
def detect_anomalies(name, data, threshold=3):
    mean = np.mean(data)
    std_dev = np.std(data)
    z_scores = (data - mean) / std_dev
    anomalies = np.where(np.abs(z_scores) > threshold)
    print(f"\nAnomalies in {name}:")
    for index in anomalies[0]:
        print(f"  Index: {index}, Value: {data[index]}, Z-score: {z_scores[index]}")
    return anomalies[0]

# Function to plot data with anomalies
def plot_data_with_anomalies(name, data, anomalies):
    plt.figure(figsize=(10, 6))
    plt.plot(data, label='Data')
    plt.scatter(anomalies, data[anomalies], color='red', label='Anomalies')
    plt.title(f'{name} with Anomalies')
    plt.xlabel('Index')
    plt.ylabel(name)
    plt.legend()
    plt.show()

# Print statistics, plot KDE, detect anomalies, and plot data with anomalies for each metric
print_statistics("CPU Usage (%)", cpu_usage)
plot_kde("CPU Usage (%)", cpu_usage)
cpu_anomalies = detect_anomalies("CPU Usage (%)", cpu_usage)
plot_data_with_anomalies("CPU Usage (%)", cpu_usage, cpu_anomalies)

print_statistics("Memory Usage (%)", mem_usage)
plot_kde("Memory Usage (%)", mem_usage)
mem_anomalies = detect_anomalies("Memory Usage (%)", mem_usage)
plot_data_with_anomalies("Memory Usage (%)", mem_usage, mem_anomalies)

print_statistics("Disk Read Bytes", disk_read_bytes)
plot_kde("Disk Read Bytes", disk_read_bytes)
disk_read_anomalies = detect_anomalies("Disk Read Bytes", disk_read_bytes)
plot_data_with_anomalies("Disk Read Bytes", disk_read_bytes, disk_read_anomalies)

print_statistics("Disk Write Bytes", disk_write_bytes)
plot_kde("Disk Write Bytes", disk_write_bytes)
disk_write_anomalies = detect_anomalies("Disk Write Bytes", disk_write_bytes)
plot_data_with_anomalies("Disk Write Bytes", disk_write_bytes, disk_write_anomalies)

print_statistics("Network Bytes Sent", net_bytes_sent)
plot_kde("Network Bytes Sent", net_bytes_sent)
net_sent_anomalies = detect_anomalies("Network Bytes Sent", net_bytes_sent)
plot_data_with_anomalies("Network Bytes Sent", net_bytes_sent, net_sent_anomalies)

print_statistics("Network Bytes Received", net_bytes_recv)
plot_kde("Network Bytes Received", net_bytes_recv)
net_recv_anomalies = detect_anomalies("Network Bytes Received", net_bytes_recv)
plot_data_with_anomalies("Network Bytes Received", net_bytes_recv, net_recv_anomalies)