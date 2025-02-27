# NYC Airbnb Analysis

## Overview

This project analyzes Airbnb prices in New York City to identify key factors influencing pricing trends. The study explores:

- The impact of **proximity to points of interest (POIs)** on pricing.
- The effect of **public transportation accessibility** on variations in Airbnb prices.
- The correlation between **neighborhood crime rates** and Airbnb pricing trends.

## Dataset

The analysis integrates multiple datasets, including:

- **Airbnb Listings**: Details about rental properties in NYC.
- **Points of Interest (POIs)**: Nearby landmarks and attractions.
- **Public Transportation Data**: Subway and bus station locations.
- **Crime Data**: Crime statistics by neighborhood.

## Methodology

1. **Data Preprocessing**

   - Cleaning and merging datasets.
   - Handling missing values.
   - Normalizing data for analysis.

2. **Exploratory Data Analysis (EDA)**

   - Visualizing Airbnb price distributions.
   - Identifying trends in popular neighborhoods.
   - Analyzing price variations based on external factors.

3. **Clustering Analysis**

   - Segmenting NYC regions using clustering techniques (e.g., K-Means, DBSCAN).
   - Analyzing how clusters relate to Airbnb pricing.

4. **Regression & Machine Learning Models**
   - Building predictive models to understand pricing influences.
   - Evaluating model performance and feature importance.

## Results & Insights

- Identified high-demand areas based on pricing and popularity.
- Determined key factors affecting pricing, such as proximity to landmarks and transportation.
- Provided insights on how crime rates influence Airbnb rental costs.

## Technologies Used

- **Python** (Pandas, NumPy, Scikit-Learn, Matplotlib, Seaborn)
- **Jupyter Notebook**
- **Geospatial Analysis** (Folium, Geopandas)
