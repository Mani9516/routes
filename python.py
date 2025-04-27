import math
import folium
from geopy.geocoders import Nominatim
import streamlit as st
from streamlit_folium import folium_static

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        st.error(f"Coordinates not found for '{city_name}'. Please check the spelling or try a different city.")
        return None, None

def distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    # Calculate the differences in latitude and longitude
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    # Calculate the distance using Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def plot_map(city1, city2, lat1, lon1, lat2, lon2):
    # Create a map centered around the midpoint of the two cities
    m = folium.Map(location=[(lat1 + lat2) / 2, (lon1 + lon2) / 2], zoom_start=5)
    # Add markers for the two cities
    folium.Marker([lat1, lon1], tooltip=city1).add_to(m)
    folium.Marker([lat2, lon2], tooltip=city2).add_to(m)
    # Add a line connecting the two cities
    folium.PolyLine([(lat1, lon1), (lat2, lon2)], color="blue", weight=2.5, opacity=1).add_to(m)
    return m

def main():
    st.title("Distance between Two Cities")

    # Input the names of the cities
    city1 = st.text_input("Enter the name of the first city:")
    city2 = st.text_input("Enter the name of the second city:")

    if st.button("Calculate Distance"):
        if not city1 or not city2:
            st.error("Please enter the names of both cities.")
            return

        # Get coordinates of the cities
        lat1, lon1 = get_coordinates(city1)
        lat2, lon2 = get_coordinates(city2)
        if lat1 is not None and lon1 is not None and lat2 is not None and lon2 is not None:
            # Calculate the distance between the cities
            dist = distance(lat1, lon1, lat2, lon2)
            # Print the result
            st.success(f"The distance between {city1} and {city2} is approximately {dist:.2f} kilometers.")
            # Plot map
            m = plot_map(city1, city2, lat1, lon1, lat2, lon2)
            # Display the map
            folium_static(m)
        else:
            st.error("Distance and map generation cannot be performed due to missing coordinates.")

if __name__ == "__main__":
    main()
