

# import streamlit as st
# import pandas as pd
# import folium
# from folium.plugins import HeatMap, MarkerCluster, MeasureControl, Fullscreen, LocateControl, MiniMap
# from geopy.geocoders import Nominatim
# from streamlit_folium import folium_static
# import requests
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
# from concurrent.futures import ThreadPoolExecutor
# import json
# import os

# # Cache file path
# CACHE_FILE = "pincode_cache.json"

# # Load cache from a file
# def load_pincode_cache():
#     if os.path.exists(CACHE_FILE):
#         with open(CACHE_FILE, 'r') as file:
#             return json.load(file)
#     return {}

# # Save cache to a file
# def save_pincode_cache(cache):
#     with open(CACHE_FILE, 'w') as file:
#         json.dump(cache, file)

# # Load pincode cache at start
# pincode_cache = load_pincode_cache()

# # Function to load data
# def load_data():
#     try:
#         Main_data = pd.read_excel('cropMain.xlsx', dtype=str)
#         Main_data = Main_data.applymap(lambda x: x.replace(',', '') if isinstance(x, str) else x)
#         return Main_data
#     except FileNotFoundError:
#         st.error("Error: Unable to find cropMain.xlsx file. Please make sure the file is in the correct location.")
#         return None
#     except Exception as e:
#         st.error(f"Error occurred while loading data: {e}")
#         return None

# # Function to get coordinates from location name
# def get_coordinates_from_location(location):
#     try:
#         geolocator = Nominatim(user_agent="your_app_name")
#         location_data = geolocator.geocode(location)
#         if location_data:
#             return [location_data.latitude, location_data.longitude]
#         else:
#             st.warning(f"No coordinates found for {location}.")
#     except Exception as e:
#         st.warning(f"Error occurred while getting coordinates: {e}")
#     return None

# # Function to get coordinates from pincode with caching
# def get_coordinates_from_pincode(pincode):
#     if pincode in pincode_cache:
#         return pincode_cache[pincode]

#     try:
#         retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
#         session = requests.Session()
#         session.mount('https://', HTTPAdapter(max_retries=retries))

#         url = f'https://nominatim.openstreetmap.org/search?q={pincode}&format=json&limit=1&countrycodes=IN'
#         response = session.get(url, timeout=10)

#         if response.status_code == 200:
#             data = response.json()
#             if data:
#                 coordinates = [float(data[0]['lat']), float(data[0]['lon'])]
#                 pincode_cache[pincode] = coordinates
#                 save_pincode_cache(pincode_cache)  # Save cache after updating
#                 return coordinates
#         else:
#             st.warning(f"Failed to fetch coordinates for pincode: {pincode}. Status code: {response.status_code}")
#     except Exception as e:
#         st.warning(f"Error occurred while getting coordinates: {e}")
#     return None

# # Function to batch fetch coordinates for pincodes
# def batch_fetch_coordinates(pincodes, batch_size=50):
#     coordinates = {}
#     batches = [pincodes[i:i+batch_size] for i in range(0, len(pincodes), batch_size)]

#     with ThreadPoolExecutor() as executor:
#         futures = {executor.submit(get_coordinates_from_pincode, pincode): pincode for pincode in pincodes}
#         for future in futures:
#             pincode = futures[future]
#             try:
#                 coordinates[pincode] = future.result()
#             except Exception as e:
#                 st.warning(f"Error occurred while fetching coordinates for pincode {pincode}: {e}")

#     return coordinates

# # Function to display overall BC details
# def display_overall_bc_details(data, state_data):
#     st.sidebar.write(f"## BC Details Count for {state_data}:")
#     state_data = data[data['State'] == state_data]
#     total_bcs = len(state_data)
#     total_male_bcs = len(state_data[state_data['Gender'].str.lower() == 'male'])
#     total_female_bcs = len(state_data[state_data['Gender'].str.lower() == 'female'])

#     st.sidebar.write(f"Total BCs: {total_bcs}")
#     st.sidebar.write(f"Total Male BCs: {total_male_bcs}")
#     st.sidebar.write(f"Total Female BCs: {total_female_bcs}")

#     bank_count = state_data['Bank Name'].value_counts()

#     st.sidebar.write("## Bank Details Count:")
#     st.sidebar.write(bank_count)

