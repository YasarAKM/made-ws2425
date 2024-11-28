import pandas as pd
import sqlite3
import requests
import geopandas as gpd
import json
import os

# Create Database & Connection
DB_FILE = 'obesity_analysis.db'
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)  # Remove if already exists for fresh start
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Step 1: Define URLs
data_url1 = "https://data.cdc.gov/api/views/hn4x-zwk7/rows.csv?accessType=DOWNLOAD"
data_url2 = "https://services3.arcgis.com/HESxeTbDliKKvec2/arcgis/rest/services/LakeCounty_Health/FeatureServer/8/query?outFields=*&where=1%3D1&f=geojson"

# Step 2: Fetch and Load Dataset 1 (CSV)
print("Fetching Dataset 1...")
response1 = requests.get(data_url1)
csv_file = 'nutrition_physical_activity.csv'
with open(csv_file, 'wb') as file:
    file.write(response1.content)

# Load CSV into Pandas DataFrame
df1 = pd.read_csv(csv_file)
df1.to_sql('nutrition_physical_activity', conn, if_exists='replace', index=False)

# Step 3: Fetch and Load Dataset 2 (GeoJSON)
print("Fetching Dataset 2...")
response2 = requests.get(data_url2)
geojson_file = 'obesity_geo_data.geojson'
with open(geojson_file, 'wb') as file:
    file.write(response2.content)

# Convert GeoJSON to Pandas DataFrame
with open(geojson_file, 'r') as file:
    geo_data = json.load(file)

gdf = gpd.GeoDataFrame.from_features(geo_data["features"])
df2 = pd.DataFrame(gdf.drop(columns='geometry'))  # Drop geometry for tabular format
df2.to_sql('obesity_geo_data', conn, if_exists='replace', index=False)

# Step 4: Data Transformation
print("Transforming Data...")
# Normalize column names for merging
df1.columns = df1.columns.str.lower().str.replace(" ", "_")
df2.columns = df2.columns.str.lower().str.replace(" ", "_")

# Ensure state names match format between datasets
df1['state'] = df1['locationdesc'].str.upper()
df2['state'] = df2['state_name'].str.upper()

# Merge Datasets
merged_df = pd.merge(df1, df2, on='state', how='inner')
merged_df.to_sql('merged_data', conn, if_exists='replace', index=False)

# Step 5: Example Analysis
print("Performing Example Analysis...")
cursor.execute("SELECT state, obesity_rate, income, education FROM merged_data LIMIT 10;")
example_data = cursor.fetchall()
print("Sample Data:", example_data)

# Step 6: Save Cleaned Data for Power BI
output_file = 'cleaned_data.csv'
merged_df.to_csv(output_file, index=False)
print(f"Cleaned data saved to {output_file}")

# Cleanup and Close
conn.close()
print("Pipeline Completed!")