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
            ax.set_title("Fuel Consumption Trend", fontsize=14, color="#1ABC9C")

            # Format x-axis dates
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
            plt.xticks(rotation=45)

            st.pyplot(fig)

        # Fuel cost plot
        with col2:
            st.markdown("### 💰 Fuel Cost Over Time")
            fig2, ax2 = plt.subplots(figsize=(6,4))
            sns.lineplot(data=df, x="Date", y="Cost", ax=ax2, color="#E74C3C", linewidth=2.5)
            ax2.set_title("Fuel Cost Trend", fontsize=14, color="#E74C3C")

            # Format x-axis dates
            ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
            ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
            plt.xticks(rotation=45)

            st.pyplot(fig2)

        # Scatter plot
        st.markdown("### 🚘 Distance vs Fuel Consumption")
        fig3, ax3 = plt.subplots(figsize=(8,5))
        sns.scatterplot(data=df, x="Distance", y="Fuel_Consumption", ax=ax3, color="#9B59B6", s=80)
        ax3.set_title("Distance vs Fuel Consumption", fontsize=14, color="#9B59B6")
        st.pyplot(fig3)

    except FileNotFoundError:
        st.error("❌ fuel_data.csv not found. Please upload it to the repo.")

# --- Statistics Tab ---
with tab3:
    try:
        df = pd.read_csv("fuel_data.csv")
        st.markdown("### 📊 Summary Statistics")

        # Calculate key stats
        avg_fuel = df['Fuel_Consumption'].mean()
        avg_cost = df['Cost'].mean()
        max_distance = df['Distance'].max()
        min_distance = df['Distance'].min()
        std_fuel = df['Fuel_Consumption'].std()

        # Show metrics in cards
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Avg Fuel Consumption", f"{avg_fuel:.2f} L")
        col2.metric("Avg Cost", f"₹{avg_cost:.0f}")
        col3.metric("Max Distance", f"{max_distance:.0f} km")
        col4.metric("Min Distance", f"{min_distance:.0f} km")
        col5.metric("Fuel Std Dev", f"{std_fuel:.2f}")

        # Show full stats table with styling
        st.markdown("### 📑 Detailed Table")
        stats = df.describe().round(2)
        st.dataframe(stats.style.background_gradient(cmap="Blues"))

    except FileNotFoundError:
        st.error("❌ fuel_data.csv not found. Please upload it to the repo.")

# --- GitHub Tab ---
with tab4:
    st.markdown("### 🔗 GitHub Repository")
    st.write("View the source code and contribute here:")
    st.markdown("[Eco Fuel App Repository](https://github.com/sanchitellur-ship-it/eco-fuel-app)")

