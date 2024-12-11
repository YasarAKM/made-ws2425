import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from shapely.geometry import Polygon
from pipeline import (
    fetch_brfss_data,
    fetch_geojson_data,
    clean_geojson_data,
    clean_brfss_data,
    merge_datasets,
)

class TestPipeline(unittest.TestCase):
    @patch("pipeline.requests.get")
    def test_fetch_geojson_data(self, mock_get):
        """Test fetching GeoJSON dataset."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "features": [
                {
                    "type": "Feature",
                    "properties": {"NAME": "TestState", "Obesity": 30.5},
                    "geometry": {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]},
                }
            ]
        }
        mock_get.return_value = mock_response

        geojson_data = fetch_geojson_data("mock_url")
        self.assertIn("features", geojson_data)
        self.assertEqual(len(geojson_data["features"]), 1)

    def test_clean_geojson_data(self):
        """Test cleaning GeoJSON data."""
        geojson_data = {
            "features": [
                {
                    "type": "Feature",
                    "properties": {"NAME": "TestState", "Obesity": 30.5},
                    "geometry": {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]},
                }
            ]
        }
        geo_data = clean_geojson_data(geojson_data)
        self.assertEqual(geo_data.shape[0], 1)
        self.assertEqual(geo_data.loc[0, "State"], "TestState")
        self.assertIsInstance(geo_data.loc[0, "geometry"], Polygon)

    def test_clean_brfss_data(self):
        """Test cleaning BRFSS data."""
        brfss_data = pd.DataFrame({
            "YearStart": [2023, 2023],
            "LocationDesc": ["TestState", "OtherState"],
            "Data_Value": [30.5, 25.2],
        })
        cleaned_data = clean_brfss_data(brfss_data)
        self.assertEqual(cleaned_data.shape[0], 2)
        self.assertEqual(cleaned_data.loc[0, "State"], "TESTSTATE")

    def test_merge_datasets(self):
        """Test merging GeoJSON and BRFSS datasets."""
        geo_data = pd.DataFrame({
            "State": ["TESTSTATE"],
            "obesity_rate": [30.5],
            "geometry": [Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])],
        })
        brfss_data = pd.DataFrame({
            "Year": [2023],
            "State": ["TESTSTATE"],
            "Obesity_Rate": [30.5],
        })
        merged_data = merge_datasets(geo_data, brfss_data)
        self.assertEqual(merged_data.shape[0], 1)
        self.assertEqual(merged_data.loc[0, "State"], "TESTSTATE")
        self.assertEqual(merged_data.loc[0, "obesity_rate"], 30.5)

if __name__ == "__main__":
    unittest.main()