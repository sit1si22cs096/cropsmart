import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('archive (1)/crop_yield.csv')

# Filter for coconut data
coconut_data = df[df['Crop'] == 'Coconut']

print("\nCoconut Growing Conditions Analysis:")
print("===================================")

# Analyze states where coconut grows well
top_states = coconut_data.groupby('State')['Yield'].agg(['mean', 'count']).sort_values('mean', ascending=False)
print("\nTop States for Coconut Yield:")
print(top_states.head())

# Analyze rainfall impact
print("\nRainfall Impact on Coconut Yield:")
rainfall_corr = coconut_data['Annual_Rainfall'].corr(coconut_data['Yield'])
print(f"Correlation with rainfall: {rainfall_corr:.3f}")

# Get optimal rainfall range
good_yields = coconut_data[coconut_data['Yield'] > coconut_data['Yield'].median()]
print(f"\nOptimal Rainfall Range:")
print(f"Min: {good_yields['Annual_Rainfall'].min():.2f} mm")
print(f"Max: {good_yields['Annual_Rainfall'].max():.2f} mm")
print(f"Average: {good_yields['Annual_Rainfall'].mean():.2f} mm")

# Season analysis
print("\nSeason-wise Performance:")
season_stats = coconut_data.groupby('Season')['Yield'].agg(['mean', 'count']).sort_values('mean', ascending=False)
print(season_stats)

# Success conditions
print("\nConditions for High Yield (Top 10% of yields):")
top_performers = coconut_data[coconut_data['Yield'] > coconut_data['Yield'].quantile(0.9)]
print(f"Average Rainfall: {top_performers['Annual_Rainfall'].mean():.2f} mm")
print(f"Best States: {', '.join(top_performers['State'].unique())}")
print(f"Best Seasons: {', '.join(top_performers['Season'].unique())}")
