import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import csv

st.set_page_config(layout="wide")

# --- File path (use script directory so relative paths work when running Streamlit) ---
BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "driver_performance.csv")
repaired_path = os.path.join(BASE_DIR, "driver_performance_repaired.csv")

def robust_read_csv(path):
    # Try normal read
    try:
        return pd.read_csv(path)
    except Exception as e:
        st.warning(f"Standard read_csv failed: {e}")
    # Try reading with QUOTE_ALL
    try:
        return pd.read_csv(path, quoting=csv.QUOTE_ALL)
    except Exception:
        pass
    # Try engine='python' and skip bad lines (warn)
    try:
        return pd.read_csv(path, engine="python", on_bad_lines="warn")
    except Exception:
        pass
    # Last resort: use csv.reader to parse and rebuild DataFrame
    rows = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f, quotechar='"', delimiter=',', escapechar='\\')
        for r in reader:
            rows.append(r)
    if not rows:
        raise RuntimeError("Could not parse CSV file at all.")
    header = [h.strip() for h in rows[0]]
    data = rows[1:]
    # Pad/truncate rows to header length
    normalized = [row + [""]*(len(header)-len(row)) if len(row) < len(header) else row[:len(header)] for row in data]
    df = pd.DataFrame(normalized, columns=header)
    return df

# Attempt to read; if fails, show instructions
if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    try:
        df = robust_read_csv(file_path)
        # Save a repaired copy for future runs
        try:
            df.to_csv(repaired_path, index=False, quoting=csv.QUOTE_ALL, encoding="utf-8")
        except Exception:
            pass
    except Exception as e:
        st.error("Failed to read driver_performance.csv: " + str(e))
        st.info("Run the repair script or fix quoting in the CSV and try again.")
        st.stop()
else:
    st.error("driver_performance.csv not found or empty. Please submit data in the Flask app first.")
    st.stop()

st.title("Driver Performance Dashboard")
st.write("Visual summary of emissions, mileage, idling time, and recommendations")

# Ensure numeric columns are numeric
numeric_cols = ["Mileage_km_per_l", "Carbon_Intensity_g_per_km", "Idling_Time_Mins", "Avg_Speed_kmh", "Composite_Eco_Score"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# --- Emissions by Fuel Type ---
st.subheader("Emissions by Fuel Type (g CO2e per km)")
if "Fuel_Type" in df.columns and "Carbon_Intensity_g_per_km" in df.columns:
    fig, ax = plt.subplots(figsize=(8,4))
    sns.barplot(x="Fuel_Type", y="Carbon_Intensity_g_per_km", data=df, ax=ax, ci=None)
    ax.set_ylabel("g CO2e per km")
    st.pyplot(fig)
else:
    st.info("Required columns for emissions chart not found.")

# --- Driver Performance Heatmap ---
st.subheader("Driver Mileage Heatmap (km per L)")
if "Driver_ID" in df.columns and "Route_ID" in df.columns and "Mileage_km_per_l" in df.columns:
    pivot = df.pivot_table(values="Mileage_km_per_l", index="Driver_ID", columns="Route_ID", aggfunc="mean")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(pivot, cmap="coolwarm", annot=True, fmt=".1f", ax=ax)
    st.pyplot(fig)
else:
    st.info("Required columns for heatmap not found.")

# --- Training Recommendations ---
st.subheader("Training Recommendations")

def recommend_tips(row):
    tips = []
    if pd.notna(row.get("Idling_Time_Mins")) and float(row["Idling_Time_Mins"]) > 30:
        tips.append("Reduce idling to save fuel")
    if pd.notna(row.get("Mileage_km_per_l")) and float(row["Mileage_km_per_l"]) < 12:
        tips.append("Maintain steady speeds for better mileage")
    return "; ".join(tips) if tips else "No specific recommendations"

df["Recommendations"] = df.apply(recommend_tips, axis=1)

display_cols = [c for c in ["Driver_ID", "Route_ID", "Mileage_km_per_l", "Idling_Time_Mins", "Carbon_Intensity_g_per_km", "Composite_Eco_Score", "Recommendations"] if c in df.columns]
st.dataframe(df[display_cols].sort_values(by=["Composite_Eco_Score"], ascending=False).reset_index(drop=True))

# --- Quick filters and summary ---
st.sidebar.header("Filters")
fuel_filter = st.sidebar.multiselect("Fuel Type", options=sorted(df["Fuel_Type"].dropna().unique()) if "Fuel_Type" in df.columns else [], default=None)
driver_filter = st.sidebar.text_input("Driver ID (partial)")

df_filtered = df.copy()
if fuel_filter:
    df_filtered = df_filtered[df_filtered["Fuel_Type"].isin(fuel_filter)]
if driver_filter:
    df_filtered = df_filtered[df_filtered["Driver_ID"].astype(str).str.contains(driver_filter, case=False, na=False)]

st.sidebar.markdown("**Summary (filtered)**")
if not df_filtered.empty:
    st.sidebar.metric("Average Mileage (km/L)", f"{df_filtered['Mileage_km_per_l'].mean():.2f}")
    st.sidebar.metric("Average Emissions (g/km)", f"{df_filtered['Carbon_Intensity_g_per_km'].mean():.1f}")
    st.sidebar.metric("Avg Idling (mins)", f"{df_filtered['Idling_Time_Mins'].mean():.1f}")
else:
    st.sidebar.write("No data for selected filters.")

