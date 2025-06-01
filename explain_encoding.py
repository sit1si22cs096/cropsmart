import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('archive (1)/crop_yield.csv')

# Get a small sample of different crops
sample_data = df.groupby('Crop').first().reset_index()[['Crop', 'Yield']].head()
print("\nOriginal Data:")
print("=============")
print(sample_data)

# Perform one-hot encoding
encoded_data = pd.get_dummies(sample_data, columns=['Crop'])
print("\nAfter One-Hot Encoding:")
print("=====================")
print(encoded_data)

# Show what happens when predicting for coconut
print("\nWhen Predicting for Coconut:")
print("=========================")
print("Crop_Coconut = 1 (Yes, it is coconut)")
print("All other Crop_* columns = 0 (No, it's not those crops)")

# Show yield ranges
print("\nYield Ranges by Crop Type:")
print("========================")
crop_stats = df.groupby('Crop')['Yield'].agg(['mean', 'min', 'max']).round(2)
print(crop_stats.head(10))
