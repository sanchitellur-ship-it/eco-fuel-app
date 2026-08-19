import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load raw dataset
df = pd.read_csv("raw_data.csv")

# Step 1: Handle missing data
df['speed'] = df.groupby('route')['speed'].transform(lambda x: x.fillna(x.median()))
df['fuel'] = df['fuel'].fillna(df['fuel'].mean())

# Step 2: Outlier filtering
df = df[(df['speed'] >= 0) & (df['speed'] <= 120)]
df = df[df['fuel'] >= 0]

# Step 3: Fairness normalization
def categorize_idling(row):
    if row['Traffic_Congestion_Index'] == 'HIGH' and row['Vehicle_Speed'] == 0:
        return 'Unavoidable Traffic Idling'
    elif row['Traffic_Congestion_Index'] == 'LOW' and row['Vehicle_Speed'] == 0:
        return 'Avoidable Driver Idling'
    else:
        return 'Normal Driving'

df['Idling_Category'] = df.apply(categorize_idling, axis=1)

# --- NEW Step 4: Eco-Driver Index Features ---
# Fuel efficiency (km/L)
df['Mileage_km_per_l'] = df['distance'] / df['fuel']

# Carbon intensity (g/km) using emission factors
emission_factors = {"Diesel":2640, "CNG":2030, "Petrol":2392}
df['Emission_Factor'] = df['fuel_type'].map(emission_factors).fillna(2640)
df['Carbon_Intensity_g_per_km'] = (df['fuel'] * df['Emission_Factor']) / df['distance']

# Composite Eco-Score (0–100 normalization of mileage, idling, speed variance)
features = df[['Mileage_km_per_l','idling_time','speed']].fillna(0).values
scaler = MinMaxScaler(feature_range=(0,100))
scaled = scaler.fit_transform(features)
df['Composite_Eco_Score'] = scaled.mean(axis=1)

# Export cleaned dataset
df.to_csv("cleaned_data.csv", index=False)
