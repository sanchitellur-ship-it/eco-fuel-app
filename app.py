import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("🚗 Eco Fuel Dashboard")

try:
    df = pd.read_csv("fuel_data.csv")
    st.write("### Dataset Preview")
    st.dataframe(df.head())
except FileNotFoundError:
    st.error("fuel_data.csv not found. Please upload it to the repo.")

if 'df' in locals():
    st.write("### Summary Statistics")
    st.write(df.describe())

    st.write("### Fuel Consumption Over Time")
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x="Date", y="Fuel_Consumption", ax=ax)
    st.pyplot(fig)

    st.write("### Fuel Cost Over Time")
    fig2, ax2 = plt.subplots()
    sns.lineplot(data=df, x="Date", y="Cost", ax=ax2, color="red")
    st.pyplot(fig2)

    st.write("### Distance vs Fuel Consumption")
    fig3, ax3 = plt.subplots()
    sns.scatterplot(data=df, x="Distance", y="Fuel_Consumption", ax=ax3)
    st.pyplot(fig3)