# # Function to display BC details in a popup
# def display_bc_details(row):
#     details = f"<b>Name:</b> {row['Name of BC']}<br>"
#     details += f"<b>Contact Number:</b> {row['Contact Number']}<br>"
#     details += f"<b>Gender:</b> {row['Gender']}<br>"
#     details += f"<b>Bank Name:</b> {row['Bank Name']}<br>"
#     details += f"<b>State:</b> {row['State']}<br>"
#     details += f"<b>Pincode:</b> {row['Pincode']}<br>"
#     return details

# # Main function
# def main():
#     st.set_page_config(
#         page_title="CropMain Dashboard",
#         page_icon="🌾",
#         layout="wide"
#     )

#     st.title("GIS Data Visualization Dashboard")

#     # Load data
#     Main_data = load_data()
#     if Main_data is None:
#         return

#     st.sidebar.write("## Data Options")

#     # Dropdown for State Name
#     state_options = ['All'] + list(Main_data['State'].unique())
#     state_input = st.sidebar.selectbox("Select State Name:", state_options)

#     # Filter pincode options based on state selection
#     if state_input != 'All':
#         pincode_options = ['None'] + list(Main_data[Main_data['State'] == state_input]['Pincode'].unique())
#     else:
#         pincode_options = ['None'] + list(Main_data['Pincode'].unique())

#     pincode_input = st.sidebar.selectbox("Select Pincode:", pincode_options)

#     # Filter bank name options based on state selection
#     if state_input != 'All':
#         bank_name_options = ['None'] + list(Main_data[Main_data['State'] == state_input]['Bank Name'].unique())
#     else:
#         bank_name_options = ['None'] + list(Main_data['Bank Name'].unique())
#     bank_name_input = st.sidebar.selectbox("Select Bank Name:", bank_name_options)

#     # Dropdown for Gender
#     gender_options = ['All', 'Male', 'Female']
#     gender_input = st.sidebar.selectbox("Select Gender:", gender_options)

#     # Filter data based on selected options
#     if pincode_input != 'None':
#         is_pincode_selected = True
#         state_data = Main_data[Main_data['Pincode'] == str(pincode_input)]
#     else:
#         is_pincode_selected = False
#         if state_input and state_input != 'All':
#             state_data = Main_data[Main_data['State'] == state_input]
#             if bank_name_input != 'None':
#                 state_data = state_data[state_data['Bank Name'] == bank_name_input]
#             if gender_input != 'All':
#                 state_data = state_data[state_data['Gender'].str.lower() == gender_input.lower()]
#         else:
#             state_data = Main_data
#             if bank_name_input != 'None':
#                 state_data = state_data[state_data['Bank Name'] == bank_name_input]
#             if gender_input != 'All':
#                 state_data = state_data[state_data['Gender'].str.lower() == gender_input.lower()]

#     show_heatmap = st.sidebar.checkbox("Show Heatmap")
#     show_gender_markers = st.sidebar.checkbox("Show Gender Markers")
#     use_marker_cluster = st.sidebar.checkbox("Use Marker Cluster")
#     visualize_button = st.sidebar.button("Visualize Data")

#     if visualize_button:
#         coordinates = None

#         # Determine the initial coordinates based on selection
#         if is_pincode_selected:
#             coordinates = get_coordinates_from_pincode(str(pincode_input))
#         elif state_input and state_input != 'All':
#             coordinates = get_coordinates_from_location(state_input)

#         # Check if coordinates were successfully retrieved
#         if coordinates:
#             m = folium.Map(location=coordinates, zoom_start=6)

#             # Add Measure Control with distance in kilometers
#             m.add_child(MeasureControl(primary_length_unit='kilometers'))

#             # Add Fullscreen button
#             Fullscreen().add_to(m)

#             # Add LocateControl
#             LocateControl().add_to(m)

#             # Add MiniMap
#             minimap = MiniMap(toggle_display=True)
#             m.add_child(minimap)

#             # Process data visualization based on pincode or state
#             if is_pincode_selected:
#                 pincode_data = Main_data[(Main_data['Pincode'] == str(pincode_input)) & (Main_data['State'] == state_input)]
#                 bc_coordinates = get_coordinates_from_pincode(str(pincode_input))
#                 if bc_coordinates:
#                     marker_color = 'red' if show_gender_markers and pincode_data.iloc[0]['Gender'].lower() == 'female' else 'blue'

