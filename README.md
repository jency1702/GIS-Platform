# GIS Data Visualization Dashboard

This is an interactive GIS dashboard built using **Streamlit** and **Folium** for visualizing and analyzing **BC (Bank Correspondent) data** based on various parameters such as state, pincode, gender, and bank name. The dashboard includes features like heatmap visualization, gender-based markers, and interactive maps with marker clustering.

## Features

- **Data Filters**: Filter the dataset by:
  - State
  - Pincode
  - Bank Name
  - Gender (Male/Female)
  
- **Data Visualization**:
  - **Heatmap**: Visualize BCs as a heatmap.
  - **Marker Clusters**: Cluster markers on the map for better visualization.
  - **Gender-based Markers**: Color-coded markers (blue for male, red for female).
  - **Detailed Popups**: Click on markers to view detailed information about BCs.
  
- **Interactive Map**:
  - Measure control to measure distance in kilometers.
  - Fullscreen option for better map view.
  - Locate control to locate your current position on the map.
  - MiniMap for a small overview of the map.

## Requirements

To run the application, ensure you have the following Python packages installed:

- `streamlit`
- `pandas`
- `folium`
- `geopy`
- `requests`
- `streamlit_folium`
- `urllib3`

You can install them using pip:

```bash
pip install streamlit pandas folium geopy requests streamlit_folium urllib3
