import streamlit as st
import pandas as pd
import os

# -----------------------------
# Load data safely (absolute path)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "bioprocess_data.csv")

st.set_page_config(page_title="Smart Bioprocess Monitoring", layout="wide")

st.title("🧪 Smart Bioprocess Monitoring Dashboard")

# Check if CSV exists
if not os.path.exists(DATA_PATH):
    st.error("❌ bioprocess_data.csv not found.")
    st.info("Run data_generator.py first to generate sensor data.")
    st.stop()

# Load data
df = pd.read_csv(DATA_PATH)

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header("Controls")

parameter = st.sidebar.selectbox(
    "Select Parameter",
    ["temperature", "pH", "oxygen", "glucose"]
)

# Thresholds (industrial-style limits)
THRESHOLDS = {
    "temperature": (36.0, 38.0),
    "pH": (6.8, 7.5),
    "oxygen": (30.0, 50.0),
    "glucose": (4.0, 6.0)
}

low, high = THRESHOLDS[parameter]

# -----------------------------
# Main chart
# -----------------------------
st.subheader(f"{parameter.upper()} Trend")

st.line_chart(df[parameter])

# -----------------------------
# Alerts section
# -----------------------------
alerts = df[(df[parameter] < low) | (df[parameter] > high)]

st.subheader("⚠️ Alerts")

if alerts.empty:
    st.success("No anomalies detected. Process is stable.")
else:
    st.warning(f"{len(alerts)} alert(s) detected.")
    st.dataframe(alerts.tail(10))

# -----------------------------
# Plant health status
# -----------------------------
st.subheader("🏭 Plant Status")

if len(alerts) > 20:
    st.error("CRITICAL – Immediate attention required")
elif len(alerts) > 5:
    st.warning("WARNING – Process deviations observed")
else:
    st.success("STABLE – Process within limits")

# -----------------------------
# Footer
# -----------------------------
st.caption("Simulated bioprocess data | Digital Twin Monitoring System")