#                     if use_marker_cluster:
#                         marker_cluster = MarkerCluster().add_to(m)
#                         marker = folium.Marker(
#                             location=bc_coordinates,
#                             popup=display_bc_details(pincode_data.iloc[0]),
#                             icon=folium.Icon(color=marker_color)
#                         )
#                         marker.add_to(marker_cluster)
#                     else:
#                         marker = folium.Marker(
#                             location=bc_coordinates,
#                             popup=display_bc_details(pincode_data.iloc[0]),
#                             icon=folium.Icon(color=marker_color)
#                         )
#                         marker.add_to(m)
#             else:
#                 # Fetch coordinates for all pincodes in the selected state
#                 if state_input != 'All':
#                     unique_pincodes = state_data['Pincode'].unique()
#                     pincode_coordinates = batch_fetch_coordinates(unique_pincodes)

#                     # Add Markers for each BC based on gender
#                     for _, row in state_data.iterrows():
#                         coordinates = pincode_coordinates.get(row['Pincode'])
#                         if coordinates:
#                             marker_color = 'red' if show_gender_markers and row['Gender'].lower() == 'female' else 'blue'
#                             if use_marker_cluster:
#                                 marker_cluster = MarkerCluster().add_to(m)
#                                 marker = folium.Marker(
#                                     location=coordinates,
#                                     popup=display_bc_details(row),
#                                     icon=folium.Icon(color=marker_color)
#                                 )
#                                 marker.add_to(marker_cluster)
#                             else:
#                                 marker = folium.Marker(
#                                     location=coordinates,
#                                     popup=display_bc_details(row),
#                                     icon=folium.Icon(color=marker_color)
#                                 )
#                                 marker.add_to(m)

#                 # Heatmap visualization
#                 if show_heatmap and not is_pincode_selected:
#                     heat_data = []
#                     for pincode in state_data['Pincode'].unique():
#                         coordinates = pincode_coordinates.get(pincode)
#                         if coordinates:
#                             heat_data.append([coordinates[0], coordinates[1]])
#                     HeatMap(heat_data).add_to(m)

#             # Display the map
#             folium_static(m)

#             # Display BC details in sidebar
#             if state_input and state_input != 'All':
#                 display_overall_bc_details(Main_data, state_input)
#         else:
#             st.warning("Unable to visualize map. Please select a valid state or pincode.")

# if __name__ == "__main__":
#     main()

import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster, MeasureControl, Fullscreen, LocateControl, MiniMap
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor
import json
import os

# Cache file path
CACHE_FILE = "pincode_cache.json"

# Load cache from a file
def load_pincode_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save cache to a file
def save_pincode_cache(cache):
    with open(CACHE_FILE, 'w') as file:
        json.dump(cache, file)

# Load pincode cache at start
pincode_cache = load_pincode_cache()

# Function to load data
def load_data():
    try:
        Main_data = pd.read_excel('cropMain.xlsx', dtype=str)
        Main_data = Main_data.applymap(lambda x: x.replace(',', '') if isinstance(x, str) else x)
        return Main_data
    except FileNotFoundError:
        st.error("Error: Unable to find cropMain.xlsx file. Please make sure the file is in the correct location.")
        return None
    except Exception as e:
        st.error(f"Error occurred while loading data: {e}")
        return None

# Function to get coordinates from location name
def get_coordinates_from_location(location):
    try:
        geolocator = Nominatim(user_agent="your_app_name")
        location_data = geolocator.geocode(location)
        if location_data:
            return [location_data.latitude, location_data.longitude]
        else:
            st.warning(f"No coordinates found for {location}.")
    except Exception as e:
        st.warning(f"Error occurred while getting coordinates: {e}")
    return None

# Function to get coordinates from pincode with caching
def get_coordinates_from_pincode(pincode):
    if pincode in pincode_cache:
        return pincode_cache[pincode]

    try:
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        session = requests.Session()
        session.mount('https://', HTTPAdapter(max_retries=retries))

        url = f'https://nominatim.openstreetmap.org/search?q={pincode}&format=json&limit=1&countrycodes=IN'
        response = session.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data:
                coordinates = [float(data[0]['lat']), float(data[0]['lon'])]
                pincode_cache[pincode] = coordinates
                save_pincode_cache(pincode_cache)  # Save cache after updating
                return coordinates
        else:
            st.warning(f"Failed to fetch coordinates for pincode: {pincode}. Status code: {response.status_code}")
    except Exception as e:
        st.warning(f"Error occurred while getting coordinates: {e}")
    return None

