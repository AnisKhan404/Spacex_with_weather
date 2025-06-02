import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Model load karo
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Sidebar navigation buttons
st.sidebar.title("Navigation")
prediction_page = st.sidebar.button("Prediction Page")
maps_page = st.sidebar.button("Maps Page")
csv_page = st.sidebar.button("CSV Data Page")

# Helper to track active page
if 'page' not in st.session_state:
    st.session_state.page = 'prediction'

if prediction_page:
    st.session_state.page = 'prediction'
elif maps_page:
    st.session_state.page = 'maps'
elif csv_page:
    st.session_state.page = 'csv'

# --------- Prediction Page ----------
if st.session_state.page == 'prediction':
    st.title("SpaceX Launch Success Prediction")

    lat = st.number_input('Latitude', value=28.5)
    lon = st.number_input('Longitude', value=-80.6)
    temperature_2m = st.number_input('Temperature (°C)', value=20.0)
    relative_humidity_2m = st.number_input('Relative Humidity (%)', value=50.0)

    weather_options = {
        'Clear sky (0)': 0,
        'Mainly clear (1)': 1,
        'Partly cloudy (2)': 2,
        'Overcast (3)': 3,
        'Drizzle light (51)': 51,
        'Drizzle moderate (53)': 53,
        'Rain light (61)': 61,
        'Rain moderate (63)': 63,
        'Rain heavy (65)': 65
    }
    selected_weather = st.selectbox('Weather Condition', list(weather_options.keys()))
    weathercode = weather_options[selected_weather]

    wind_speed_10m = st.number_input('Wind Speed (m/s)', value=5.0)
    rocket = st.selectbox('Rocket Type (Encoded)', [0, 1, 2])
    payloads = st.selectbox('Number of Payloads (encoded)', [28, 2, 56, 84, 448])
    year = st.number_input('Year', min_value=2000, max_value=2050, value=2025)
    month = st.number_input('Month', min_value=1, max_value=12, value=6)
    day = st.number_input('Day', min_value=1, max_value=31, value=1)
    hour = st.number_input('Hour', min_value=0, max_value=23, value=12)

    input_data = np.array([[lat, lon, temperature_2m, relative_humidity_2m, weathercode,
                            wind_speed_10m, rocket, payloads, year, month, day, hour]])

    if st.button('Predict'):
        prediction = model.predict(input_data)
        confidence = model.predict_proba(input_data)[0][1]
        result = 'Success' if prediction[0] == 1 else 'Failure'
        st.success(f'Launch Prediction: {result} ({confidence*100:.2f}% confidence)')

# --------- Maps Page ----------
elif st.session_state.page == 'maps':
    st.title("All Launch Maps")

    map_files = [
        ("Cluster Map", "cluster_map.html"),
        ("Launch Map", "launch_map.html"),
        ("Launch Temperature Map", "launch_temperature_map.html")
    ]

    for title, map_path in map_files:
        st.subheader(title)
        with open(map_path, 'r', encoding='utf-8') as f:
            map_html = f.read()
        st.components.v1.html(map_html, height=600, scrolling=True)

# --------- CSV Page ----------
elif st.session_state.page == 'csv':
    st.title("CSV Data Viewer")

    df = pd.read_csv('Cleaned_spacex_weather.csv')
    st.dataframe(df)
