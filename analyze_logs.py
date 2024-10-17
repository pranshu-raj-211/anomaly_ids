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

def plot_kde(name, data):
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data, fill=True)
    plt.title(f'KDE Plot for {name}')
    plt.xlabel(name)
    plt.ylabel('Density')
    plt.show()


print_statistics("Memory Usage (%)", mem_usage)
plot_kde("Memory Usage (%)", mem_usage)

print_statistics("Disk Read Bytes", disk_read_bytes)
plot_kde("Disk Read Bytes", disk_read_bytes)

print_statistics("Disk Write Bytes", disk_write_bytes)
plot_kde("Disk Write Bytes", disk_write_bytes)

print_statistics("Network Bytes Sent", net_bytes_sent)
plot_kde("Network Bytes Sent", net_bytes_sent)

print_statistics("Network Bytes Received", net_bytes_recv)
plot_kde("Network Bytes Received", net_bytes_recv)