# Function to batch fetch coordinates for pincodes
def batch_fetch_coordinates(pincodes, batch_size=50):
    coordinates = {}
    batches = [pincodes[i:i+batch_size] for i in range(0, len(pincodes), batch_size)]

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_coordinates_from_pincode, pincode): pincode for pincode in pincodes}
        for future in futures:
            pincode = futures[future]
            try:
                coordinates[pincode] = future.result()
            except Exception as e:
                st.warning(f"Error occurred while fetching coordinates for pincode {pincode}: {e}")

    return coordinates

# Function to display overall BC details
def display_overall_bc_details(data, state_data):
    st.sidebar.write(f"## BC Details Count for {state_data}:")
    state_data = data[data['State'] == state_data]
    total_bcs = len(state_data)
    total_male_bcs = len(state_data[state_data['Gender'].str.lower() == 'male'])
    total_female_bcs = len(state_data[state_data['Gender'].str.lower() == 'female'])

    st.sidebar.write(f"Total BCs: {total_bcs}")
    st.sidebar.write(f"Total Male BCs: {total_male_bcs}")
    st.sidebar.write(f"Total Female BCs: {total_female_bcs}")

    bank_count = state_data['Bank Name'].value_counts()

    st.sidebar.write("## Bank Details Count:")
    st.sidebar.write(bank_count)

# Function to display BC charts
def display_bc_charts(state_data):
    # Gender distribution chart
    gender_count = state_data['Gender'].value_counts()
    st.sidebar.write("### Gender Distribution")
    st.bar_chart(gender_count)

    # Bank-wise distribution chart
    bank_count = state_data['Bank Name'].value_counts()
    st.sidebar.write("### Bank-wise Distribution")
    st.bar_chart(bank_count)

# Function to display BC details in a popup
def display_bc_details(row):
    details = f"<b>Name:</b> {row['Name of BC']}<br>"
    details += f"<b>Contact Number:</b> {row['Contact Number']}<br>"
    details += f"<b>Gender:</b> {row['Gender']}<br>"
    details += f"<b>Bank Name:</b> {row['Bank Name']}<br>"
    details += f"<b>State:</b> {row['State']}<br>"
    details += f"<b>Pincode:</b> {row['Pincode']}<br>"
    return details



