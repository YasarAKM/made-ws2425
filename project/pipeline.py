import pandas as pd
import requests
from shapely.geometry import shape

# URLs for datasets
BRFSS_URL = "https://data.cdc.gov/api/views/hn4x-zwk7/rows.csv?accessType=DOWNLOAD"
GEOJSON_URL = "https://services3.arcgis.com/HESxeTbDliKKvec2/arcgis/rest/services/LakeCounty_Health/FeatureServer/8/query?outFields=*&where=1%3D1&f=geojson"

def fetch_brfss_data(url):
    """Fetch BRFSS dataset from the given URL."""
    print("Fetching BRFSS dataset...")
    try:
        data = pd.read_csv(url)
        print(f"BRFSS dataset loaded successfully with {data.shape[0]} rows and {data.shape[1]} columns.")
        return data
    except Exception as e:
        print(f"Failed to fetch BRFSS dataset: {e}")
        exit()

def fetch_geojson_data(url):
    """Fetch GeoJSON dataset from the given URL."""
    print("Fetching GeoJSON dataset...")
    try:
        data = requests.get(url).json()
        print("GeoJSON dataset loaded successfully.")
        return data
    except Exception as e:
        print(f"Failed to fetch GeoJSON dataset: {e}")
        exit()

def clean_geojson_data(geojson_data):
    """Normalize and clean GeoJSON data."""
    print("Cleaning GeoJSON data...")
    geo_data = pd.json_normalize(geojson_data["features"])
    geo_data = geo_data.rename(columns={"properties.NAME": "State", "properties.Obesity": "obesity_rate"})
    print("Parsing GeoJSON geometries...")
    geo_data['geometry'] = geojson_data["features"]
    geo_data['geometry'] = geo_data['geometry'].apply(
        lambda feature: shape(feature['geometry']) if isinstance(feature['geometry'], dict) else None
    )
    geo_data = geo_data[['State', 'obesity_rate', 'geometry']]
    print(f"GeoJSON dataset processed with {geo_data.shape[0]} rows.")
    return geo_data

def clean_brfss_data(brfss_data):
    """Clean and prepare BRFSS dataset."""
    print("Cleaning BRFSS dataset...")
    data_cleaned = brfss_data[['YearStart', 'LocationDesc', 'Data_Value']]
    data_cleaned.columns = ['Year', 'State', 'Obesity_Rate']
    data_cleaned['State'] = data_cleaned['State'].str.strip().str.upper()
    print(f"BRFSS dataset cleaned with {data_cleaned.shape[0]} rows.")
    return data_cleaned

def merge_datasets(geo_data, brfss_data):
    """Merge GeoJSON and BRFSS datasets."""
    print("Merging datasets...")
    latest_year = brfss_data['Year'].max()
    brfss_latest = brfss_data[brfss_data['Year'] == latest_year]
    merged_data = geo_data.merge(brfss_latest, on='State', how='inner')
    print(f"Merged dataset contains {merged_data.shape[0]} rows.")
    return merged_data

def save_data(data, filename):
    """Save dataset to a CSV file."""
    print(f"Saving data to {filename}...")
    data.to_csv(filename, index=False)
    print(f"Data saved successfully as {filename}.")

def main_pipeline():
    """Main pipeline function to fetch, process, and save datasets."""
    # Fetch datasets
    brfss_data = fetch_brfss_data(BRFSS_URL)
    geojson_data = fetch_geojson_data(GEOJSON_URL)
    
    # Clean datasets
    geo_data = clean_geojson_data(geojson_data)
    brfss_data_cleaned = clean_brfss_data(brfss_data)
    
    # Save cleaned GeoJSON data
    save_data(geo_data, "geo_data_cleaned.csv")
    
    # Merge datasets
    merged_data = merge_datasets(geo_data, brfss_data_cleaned)
    
    # Save merged data
    save_data(merged_data, "merged_data.csv")

# Run the pipeline
if __name__ == "__main__":
    main_pipeline()