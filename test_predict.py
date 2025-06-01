import requests

# Sample input data for prediction
sample_data = {
    'area': 100,
    'rainfall': 150,
    'annual_rainfall': 200,
    'production': 300,
    'fertilizer': 50,
    'pesticide': 10,
    'state': 'SomeState',
    'crop': 'SomeCrop',
    'season': 'Kharif'
}

# URL of the prediction endpoint
url = 'http://localhost:5000/api/predict'

# Make the POST request to the prediction endpoint
response = requests.post(url, json=sample_data)

# Print the response from the server
print(response.json())
