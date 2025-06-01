"""Location data for India including states, districts, and taluks"""

from datetime import datetime
import random

# Location data structure
INDIA_LOCATIONS = {
    "Andhra Pradesh": {},
    "Arunachal Pradesh": {},
    "Assam": {},
    "Bihar": {},
    "Chhattisgarh": {},
    "Goa": {},
    "Gujarat": {},
    "Haryana": {},
    "Himachal Pradesh": {},
    "Jharkhand": {},
    "Karnataka": {},
    "Kerala": {},
    "Madhya Pradesh": {},
    "Maharashtra": {},
    "Manipur": {},
    "Meghalaya": {},
    "Mizoram": {},
    "Nagaland": {},
    "Odisha": {},
    "Punjab": {},
    "Rajasthan": {},
    "Sikkim": {},
    "Tamil Nadu": {},
    "Telangana": {},
    "Tripura": {},
    "Uttar Pradesh": {},
    "Uttarakhand": {},
    "West Bengal": {},
    "Andaman and Nicobar Islands": {},
    "Chandigarh": {},
    "Dadra and Nagar Haveli": {},
    "Daman and Diu": {},
    "Delhi": {},
    "Jammu and Kashmir": {},
    "Ladakh": {},
    "Lakshadweep": {},
    "Puducherry": {}
}

def get_states():
    """Get list of all states"""
    return sorted(list(INDIA_LOCATIONS.keys()))

def get_districts(state):
    """Get list of districts for a given state"""
    if state in INDIA_LOCATIONS:
        return sorted(list(INDIA_LOCATIONS[state].keys())) if INDIA_LOCATIONS[state] else []
    return []

def get_taluks(state, district):
    """Get list of taluks for a given state and district"""
    if state in INDIA_LOCATIONS and district in INDIA_LOCATIONS[state]:
        return sorted(INDIA_LOCATIONS[state][district])
    return []

def get_weather_for_location(state, district):
    """Get weather data for a given location.
    This is a mock function that returns simulated weather data.
    """
    # Base values for different regions
    region_data = {
        'North': {'temp': 25, 'humidity': 45, 'rainfall': 750},
        'South': {'temp': 28, 'humidity': 70, 'rainfall': 1200},
        'East': {'temp': 26, 'humidity': 65, 'rainfall': 1500},
        'West': {'temp': 27, 'humidity': 55, 'rainfall': 850},
        'Central': {'temp': 26, 'humidity': 50, 'rainfall': 1000},
        'Northeast': {'temp': 24, 'humidity': 75, 'rainfall': 2000}
    }
    
    # Map states to regions
    state_regions = {
        'Jammu and Kashmir': 'North', 'Himachal Pradesh': 'North', 'Punjab': 'North',
        'Uttarakhand': 'North', 'Haryana': 'North', 'Delhi': 'North',
        'Kerala': 'South', 'Tamil Nadu': 'South', 'Karnataka': 'South',
        'Andhra Pradesh': 'South', 'Telangana': 'South', 'Puducherry': 'South',
        'West Bengal': 'East', 'Odisha': 'East', 'Bihar': 'East',
        'Jharkhand': 'East',
        'Gujarat': 'West', 'Maharashtra': 'West', 'Goa': 'West',
        'Madhya Pradesh': 'Central', 'Chhattisgarh': 'Central',
        'Assam': 'Northeast', 'Meghalaya': 'Northeast', 'Manipur': 'Northeast',
        'Nagaland': 'Northeast', 'Mizoram': 'Northeast', 'Tripura': 'Northeast',
        'Sikkim': 'Northeast', 'Arunachal Pradesh': 'Northeast'
    }
    
    region = state_regions.get(state, 'Central')
    base_data = region_data[region]
    
    # Add some randomization
    temp_var = random.uniform(-2, 2)
    humidity_var = random.uniform(-5, 5)
    rainfall_var = random.uniform(-100, 100)
    
    return {
        'temperature': round(base_data['temp'] + temp_var, 1),
        'humidity': round(base_data['humidity'] + humidity_var, 1),
        'annual_rainfall': round(base_data['rainfall'] + rainfall_var, 1)
    }
