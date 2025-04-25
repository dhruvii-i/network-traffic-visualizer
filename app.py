import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Network Traffic Comparison", layout="wide")

@st.cache_data
def load_data():
    real = pd.read_csv("real.csv")
    ctgan = pd.read_csv("ctgan_synthetic.csv")
    tablegan = pd.read_csv("tablegan_synthetic.csv")
    custom = pd.read_csv("custom_synthetic.csv")
    return real, ctgan, tablegan, custom

real, ctgan, tablegan, custom = load_data()

st.title("🔍 Real vs Synthetic Network Traffic Dashboard")

# Feature comparison
st.header("📊 Feature Distribution Comparison")
features = ['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 'sload', 'dload']
selected_feature = st.selectbox("Select a feature", features)

fig, ax = plt.subplots(figsize=(12, 5))
sns.kdeplot(real[selected_feature], label="Real", fill=True)
sns.kdeplot(ctgan[selected_feature], label="CTGAN", fill=False)
sns.kdeplot(tablegan[selected_feature], label="TableGAN", fill=False)
sns.kdeplot(custom[selected_feature], label="Custom Model", fill=False)
plt.legend()
st.pyplot(fig)

# Spot the difference
st.header("🕵️ Spot the Difference")
sample = st.radio("Choose sample type", ["Real", "CTGAN", "TableGAN", "Custom Model"])
sample_size = st.slider("Number of rows", 5, 20, 10)

if sample == "Real":
    st.dataframe(real.sample(sample_size))
elif sample == "CTGAN":
    st.dataframe(ctgan.sample(sample_size))
elif sample == "TableGAN":
    st.dataframe(tablegan.sample(sample_size))
else:
    st.dataframe(custom.sample(sample_size))

# Mean metric comparison
st.header("📋 Feature Averages (Real vs Synthetic)")
selected_metrics = st.multiselect("Select features", features, default=features[:4])
compare_df = pd.DataFrame({
    'Real': real[selected_metrics].mean(),
    'CTGAN': ctgan[selected_metrics].mean(),
    'TableGAN': tablegan[selected_metrics].mean(),
    'Custom': custom[selected_metrics].mean()
}).T.round(2)
st.dataframe(compare_df)

# Optional: Anomaly Detection
st.header("🚨 Anomaly Detection Performance (Demo Results)")
st.table({
    "Model": ["CTGAN", "TableGAN", "Custom"],
    "Detection Rate (%)": [91.2, 87.8, 93.4],
    "False Positives (%)": [6.3, 7.1, 4.9]
})