# Main function
def main():
    st.set_page_config(
        page_title="CropMain Dashboard",
        page_icon="🌾",
        layout="wide"
    )

    st.title("GIS Data Visualization Dashboard")

    # Load data
    Main_data = load_data()
    if Main_data is None:
        return

    st.sidebar.write("## Data Options")

    # Dropdown for State Name
    state_options = ['All'] + list(Main_data['State'].unique())
    state_input = st.sidebar.selectbox("Select State Name:", state_options)

    # Filter pincode options based on state selection
    if state_input != 'All':
        pincode_options = ['None'] + list(Main_data[Main_data['State'] == state_input]['Pincode'].unique())
    else:
        pincode_options = ['None'] + list(Main_data['Pincode'].unique())

    pincode_input = st.sidebar.selectbox("Select Pincode:", pincode_options)

    # Filter bank name options based on state selection
    if state_input != 'All':
        bank_name_options = ['None'] + list(Main_data[Main_data['State'] == state_input]['Bank Name'].unique())
    else:
        bank_name_options = ['None'] + list(Main_data['Bank Name'].unique())
    bank_name_input = st.sidebar.selectbox("Select Bank Name:", bank_name_options)

    # Dropdown for Gender
    gender_options = ['All', 'Male', 'Female']
    gender_input = st.sidebar.selectbox("Select Gender:", gender_options)

    # Filter data based on selected options
    if pincode_input != 'None':
        is_pincode_selected = True
        state_data = Main_data[Main_data['Pincode'] == str(pincode_input)]
    else:
        is_pincode_selected = False
        if state_input and state_input != 'All':
            state_data = Main_data[Main_data['State'] == state_input]
            if bank_name_input != 'None':
                state_data = state_data[state_data['Bank Name'] == bank_name_input]
            if gender_input != 'All':
                state_data = state_data[state_data['Gender'].str.lower() == gender_input.lower()]
        else:
            state_data = Main_data
            if bank_name_input != 'None':
                state_data = state_data[state_data['Bank Name'] == bank_name_input]
            if gender_input != 'All':
                state_data = state_data[state_data['Gender'].str.lower() == gender_input.lower()]

    show_heatmap = st.sidebar.checkbox("Show Heatmap")
    show_gender_markers = st.sidebar.checkbox("Show Gender Markers")
    use_marker_cluster = st.sidebar.checkbox("Use Marker Cluster")
    visualize_button = st.sidebar.button("Visualize Data")

    if visualize_button:
        coordinates = None

        # Determine the initial coordinates based on selection
        if is_pincode_selected:
            coordinates = get_coordinates_from_pincode(str(pincode_input))
        elif state_input and state_input != 'All':
            coordinates = get_coordinates_from_location(state_input)

        # Check if coordinates were successfully retrieved
        if coordinates:
            m = folium.Map(location=coordinates, zoom_start=6)

            # Add Measure Control with distance in kilometers
            m.add_child(MeasureControl(primary_length_unit='kilometers'))

            # Add Fullscreen button
            Fullscreen().add_to(m)

            # Add LocateControl
            LocateControl().add_to(m)

            # Add MiniMap
            minimap = MiniMap(toggle_display=True)
            m.add_child(minimap)

            # Process data visualization based on pincode or state
            if is_pincode_selected:
                pincode_data = Main_data[(Main_data['Pincode'] == str(pincode_input)) & (Main_data['State'] == state_input)]
                bc_coordinates = get_coordinates_from_pincode(str(pincode_input))
                if bc_coordinates:
                    marker_color = 'red' if show_gender_markers and pincode_data.iloc[0]['Gender'].lower() == 'female' else 'blue'

                    if use_marker_cluster:
                        marker_cluster = MarkerCluster().add_to(m)
                        marker = folium.Marker(
                            location=bc_coordinates,
                            popup=display_bc_details(pincode_data.iloc[0]),
                            icon=folium.Icon(color=marker_color)
                        )
                        marker.add_to(marker_cluster)
                    else:
                        marker = folium.Marker(
                            location=bc_coordinates,
                            popup=display_bc_details(pincode_data.iloc[0]),
                            icon=folium.Icon(color=marker_color)
                        )
                        marker.add_to(m)
            else:
                # Fetch coordinates for all pincodes in the selected state
                if state_input != 'All':
                    unique_pincodes = state_data['Pincode'].unique()
                    pincode_coordinates = batch_fetch_coordinates(unique_pincodes)

                    # Add Markers for each BC based on gender
                    for _, row in state_data.iterrows():
                        coordinates = pincode_coordinates.get(row['Pincode'])
                        if coordinates:
                            marker_color = 'red' if show_gender_markers and row['Gender'].lower() == 'female' else 'blue'
                            if use_marker_cluster:
                                marker_cluster = MarkerCluster().add_to(m)
                                marker = folium.Marker(
                                    location=coordinates,
                                    popup=display_bc_details(row),
                                    icon=folium.Icon(color=marker_color)
                                )
                                marker.add_to(marker_cluster)
                            else:
                                marker = folium.Marker(
                                    location=coordinates,
                                    popup=display_bc_details(row),
                                    icon=folium.Icon(color=marker_color)
                                )
                                marker.add_to(m)

                # Heatmap visualization
                if show_heatmap and not is_pincode_selected:
                    heat_data = []
                    for pincode in state_data['Pincode'].unique():
                        coordinates = pincode_coordinates.get(pincode)
                        if coordinates:
                            heat_data.append([coordinates[0], coordinates[1]])
                    HeatMap(heat_data).add_to(m)

            # Display the map
            folium_static(m)

            # Display BC details in sidebar
            if state_input and state_input != 'All':
                display_overall_bc_details(Main_data, state_input)
        else:
            st.warning("Unable to visualize map. Please select a valid state or pincode.")

if __name__ == "__main__":
    main()



