import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data():
    """Load and preprocess the crop yield dataset"""
    try:
        # Load the dataset
        df = pd.read_csv('data/crop_yields.csv')
        
        # Basic preprocessing
        df = df.dropna()  # Remove rows with missing values
        
        # Rename columns for consistency
        df = df.rename(columns={
            'State_Name': 'State',
            'Crop_Year': 'Year',
            'Season': 'Season',
            'Crop': 'Crop',
            'Area': 'Area',
            'Production': 'Production',
            'Yield': 'Yield'
        })
        
        return df
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return None

def prepare_features(df):
    """Prepare features for model training"""
    try:
        # Create dummy variables for categorical columns
        categorical_columns = ['State', 'Crop', 'Season']
        df_encoded = pd.get_dummies(df, columns=categorical_columns)
        
        # Add weather-related features (simulated)
        df_encoded['Annual_Rainfall'] = np.random.normal(1000, 200, size=len(df_encoded))
        df_encoded['Fertilizer'] = np.random.normal(100, 20, size=len(df_encoded))
        df_encoded['Pesticide'] = np.random.normal(50, 10, size=len(df_encoded))
        
        # Separate features and target
        X = df_encoded.drop(['Yield', 'Year'], axis=1)
        y = df_encoded['Yield']
        
        return X, y, list(X.columns)
    except Exception as e:
        logger.error(f"Error preparing features: {str(e)}")
        return None, None, None

def train_model():
    """Train the crop yield prediction model"""
    try:
        # Load and prepare data
        df = load_data()
        if df is None:
            raise ValueError("Failed to load data")
        
        # Prepare features
        X, y, feature_columns = prepare_features(df)
        if X is None or y is None:
            raise ValueError("Failed to prepare features")
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train the model
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        model.fit(X_train_scaled, y_train)
        
        # Evaluate the model
        y_pred = model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        logger.info(f"Model Performance - MSE: {mse:.2f}, R2: {r2:.2f}")
        
        return model, scaler, feature_columns
        
    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        return None, None, None

def hectare_to_acre(value):
    """Convert hectare to acre."""
    return value * 2.47105

def print_crop_stats(df):
    """Print statistics about crop yields."""
    print("\nCrop Yield Statistics (per acre):")
    print("=================================\n")
    
    # Convert yields to per acre
    df['Yield'] = df['Yield'].apply(hectare_to_acre)
    
    # Group by crop and calculate statistics
    crop_stats = df.groupby('Crop')['Yield'].agg(['mean', 'std', 'min', 'max', 'count'])
    crop_stats = crop_stats.sort_values('mean', ascending=False)
    
    print("\nTop 10 Highest Yielding Crops:")
    print(crop_stats.head(10))
    
    print("\nTypical Yield Ranges by Crop Type:")
    for crop in crop_stats.index:
        stats = crop_stats.loc[crop]
        print(f"\n{crop}:")
        print(f"  Average: {stats['mean']:.2f} per acre")
        print(f"  Normal Range: {max(0, stats['mean'] - stats['std']):.2f} to {stats['mean'] + stats['std']:.2f} per acre")
        print(f"  Historical Range: {stats['min']:.2f} to {stats['max']:.2f} per acre")
        print(f"  Number of records: {int(stats['count'])}")
    
    # Print best states for top crops
    print("\nBest States for Different Crops:")
    print("===============================")
    
    for crop in crop_stats.head(10).index:
        print(f"\n{crop}:")
        state_stats = df[df['Crop'] == crop].groupby('State')['Yield'].agg(['mean', 'count'])
        state_stats = state_stats[state_stats['count'] >= 5]  # At least 5 records
        state_stats = state_stats.sort_values('mean', ascending=False)
        
        for state in state_stats.head(3).index:
            mean = state_stats.loc[state, 'mean']
            count = int(state_stats.loc[state, 'count'])
            print(f"  {state}: {mean:.2f} per acre (based on {count} records)")
    
    # Print seasonal performance
    print("\nSeasonal Performance:")
    print("====================")
    
    for crop in crop_stats.head(10).index:
        print(f"\n{crop}:")
        season_stats = df[df['Crop'] == crop].groupby('Season')['Yield'].agg(['mean', 'count'])
        season_stats = season_stats[season_stats['count'] >= 5]  # At least 5 records
        season_stats = season_stats.sort_values('mean', ascending=False)
        
        for season in season_stats.index:
            mean = season_stats.loc[season, 'mean']
            count = int(season_stats.loc[season, 'count'])
            print(f"  {season:10s}: {mean:.2f} per acre (based on {count} records)")

if __name__ == '__main__':
    # Load data and print statistics
    df = load_data()
    if df is not None:
        print("Loading data...")
        print_crop_stats(df)
    
    # Train and save the model
    model, scaler, feature_columns = train_model()
    
    if model is not None and scaler is not None:
        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)
        
        # Save model components
        joblib.dump(model, 'models/crop_yield_model.pkl')
        joblib.dump(scaler, 'models/scaler.pkl')
        
        # Save feature columns
        import json
        with open('models/feature_columns.json', 'w') as f:
            json.dump(feature_columns, f)
            
        logger.info("Model training and saving completed successfully")
