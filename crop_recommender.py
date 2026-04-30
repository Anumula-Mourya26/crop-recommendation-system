import streamlit as st
import requests
import pandas as pd
    
# --- 1. Mock Database (Expanded) ---
CROP_DATABASE = [
    # Cereals & Grains
    {"name": "Rice", "soil": "Clay", "water": "High", "min_temp": 20, "max_temp": 35, "harvest_time": "4-5 Months",
     "price": "₹2,200 / quintal"},
    {"name": "Wheat", "soil": "Loamy", "water": "Moderate", "min_temp": 10, "max_temp": 25,
     "harvest_time": "4-5 Months", "price": "₹2,125 / quintal"},
    {"name": "Maize", "soil": "Sandy", "water": "Low", "min_temp": 18, "max_temp": 27, "harvest_time": "3-4 Months",
     "price": "₹1,960 / quintal"},
    {"name": "Millets", "soil": "Sandy", "water": "Low", "min_temp": 25, "max_temp": 35, "harvest_time": "2-3 Months",
     "price": "₹2,500 / quintal"},
    {"name": "Sorghum (Jowar)", "soil": "Black", "water": "Low", "min_temp": 25, "max_temp": 32,
     "harvest_time": "3-4 Months", "price": "₹3,180 / quintal"},
    {"name": "Barley", "soil": "Loamy", "water": "Moderate", "min_temp": 12, "max_temp": 32,
     "harvest_time": "4-5 Months", "price": "₹2,000 / quintal"},

    # Cash Crops
    {"name": "Cotton", "soil": "Black", "water": "Moderate", "min_temp": 21, "max_temp": 30,
     "harvest_time": "5-6 Months", "price": "₹7,000 / quintal"},
    {"name": "Sugarcane", "soil": "Loamy", "water": "High", "min_temp": 20, "max_temp": 35,
     "harvest_time": "10-12 Months", "price": "₹315 / quintal"},
    {"name": "Jute", "soil": "Clay", "water": "High", "min_temp": 24, "max_temp": 38, "harvest_time": "4-5 Months",
     "price": "₹5,050 / quintal"},

    # Oilseeds & Pulses
    {"name": "Soybean", "soil": "Loamy", "water": "Moderate", "min_temp": 20, "max_temp": 30,
     "harvest_time": "3-4 Months", "price": "₹4,600 / quintal"},
    {"name": "Groundnut", "soil": "Sandy", "water": "Low", "min_temp": 25, "max_temp": 35, "harvest_time": "4-5 Months",
     "price": "₹6,377 / quintal"},
    {"name": "Gram (Chickpea)", "soil": "Loamy", "water": "Low", "min_temp": 20, "max_temp": 30,
     "harvest_time": "4-5 Months", "price": "₹5,335 / quintal"},
    {"name": "Mustard", "soil": "Loamy", "water": "Low", "min_temp": 10, "max_temp": 25, "harvest_time": "4-5 Months",
     "price": "₹5,450 / quintal"},

    # Vegetables & Tubers
    {"name": "Potato", "soil": "Sandy", "water": "Moderate", "min_temp": 15, "max_temp": 25,
     "harvest_time": "3-4 Months", "price": "₹1,500 / quintal"},
    {"name": "Tomato", "soil": "Loamy", "water": "Moderate", "min_temp": 21, "max_temp": 27,
     "harvest_time": "3-4 Months", "price": "₹2,000 / quintal"},
    {"name": "Onion", "soil": "Loamy", "water": "Low", "min_temp": 15, "max_temp": 30, "harvest_time": "4-5 Months",
     "price": "₹1,800 / quintal"},

    # Plantation & Beverage Crops
    {"name": "Coffee (Arabica)", "soil": "Loamy", "water": "Moderate", "min_temp": 15, "max_temp": 25,
     "harvest_time": "Annual (Nov-Jan)", "price": "₹28,000 / quintal"},
    {"name": "Coffee (Robusta)", "soil": "Loamy", "water": "High", "min_temp": 20, "max_temp": 30,
     "harvest_time": "Annual (Dec-Feb)", "price": "₹22,000 / quintal"},
    {"name": "Tea", "soil": "Loamy", "water": "High", "min_temp": 13, "max_temp": 32,
     "harvest_time": "Continuous Plucking", "price": "₹25,000 / quintal"},
    {"name": "Rubber", "soil": "Loamy", "water": "High", "min_temp": 25, "max_temp": 34,
     "harvest_time": "Continuous Tapping", "price": "₹15,000 / quintal"},

    # Spices (Good for Southern states)
    {"name": "Black Pepper", "soil": "Loamy", "water": "High", "min_temp": 20, "max_temp": 30,
     "harvest_time": "Annual (Dec-Mar)", "price": "₹50,000 / quintal"},
    {"name": "Cardamom", "soil": "Loamy", "water": "High", "min_temp": 15, "max_temp": 25,
     "harvest_time": "Annual (Aug-Dec)", "price": "₹1,50,000 / quintal"},

    # Cold Weather / Hill Crops (Good for Himachal Pradesh testing)
    {"name": "Apple", "soil": "Loamy", "water": "Moderate", "min_temp": 5, "max_temp": 25,
     "harvest_time": "Annual (Aug-Oct)", "price": "₹8,000 / quintal"}
]

