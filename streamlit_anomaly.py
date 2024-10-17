import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import PowerTransformer


@st.cache_data
def load_data():
    data = np.genfromtxt(
        "usage.log",
        delimiter=",",
        skip_header=1,
        dtype=float,
        usecols=(1, 2, 3, 4, 5, 6),
    )
    return pd.DataFrame(
        data,
        columns=[
            "timestamp",
            "mem_usage",
            "disk_read_bytes",
            "disk_write_bytes",
            "net_bytes_sent",
            "net_bytes_recv",
        ],
    )


data = load_data()


def calculate_change(data):
    return np.diff(data, prepend=data.iloc[0])


def transform_visual(data):
    series_reshaped = data.values.reshape(-1, 1)  # Convert Series to 2D array
    power_transformer = PowerTransformer(method='yeo-johnson')
    transformed_data = power_transformer.fit_transform(series_reshaped)
    return pd.Series(transformed_data.flatten(), index=data.index)


data["disk_write_bytes_change"] = calculate_change(data["disk_write_bytes"])
data["net_bytes_sent_change"] = calculate_change(data["net_bytes_sent"])
data["net_bytes_recv_change"] = calculate_change(data["net_bytes_recv"])

#data["disk_write_bytes_change"] = transform_visual(data["disk_write_bytes_change"])
data["net_bytes_sent_change"] = transform_visual(data["net_bytes_sent_change"])
#data["net_bytes_recv_change"] = transform_visual(data["net_bytes_recv_change"])


def detect_anomalies(data, lower_percentile, upper_percentile):
    lower_bound = np.percentile(data, lower_percentile)
    upper_bound = np.percentile(data, upper_percentile)
    return np.where((data < lower_bound) | (data > upper_bound))[0]


def plot_data_with_anomalies(data, anomalies, name):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data, label="Data")
    ax.scatter(anomalies, data.iloc[anomalies], color="red", label="Anomalies")
    ax.axhline(
        np.percentile(data, 90), color="purple", linestyle="--", label="90th Percentile"
    )
    ax.axhline(
        np.percentile(data, 95), color="orange", linestyle="--", label="95th Percentile"
    )
    ax.axhline(
        np.percentile(data, 10), color="purple", linestyle="--", label="10th Percentile"
    )
    ax.axhline(
        np.percentile(data, 5), color="orange", linestyle="--", label="5th Percentile"
    )
    ax.set_title(f"{name} with Anomalies")
    ax.set_xlabel("Index")
    ax.set_ylabel(name)
    ax.legend()
    return fig


st.title("Time Series Anomaly Detection")

st.sidebar.header("Settings")
metric = st.sidebar.selectbox(
    "Select metric to analyze",
    (
        "Memory Usage (%)",
        "Disk Read Bytes",
        "Disk Write Bytes Change",
        "Network Bytes Sent Change",
        "Network Bytes Received Change",
    ),
)

lower_percentile = st.sidebar.slider("Lower percentile threshold", 1, 10, 5)
upper_percentile = st.sidebar.slider("Upper percentile threshold", 90, 99, 95)

# Map metric names to DataFrame columns
metric_to_column = {
    "Memory Usage (%)": "mem_usage",
    "Disk Read Bytes": "disk_read_bytes",
    "Disk Write Bytes Change": "disk_write_bytes_change",
    "Network Bytes Sent Change": "net_bytes_sent_change",
    "Network Bytes Received Change": "net_bytes_recv_change",
}

selected_data = data[metric_to_column[metric]]

anomalies = detect_anomalies(selected_data, lower_percentile, upper_percentile)

st.header(f"Statistics for {metric}")
st.write(f"Mean: {selected_data.mean():.2f}")
st.write(f"Max: {selected_data.max():.2f}")
st.write(f"Min: {selected_data.min():.2f}")
st.write(f"Variance: {selected_data.var():.2f}")
st.write(f"Standard Deviation: {selected_data.std():.2f}")
st.write(f"90th Percentile: {np.percentile(selected_data, 90):.2f}")
st.write(f"95th Percentile: {np.percentile(selected_data, 95):.2f}")

st.header(f"KDE Plot for {metric}")
fig_kde, ax_kde = plt.subplots(figsize=(10, 6))
sns.kdeplot(selected_data, fill=True, ax=ax_kde)
ax_kde.set_title(f"KDE Plot for {metric}")
ax_kde.set_xlabel(metric)
ax_kde.set_ylabel("Density")
st.pyplot(fig_kde)

st.header(f"{metric} with Anomalies")
fig_anomalies = plot_data_with_anomalies(selected_data, anomalies, metric)
st.pyplot(fig_anomalies)

st.header("Detected Anomalies")
if len(anomalies) > 0:
    anomaly_df = pd.DataFrame(
        {"Index": anomalies, "Value": selected_data.iloc[anomalies]}
    )
    st.write(anomaly_df)
else:
    st.write("No anomalies detected with the current settings.")
