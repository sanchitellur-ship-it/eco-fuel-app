import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Page setup
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

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Charts", "Statistics", "GitHub"])

# --- Overview Tab ---
with tab1:
    st.markdown("### Welcome to the Eco Fuel Dashboard")
    st.info("Track your fuel usage, costs, and efficiency with interactive charts.")

# --- Charts Tab ---
with tab2:
    try:
        df = pd.read_csv("fuel_data.csv")
        st.success("✅ Data loaded successfully!")

        col1, col2 = st.columns(2)

        # Fuel consumption plot
        with col1:
            st.markdown("### ⛽ Fuel Consumption Over Time")
            fig, ax = plt.subplots(figsize=(6,4))
            sns.lineplot(data=df, x="Date", y="Fuel_Consumption", ax=ax, color="#1ABC9C", linewidth=2.5)
            ax.set_title("Fuel Consumption Trend