# State coordinates for the Weather API (Expanded)
STATE_COORDINATES = {
    "Telangana": {"lat": 17.1231, "lon": 79.2088},
    "Maharashtra": {"lat": 19.7515, "lon": 75.7139},
    "Punjab": {"lat": 31.1471, "lon": 75.3412},
    "Gujarat": {"lat": 22.2587, "lon": 71.1924},
    "Uttar Pradesh": {"lat": 26.8467, "lon": 80.9462},
    "Karnataka": {"lat": 15.3173, "lon": 75.7139},  # Coffee hub
    "Kerala": {"lat": 10.8505, "lon": 76.2711},  # Spices & Rubber
    "Assam": {"lat": 26.2006, "lon": 92.9376},  # Tea hub
    "West Bengal": {"lat": 22.9868, "lon": 87.8550},  # Tea (Darjeeling) & Jute
    "Tamil Nadu": {"lat": 11.1271, "lon": 78.6569},  # Mixed plantations
    "Madhya Pradesh": {"lat": 22.9734, "lon": 78.6569},  # Soybeans & Pulses
    "Rajasthan": {"lat": 27.0238, "lon": 74.2179},  # Millets & Mustard (Low water)
    "Himachal Pradesh": {"lat": 31.1048, "lon": 77.1734}  # Cold weather crops
}

# --- 2. API Integration ---
def fetch_climate_data(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        avg_max = sum(data['daily']['temperature_2m_max']) / len(data['daily']['temperature_2m_max'])
        avg_min = sum(data['daily']['temperature_2m_min']) / len(data['daily']['temperature_2m_min'])
        return (avg_max + avg_min) / 2

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

# --- 3. Recommendation Logic (UPDATED) ---
def recommend_crops(soil, water, current_temp):
    suggestions = []

    # Establish a hierarchy for water needs
    water_hierarchy = {"Low": 1, "Moderate": 2, "High": 3}
    user_water_score = water_hierarchy.get(water, 0)

    for crop in CROP_DATABASE:
        crop_water_score = water_hierarchy.get(crop["water"], 0)

        # Match soil exactly, but allow crops that need equal or LESS water than available
        if crop["soil"] == soil and crop_water_score <= user_water_score:
            # Check temperature tolerance
            if crop["min_temp"] <= current_temp <= crop["max_temp"]:
                suggestions.append(crop)

    return suggestions

# --- 4. User Interface (Streamlit) (UPDATED) ---
def main():
    st.set_page_config(page_title="AgriSuggest", layout="centered")
    st.title("🌱 Intelligent Crop Recommendation System")
    st.write("Enter your field details below to get data-driven crop suggestions based on real-time climate data.")

    # UI Inputs
    col1, col2 = st.columns(2)
    with col1:
        state = st.selectbox("Select State", list(STATE_COORDINATES.keys()))
        water_availability = st.selectbox("Water Availability", ["Low", "Moderate", "High"])
    with col2:
        soil_type = st.selectbox("Soil Type", ["Clay", "Loamy", "Black", "Sandy"])

    # Processing trigger
    if st.button("Get Recommendations", type="primary"):
        with st.spinner("Analyzing climate data and matching crops..."):

            lat = STATE_COORDINATES[state]["lat"]
            lon = STATE_COORDINATES[state]["lon"]

            avg_temp = fetch_climate_data(lat, lon)

            if avg_temp is not None:
                st.success(f"🌡️ Estimated Regional Average Temperature: {avg_temp:.1f}°C")

                results = recommend_crops(soil_type, water_availability, avg_temp)

                st.subheader("Recommended Crops for your Profile:")
                if results:
                    for crop in results:
                        with st.expander(f"🌾 {crop['name']}", expanded=True):
                            # ADDED: Displaying the specific water requirement
                            st.write(f"**Water Requirement:** {crop['water']}")
                            st.write(f"**Estimated Harvest Time:** {crop['harvest_time']}")
                            st.write(f"**Approximate Market Rate:** {crop['price']}")
                            st.write(f"**Ideal Temp Range:** {crop['min_temp']}°C to {crop['max_temp']}°C")
                else:
                    st.warning("No perfect matches found. Try adjusting your inputs.")


if __name__ == "__main__":
    main()