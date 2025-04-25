import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random

st.set_page_config(page_title="Network Traffic Demo", layout="wide")

@st.cache_data
def load_data():
    real = pd.read_csv("real.csv")
    ctgan = pd.read_csv("ctgan_synthetic.csv")
    tablegan = pd.read_csv("tablegan_synthetic.csv")
    custom = pd.read_csv("custom_synthetic.csv")
    return real, ctgan, tablegan, custom

real, ctgan, tablegan, custom = load_data()
models = {"Real": real, "CTGAN": ctgan, "TableGAN": tablegan, "Custom": custom}

st.title("📶 Real vs Synthetic Network Traffic Simulator")

# -------------------
# 1. Packet Flow Animation (Time Slider)
# -------------------
st.header("📈 Packet Flow Over Time")

selected_model = st.selectbox("Choose a dataset", list(models.keys()))
df = models[selected_model]

if "timestamp" not in df.columns:
    st.warning("No timestamp column found. Skipping animated view.")
else:
    df = df.sort_values(by="timestamp").reset_index(drop=True)
    time_range = st.slider("Select time index", 0, len(df)-1, 50, 1)
    flow_cols = ["sbytes", "dbytes", "rate"]

    fig, ax = plt.subplots(figsize=(10, 4))
    df.iloc[:time_range][flow_cols].plot(ax=ax)
    ax.set_title(f"{selected_model} - Flow Metrics Over Time")
    ax.set_xlabel("Packets")
    ax.set_ylabel("Metric Value")
    st.pyplot(fig)

# -------------------
# 2. Spot the Difference Game
# -------------------
st.header("🕵️ Spot the Difference: Real vs Synthetic")

random_model = random.choice(["Real", "CTGAN", "TableGAN", "Custom"])
random_row = models[random_model].sample(1).reset_index(drop=True)

st.dataframe(random_row)

guess = st.radio("Is this Real or Synthetic?", ["Real", "Synthetic"])
if st.button("Reveal Answer"):
    if guess == "Real" and random_model == "Real":
        st.success("✅ Correct! It was Real.")
    elif guess == "Synthetic" and random_model != "Real":
        st.success(f"✅ Correct! It was {random_model}.")
    else:
        st.error(f"❌ Oops! It was actually {random_model}.")

# -------------------
# 3. Protocol Distribution Comparison
# -------------------
if 'proto' in real.columns:
    st.header("📡 Protocol Distribution")

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    real['proto'].value_counts().plot(kind='bar', alpha=0.5, label='Real', ax=ax2)
    ctgan['proto'].value_counts().plot(kind='bar', alpha=0.5, label='CTGAN', ax=ax2)
    tablegan['proto'].value_counts().plot(kind='bar', alpha=0.5, label='TableGAN', ax=ax2)
    custom['proto'].value_counts().plot(kind='bar', alpha=0.5, label='Custom', ax=ax2)

    ax2.legend()
    ax2.set_title("Protocol Frequency in Real vs Synthetic Data")
    st.pyplot(fig2)

# -------------------
# 4. Mean Metric Comparison
# -------------------
st.header("📋 Feature Averages (Real vs Synthetic)")
features = ['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 'sload', 'dload']
selected_metrics = st.multiselect("Select features", features, default=features[:4])
compare_df = pd.DataFrame({
    'Real': real[selected_metrics].mean(),
    'CTGAN': ctgan[selected_metrics].mean(),
    'TableGAN': tablegan[selected_metrics].mean(),
    'Custom': custom[selected_metrics].mean()
}).T.round(2)
st.dataframe(compare_df)
