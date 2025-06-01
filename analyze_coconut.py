import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('archive (1)/crop_yield.csv')

# Filter for coconut crops
coconut_data = df[df['Crop'].str.strip() == 'Coconut']

# Calculate state-wise statistics
state_stats = coconut_data.groupby('State').agg({
    'Yield': ['mean', 'min', 'max', 'std'],
    'Annual_Rainfall': 'mean',
    'Production': 'mean',
    'Area': 'mean'
}).round(2)

# Calculate rainfall correlation
rainfall_corr = coconut_data['Annual_Rainfall'].corr(coconut_data['Yield'])

print("\n=== Coconut Yield Analysis ===")
print("\nState-wise Coconut Yield Statistics:")
print("===================================")
print(state_stats)

print("\nRainfall Impact:")
print("===============")
print(f"Correlation between Rainfall and Yield: {rainfall_corr:.3f}")

# Find optimal conditions
best_yields = coconut_data.nlargest(5, 'Yield')
print("\nTop 5 Highest Yield Conditions:")
print("==============================")
for _, row in best_yields.iterrows():
    print(f"\nState: {row['State']}")
    print(f"Yield: {row['Yield']:.2f}")
    print(f"Rainfall: {row['Annual_Rainfall']:.2f}")
    print(f"Area: {row['Area']:.2f}")
    print(f"Year: {row['Crop_Year']}")
