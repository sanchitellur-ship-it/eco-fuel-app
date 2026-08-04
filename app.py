import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page config
st.set_page_config(page_title="Eco Fuel Dashboard", page_icon="⛽", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    h1 {
        color: #2E86C1;
        text-align: center;
    }
    .stDataFrame {
        border: 2px solid #2E86C1;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🚗 Eco Fuel Dashboard")
st.markdown("### Track your fuel usage, costs, and efficiency with beautiful charts.")

# Load dataset
try:
    df = pd.read_csv("fuel_data.csv")
    st.success("✅ Data loaded successfully!")
    st.write("### Dataset Preview")
    st.dataframe(df.head())
except FileNotFoundError:
    st.error("❌ fuel_data.csv not found. Please upload it to the repo.")

# If dataset loaded, show stats and plots
if 'df' in locals():
    # Summary stats
    st.markdown("### 📊 Summary Statistics")
    st.write(df.describe())

    # Layout with columns
    col1, col2 = st.columns(2)

    # Fuel consumption plot
    with col1:
        st.markdown("### ⛽ Fuel Consumption Over Time")
        fig, ax = plt.subplots(figsize=(6,4))
        import matplotlib.dates as mdates

# Fuel consumption plot
fig, ax = plt.subplots(figsize=(6,4))
sns.lineplot(data=df, x="Date", y="Fuel_Consumption", ax=ax, color="#1ABC9C", linewidth=2.5)
ax.set_title("Fuel Consumption Trend", fontsize=14, color="#1ABC9C")

# Format x-axis dates
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))  # e.g. Aug 01
plt.xticks(rotation=45)

st.pyplot(fig)

# Fuel cost plot
fig2, ax2 = plt.subplots(figsize=(6,4))
sns.lineplot(data=df, x="Date", y="Cost", ax=ax2, color="#E74C3C", linewidth=2.5)
ax2.set_title("Fuel Cost Trend", fontsize=14, color="#E74C3C")

# Format x-axis dates
ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
plt.xticks(rotation=45)

st.pyplot(fig2)


    # Fuel cost plot
    with col2:
        st.markdown("### 💰 Fuel Cost Over Time")
        fig2, ax2 = plt.subplots(figsize=(6,4))
        sns.lineplot(data=df, x="Date", y="Cost", ax=ax2, color="#E74C3C", linewidth=2.5)
        ax2.set_title("Fuel Cost Trend", fontsize=14, color="#E74C3C")
        st.pyplot(fig2)

    # Scatter plot
    st.markdown("### 🚘 Distance vs Fuel Consumption")
    fig3, ax3 = plt.subplots(figsize=(8,5))
    sns.scatterplot(data=df, x="Distance", y="Fuel_Consumption", ax=ax3, color="#9B59B6", s=80)
    ax3.set_title("Distance vs Fuel Consumption", fontsize=14, color="#9B59B6")
    st.pyplot(fig3)

