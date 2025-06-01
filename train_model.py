import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
import logging
import os
import json
from flask import request, Flask

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

def train_model():
    try:
        # Update the path to the crop yield data
        crop_yield_data_path = 'data/crop_yield.csv'
        logger.info(f"Loading data from {crop_yield_data_path}")
        
        if not os.path.exists(crop_yield_data_path):
            raise FileNotFoundError(f"Data file not found at {crop_yield_data_path}")
        
        data = pd.read_csv(crop_yield_data_path)
        logger.info(f"Loaded dataset with shape: {data.shape}")

        # Analyze data to identify trends
        average_yield = data.groupby('Crop')['Yield'].mean().reset_index()
        print('Average Yield per Crop:', average_yield)

        # Data preprocessing
        logger.info("Starting data preprocessing")
        
        # Drop any missing values
        if data.isnull().values.any():
            data = data.dropna()
            logger.info("Dropped missing values")

        # Strip whitespace from string columns
        categorical_columns = ['Crop', 'Season', 'State']
        for col in categorical_columns:
            data[col] = data[col].str.strip()
        logger.info("Cleaned string columns")

        # Save unique values for each categorical column
        categorical_values = {
            col: sorted(data[col].unique().tolist())
            for col in categorical_columns
        }

        # Create dummy variables for each categorical column
        encoded_data = data.copy()
        for col in categorical_columns:
            # Create dummy variables
            dummies = pd.get_dummies(encoded_data[col], prefix=col)
            # Add dummy variables to the dataset
            encoded_data = pd.concat([encoded_data, dummies], axis=1)
            # Remove the original categorical column
            encoded_data.drop(col, axis=1, inplace=True)

        # Get feature columns (all columns except 'Yield')
        feature_columns = [col for col in encoded_data.columns if col != 'Yield']
        
        # Create models directory if it doesn't exist
        models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)

        # Save categorical values
        with open(os.path.join(models_dir, 'categorical_values.json'), 'w') as f:
            json.dump(categorical_values, f)
        logger.info("Saved categorical values")

        # Save feature columns
        with open(os.path.join(models_dir, 'feature_columns.json'), 'w') as f:
            json.dump(feature_columns, f)
        logger.info("Saved feature columns")

        # Calculate and save crop statistics for denormalization
        crop_means = data.groupby('Crop')['Yield'].mean()
        crop_stds = data.groupby('Crop')['Yield'].std()
        crop_stats = {
            'means': crop_means.to_dict(),
            'stds': crop_stds.to_dict()
        }
        with open(os.path.join(models_dir, 'crop_stats.json'), 'w') as f:
            json.dump(crop_stats, f)
        logger.info("Saved crop statistics")

        # Split features and target
        X = encoded_data[feature_columns]
        y = encoded_data['Yield']

        # Create and fit the scaler
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=X.columns)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        logger.info("Split data into training and test sets")

        # Check for negative yield stability
        yield_stability = np.std(y) / np.mean(y)
        if yield_stability < 0:
            raise ValueError("Yield stability cannot be negative.")

        # Function to calculate optimal rainfall
        def calculate_optimal_rainfall(rainfall_input):
            optimal_rainfall = 919.82  # mm/year
            if rainfall_input < optimal_rainfall:
                return f'Optimal rainfall is {optimal_rainfall} mm/year.'
            else:
                return 'Rainfall is sufficient.'

        @app.route('/rainfall', methods=['POST'])
        def process_rainfall():
            rainfall_input = float(request.form['rainfall'])  # Get rainfall from the request
            rainfall_status = calculate_optimal_rainfall(rainfall_input)
            return rainfall_status

        @app.route('/api/predict', methods=['POST'])
        def predict():
            data = request.get_json()
            # Validate input data
            required_fields = ['area', 'rainfall', 'annual_rainfall', 'production', 'fertilizer', 'pesticide', 'state', 'crop', 'season']
            for field in required_fields:
                if field not in data:
                    return json.dumps({'success': False, 'error': f'Missing field: {field}'})

            # Check if model file exists
            model_path = 'g:/Mini Project/models/crop_yield_model.pkl'
            if not os.path.exists(model_path):
                return json.dumps({'success': False, 'error': 'Model file not found.'})

            # Load the trained model
            model = joblib.load(model_path)

            # Extract input data
            area = data['area']
            rainfall = data['rainfall']
            annual_rainfall = data['annual_rainfall']
            production = data['production']
            fertilizer = data['fertilizer']
            pesticide = data['pesticide']
            state = data['state']
            crop = data['crop']
            season = data['season']

            # Prepare the input features for prediction
            input_features = np.array([[area, rainfall, annual_rainfall, production, fertilizer, pesticide]])

            logger.info('Starting prediction process')
            # Make the prediction
            try:
                logger.info('Calling model.predict()')
                prediction = model.predict(input_features)
                logger.info(f'Prediction result: {prediction}')
                logger.info('Prediction process completed')
                return json.dumps({'success': True, 'prediction': prediction[0]})
            except Exception as e:
                logger.error(f"Error during prediction: {str(e)}")
                return json.dumps({'success': False, 'error': 'Prediction failed. Please check your input.'})

        # Analyze crop yield data and adjust model training
        crop_yield_data = pd.read_csv('data/crop_yield.csv')
        average_yield = crop_yield_data.groupby('Crop')['Yield'].mean().reset_index()
        print('Average Yield per Crop:', average_yield)

        # Train random forest model with adjusted parameters
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=42,
            n_jobs=-1
        )
        
        logger.info("Training model")
        model.fit(X_train, y_train)
        logger.info("Model training completed")

        # Save model and scaler
        joblib.dump(model, os.path.join(models_dir, 'crop_yield_model.pkl'))
        joblib.dump(scaler, os.path.join(models_dir, 'scaler.pkl'))

        # Evaluate model
        train_predictions = model.predict(X_train)
        test_predictions = model.predict(X_test)

        train_mse = mean_squared_error(y_train, train_predictions)
        test_mse = mean_squared_error(y_test, test_predictions)
        train_r2 = r2_score(y_train, train_predictions)
        test_r2 = r2_score(y_test, test_predictions)

        logger.info(f"Train MSE: {train_mse:.4f}, R2: {train_r2:.4f}")
        logger.info(f"Test MSE: {test_mse:.4f}, R2: {test_r2:.4f}")

        return {
            'status': 'success',
            'model': model,
            'scaler': scaler,
            'feature_columns': feature_columns,
            'categorical_values': categorical_values,
            'metrics': {
                'train_mse': train_mse,
                'test_mse': test_mse,
                'train_r2': train_r2,
                'test_r2': test_r2
            }
        }
    except Exception as e:
        logger.error(f"Error in training model: {str(e)}")
        return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    result = train_model()
    if result['status'] == 'success':
        logger.info("Model training completed successfully!")