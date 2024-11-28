# Project Plan

## Title
Analyzing Obesity Trends and Geographic Correlations Using Automated Data Pipeline


## Main Question

How are obesity trends distributed across different regions in the U.S., and what geographic factors influence these trends?

## Description

Obesity in the United States presents a significant challenge to public health, with varying trends across different regions. This project will focus on analyzing obesity patterns by combining data on physical activity, nutrition, and obesity from the Behavioral Risk Factor Surveillance System (BRFSS) with geographic data on obesity rates by state. The goal is to identify key geographic and behavioral trends that influence obesity across the country. By developing an automated data pipeline, this project will efficiently process large datasets to uncover correlations between regional factors and obesity rates. Ultimately, this analysis aims to inform public health strategies by pinpointing the areas most affected and the factors contributing to these disparities.

## Datasources

Datasource1: Obesity and Health Behaviors Survey Data

Metadata URL: https://catalog.data.gov/dataset/nutrition-physical-activity-and-obesity-behavioral-risk-factor-surveillance-system/resource/0280bb9c-4de8-4b95-9642-93f727c4d305

Data URL: https://data.cdc.gov/api/views/hn4x-zwk7/rows.csv?accessType=DOWNLOAD

Data Type: CSV

Description: This dataset contains information about nutrition, physical activity, and obesity from the Behavioral Risk Factor Surveillance System. It provides valuable insights into obesity-related behaviors, demographics, and health conditions across various U.S. regions.

Datasource2: Geographic Obesity Patterns by State
Metadata URL: https://data-lakecountyil.opendata.arcgis.com/datasets/lakecountyil::national-obesity-by-state/explore

Data URL: https://services3.arcgis.com/HESxeTbDliKKvec2/arcgis/rest/services/LakeCounty_Health/FeatureServer/8/query?outFields=*&where=1%3D1&f=geojson

Data Type: GeoJSON

Description: This dataset provides geographic data on obesity rates across different states, which can be used to correlate obesity trends with regional factors like urbanization, socioeconomic status, and access to healthcare.


## Work Packages

-> Data Cleaning and Preprocessing
-> Exploratory Data Analysis (EDA) and Visualization
-> Geographic Correlation Analysis
-> Automated Data Pipeline Development
-> Reporting and Documentation
