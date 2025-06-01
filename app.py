from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import numpy as np
from data.location_data import get_states, get_districts, get_taluks, get_weather_for_location
from data.crop_data import CROP_DATA, load_crop_yield_data, average_yield_per_crop
from train_model import train_model
import logging
import os
import json

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define model paths
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

MODEL_PATH = os.path.join(MODEL_DIR, 'crop_yield_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')
FEATURES_PATH = os.path.join(MODEL_DIR, 'feature_columns.json')
CATEGORICAL_VALUES_PATH = os.path.join(MODEL_DIR, 'categorical_values.json')
CROP_STATS_PATH = os.path.join(MODEL_DIR, 'crop_stats.json')

# Initialize model and scaler
model = None
scaler = None
feature_columns = None
categorical_values = None

def initialize_model():
    global model, scaler, feature_columns, categorical_values
    
    try:
        # Check if model exists, if not train it
        if not os.path.exists(MODEL_PATH):
            logger.info("Model not found. Training new model...")
            result = train_model()
            
            if result['status'] != 'success':
                raise Exception(f"Model training failed: {result.get('error', 'Unknown error')}")
                
            model = result['model']
            feature_columns = result['feature_columns']
            scaler = result['scaler']  # Ensure scaler is included in the training result
            
            # Save the model components
            joblib.dump(model, MODEL_PATH)
            joblib.dump(scaler, SCALER_PATH)  # Save the scaler
            with open(FEATURES_PATH, 'w') as f:
                json.dump(feature_columns, f)
            
            # Save categorical values
            categorical_values = result.get('categorical_values', {})
            with open(CATEGORICAL_VALUES_PATH, 'w') as f:
                json.dump(categorical_values, f)
            
            logger.info("Model trained and saved successfully")
        else:
            # Load existing model components
            logger.info("Loading existing model...")
            model = joblib.load(MODEL_PATH)
            scaler = joblib.load(SCALER_PATH)  # Load the scaler
            with open(FEATURES_PATH, 'r') as f:
                feature_columns = json.load(f)
            
            # Load categorical values
            with open(CATEGORICAL_VALUES_PATH, 'r') as f:
                categorical_values = json.load(f)
        
        logger.info("Model initialization successful")
        return True
    except Exception as e:
        logger.error(f"Error initializing model: {str(e)}")
        return False

# Initialize the model when app starts
if not initialize_model():
    logger.error("Failed to initialize model. Application may not work correctly.")

# Load and clean the data once when the app starts
try:
    df = pd.read_csv('data/crop_yield.csv')
    # Clean the data
    df['Season'] = df['Season'].str.strip()  # Remove extra spaces
    df['State'] = df['State'].str.strip()    # Remove extra spaces
    df['Crop'] = df['Crop'].str.strip()      # Remove extra spaces
    
    # Debug info
    logger.info(f"Data loaded successfully. Shape: {df.shape}")
    logger.info(f"Unique seasons: {sorted(df['Season'].unique())}")
    logger.info(f"Unique states: {sorted(df['State'].unique())}")
    logger.info(f"Sample of first few rows:\n{df.head()}")
except Exception as e:
    logger.error(f"Error loading data: {str(e)}")
    df = None

@app.route('/')
def home():
    """Render the home page"""
    try:
        states = get_states()
        return render_template('home.html', states=states)
    except Exception as e:
        logger.error(f"Error in home route: {str(e)}")
        return render_template('error.html', error=str(e))

@app.route('/predict', methods=['GET'])
def predict_page():
    """Render the predict page"""
    try:
        states = get_states()
        # Use the same crop list as optimize page
        crops = sorted(df['Crop'].unique())
        return render_template('predict.html', states=states, crops=crops)
    except Exception as e:
        logger.error(f"Error in predict route: {str(e)}")
        return render_template('error.html', error=str(e))

@app.route('/api/predict', methods=['POST'])
def predict():
    """Make crop yield predictions"""
    try:
        # Ensure model is initialized
        if model is None or scaler is None or feature_columns is None or categorical_values is None:
            if not initialize_model():
                raise ValueError("Failed to initialize model components")

        # Get JSON data
        data = request.json
        logger.info(f"Received prediction request with data: {data}")

        # Get weather data for the location
        weather = get_weather_for_location(data['state'], data.get('district', ''))
        
        # Convert numeric values
        def safe_float(value, default=0.0):
            try:
                return float(value) if value else default
            except (ValueError, TypeError):
                return default
        
        # Get current year if not provided
        from datetime import datetime
        current_year = datetime.now().year
        
        # Prepare input data with actual provided values
        input_data = {
            'State': data['state'],
            'District': data.get('district', ''),
            'Crop': data['crop'],
            'Season': data.get('season', 'Kharif'),
            'Area': safe_float(data.get('area')),  # Remove default to see if value is provided
            'Production': safe_float(data.get('production')),
            'Annual_Rainfall': weather.get('annual_rainfall'),
            'Fertilizer': safe_float(data.get('fertilizer')),
            'Pesticide': safe_float(data.get('pesticide')),
            'Crop_Year': int(data.get('year', current_year))
        }

        # Log the received data for debugging
        logger.info(f"Received input data: {data}")
        logger.info(f"Processed input data: {input_data}")
        
        # Create initial DataFrame
        df = pd.DataFrame([input_data])
        
        # Fill missing numeric values with defaults after creating DataFrame
        default_values = {
            'Area': 1.0,  # 1 hectare
            'Production': 0.0,
            'Annual_Rainfall': 1000.0,  # 1000mm
            'Fertilizer': 100.0,  # 100kg
            'Pesticide': 1.0  # 1kg
        }
        
        # Fill NaN values with defaults and log what was filled
        for col, default_val in default_values.items():
            if pd.isna(df[col]).any():
                logger.info(f"Filling missing value for {col} with default: {default_val}")
                df[col] = df[col].fillna(default_val)

        logger.info(f"DataFrame after filling defaults: {df.to_dict('records')}")

        # Strip whitespace from string columns
        categorical_columns = ['Crop', 'Season', 'State']
        for col in categorical_columns:
            df[col] = df[col].str.strip()

        # Create dummy variables for each categorical column
        encoded_df = df.copy()
        for col in categorical_columns:
            # Get all possible categories for this column from training
            possible_categories = categorical_values[col]
            
            # Create dummy variables for the current column
            dummies = pd.get_dummies(encoded_df[col], prefix=col)
            
            # Add all possible dummy columns from training
            for category in possible_categories:
                dummy_col = f"{col}_{category}"
                if dummy_col not in dummies.columns:
                    dummies[dummy_col] = 0
            
            # Only keep dummy columns that were in training
            keep_cols = [f"{col}_{category}" for category in possible_categories]
            dummies = dummies[keep_cols]
            
            # Add dummy variables to the dataset
            encoded_df = pd.concat([encoded_df, dummies], axis=1)
            # Remove the original categorical column
            encoded_df.drop(col, axis=1, inplace=True)

        # Ensure all numeric feature columns are present
        numeric_features = ['Crop_Year', 'Area', 'Production', 'Annual_Rainfall', 'Fertilizer', 'Pesticide']
        
        # Log the values before scaling
        logger.info("Numeric feature values before scaling:")
        for col in numeric_features:
            if col in encoded_df.columns:
                logger.info(f"{col}: {encoded_df[col].values[0]}")

        # Reorder columns to match training data
        encoded_df = encoded_df[feature_columns]
        logger.info(f"Final feature values before scaling: {encoded_df.iloc[0].to_dict()}")

        # Scale the features
        scaled_features = scaler.transform(encoded_df)
        logger.info(f"Scaled features shape: {scaled_features.shape}")

        # Make prediction
        prediction = model.predict(scaled_features)
        predicted_yield = float(prediction[0])
        
        # Get crop statistics for this specific crop
        with open(CROP_STATS_PATH, 'r') as f:
            crop_stats = json.load(f)
            
        crop_name = data['crop']
        crop_mean = crop_stats['means'].get(crop_name, 5.0)  # Default mean if crop not found
        crop_std = crop_stats['stds'].get(crop_name, 2.0)   # Default std if crop not found
        
        # Set reasonable bounds based on crop statistics (mean ± 3 standard deviations)
        min_yield = max(0.1, crop_mean - 3 * crop_std)
        max_yield = crop_mean + 3 * crop_std
        
        # Ensure prediction is within reasonable bounds for this specific crop
        predicted_yield = max(min_yield, min(max_yield, predicted_yield))
        
        # Convert yield from tonnes/hectare to tons/acre (1 hectare = 2.47105 acres)
        predicted_yield_per_acre = predicted_yield / 2.47105
        
        # Calculate total yield based on area if provided
        area = safe_float(data.get('area', 1.0))
        total_predicted_yield = predicted_yield_per_acre * area  # Total yield in tons
        
        # Round all values to 2 decimal places
        predicted_yield_per_acre = round(predicted_yield_per_acre, 2)
        total_predicted_yield = round(total_predicted_yield, 2)
        
        logger.info(f"Prediction details:")
        logger.info(f"Crop: {crop_name}")
        logger.info(f"Mean yield for crop: {crop_mean:.2f} tonnes/hectare")
        logger.info(f"Std dev for crop: {crop_std:.2f} tonnes/hectare")
        logger.info(f"Raw prediction: {prediction[0]:.2f} tonnes/hectare")
        logger.info(f"Bounded prediction: {predicted_yield:.2f} tonnes/hectare")
        logger.info(f"Area: {area:.2f} acres")
        logger.info(f"Final prediction per acre: {predicted_yield_per_acre:.2f} tons/acre")
        logger.info(f"Total predicted yield: {total_predicted_yield:.2f} tons")

        # Get crop information
        crop_info = CROP_DATA.get(data['crop'], {})
        
        response = {
            'success': True,
            'predicted_yield': predicted_yield_per_acre,
            'total_yield': total_predicted_yield,
            'area': area,
            'crop_info': crop_info,
            'input_data': input_data
        }
        
        logger.info(f"Prediction response: {response}")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error in predict route: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/optimize')
def optimize():
    """Render the optimize page"""
    try:
        states = sorted(df['State'].unique())
        seasons = sorted(df['Season'].unique())
        logger.info(f"Available states: {states}")
        logger.info(f"Available seasons: {seasons}")
        return render_template('optimize.html', states=states, seasons=seasons)
    except Exception as e:
        logger.error(f"Error in optimize route: {str(e)}")
        return render_template('error.html', error=str(e))

@app.route('/disease')
def disease():
    """Render the disease detection page"""
    try:
        return render_template('disease.html')
    except Exception as e:
        logger.error(f"Error in disease route: {str(e)}")
        return render_template('error.html', error=str(e))

@app.route('/get_districts')
def get_districts_route():
    """Get districts for a given state"""
    try:
        state = request.args.get('state')
        districts = get_districts(state)
        return jsonify(districts)
    except Exception as e:
        logger.error(f"Error in get_districts route: {str(e)}")
        return jsonify([])

@app.route('/get_taluks')
def get_taluks_route():
    """Get taluks for a given state and district"""
    try:
        state = request.args.get('state')
        district = request.args.get('district')
        taluks = get_taluks(state, district)
        return jsonify(taluks)
    except Exception as e:
        logger.error(f"Error in get_taluks route: {str(e)}")
        return jsonify([])

@app.route('/get_crops')
def get_crops():
    try:
        state = request.args.get('state')
        season = request.args.get('season')
        
        if not state or not season:
            return jsonify({'error': 'State and season are required'}), 400
            
        # Debug info
        logger.info(f"Received request for state: '{state}' and season: '{season}'")
        logger.info(f"Sample of data for this state/season:\n{df[df['State'] == state].head()}")
            
        # Filter crops based on state and season
        filtered_df = df[
            (df['State'] == state) & 
            (df['Season'] == season)
        ]
        
        # Debug info
        logger.info(f"Filtered data shape: {filtered_df.shape}")
        logger.info(f"Filtered data sample:\n{filtered_df.head()}")
        
        filtered_crops = filtered_df['Crop'].unique().tolist()
        filtered_crops.sort()
        
        logger.info(f"Found {len(filtered_crops)} crops for {state} in {season} season")
        logger.info(f"Crops: {filtered_crops}")
        
        return jsonify(filtered_crops)
    except Exception as e:
        logger.error(f"Error in get_crops: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/optimize', methods=['POST'])
def optimize_yield():
    try:
        data = request.json
        logger.info(f"Received optimization request: {data}")

        # Load crop yield data
        df = pd.read_csv('data/crop_yield.csv')

        # Get input parameters
        state = data['state']
        season = data['season']
        crop = data['crop']
        area = float(data['area'])  # in acres
        fertilizer = float(data['fertilizer'])  # per acre
        pesticide = float(data['pesticide'])  # per acre
        rainfall = float(data['rainfall'])  # in mm

        # Convert acres to hectares (1 acre = 0.4047 hectares)
        area_hectares = area * 0.4047
        fertilizer_per_hectare = fertilizer / 0.4047  # convert to kg/hectare
        pesticide_per_hectare = pesticide / 0.4047  # convert to kg/hectare

        # Filter data for the state, season, and crop
        filtered_data = df[
            (df['State'].str.strip() == state.strip()) &
            (df['Season'].str.strip() == season.strip()) &
            (df['Crop'].str.strip() == crop.strip())
        ].copy()

        if filtered_data.empty:
            return jsonify({
                'error': f'No data available for {crop} in {state} during {season} season'
            }), 404

        # Calculate input ratios (per hectare)
        input_fertilizer_ratio = fertilizer_per_hectare
        input_pesticide_ratio = pesticide_per_hectare

        # Calculate same ratios for historical data
        filtered_data['fertilizer_ratio'] = filtered_data['Fertilizer'] / filtered_data['Area']
        filtered_data['pesticide_ratio'] = filtered_data['Pesticide'] / filtered_data['Area']

        # Calculate similarity scores based on input ratios
        filtered_data['fertilizer_similarity'] = 1 / (1 + abs(filtered_data['fertilizer_ratio'] - input_fertilizer_ratio))
        filtered_data['pesticide_similarity'] = 1 / (1 + abs(filtered_data['pesticide_ratio'] - input_pesticide_ratio))

        # Calculate overall similarity score (weighted average)
        filtered_data['similarity_score'] = (
            filtered_data['fertilizer_similarity'] * 0.4 +
            filtered_data['pesticide_similarity'] * 0.4 +
            filtered_data['Yield'] * 0.2  # Also consider historical yield
        )

        # Calculate statistics for the selected crop
        avg_yield = filtered_data['Yield'].mean()
        yield_std = filtered_data['Yield'].std()
        avg_rainfall = filtered_data['Annual_Rainfall'].mean()
        avg_fertilizer = filtered_data['fertilizer_ratio'].mean()
        avg_pesticide = filtered_data['pesticide_ratio'].mean()

        # Calculate yield stability
        yield_stability = 1 - (yield_std / avg_yield) if avg_yield > 0 else 0

        # Convert yield from tonnes/hectare to tons/acre
        # 1 hectare = 2.47105 acres
        yield_per_acre = avg_yield / 2.47105  # Convert to tons/acre directly
        total_expected_yield = yield_per_acre * area  # Total yield in tons

        # Round all values to 2 decimal places
        yield_per_acre = round(yield_per_acre, 2)
        total_expected_yield = round(total_expected_yield, 2)

        # Log the yield calculations for debugging
        logger.info(f"Yield calculations:")
        logger.info(f"Average yield: {avg_yield:.2f} tonnes/hectare")
        logger.info(f"Area: {area:.2f} acres")
        logger.info(f"Yield per acre: {yield_per_acre:.2f} tons/acre")
        logger.info(f"Total expected yield: {total_expected_yield:.2f} tons")

        # Convert input ratios to per acre basis
        fertilizer_per_acre = avg_fertilizer / 2.47105
        pesticide_per_acre = avg_pesticide / 2.47105

        # Prepare recommendations
        recommendations = [{
            'crop': crop,
            'season': season,
            'similarity_score': round(filtered_data['similarity_score'].mean(), 2),
            'yield_per_acre': yield_per_acre,  # Yield per acre in tons
            'expected_yield': total_expected_yield,  # Total yield in tons for the given area
            'yield_stability': round(yield_stability * 100, 1),
            'requirements': {
                'area': f"{area} acres",
                'fertilizer': f"{round(fertilizer_per_acre, 2)} kg/acre",
                'pesticide': f"{round(pesticide_per_acre, 2)} kg/acre",
                'rainfall': f"{round(avg_rainfall, 2)} mm/year"
            },
            'optimization_tips': [
                f"Optimal fertilizer usage: {round(fertilizer_per_acre, 2)} kg/acre",
                f"Optimal pesticide usage: {round(pesticide_per_acre, 2)} kg/acre",
                f"Expected yield per acre: {yield_per_acre} tons/acre",
                f"Total expected yield: {total_expected_yield} tons",
                f"Expected yield stability: {round(yield_stability * 100, 1)}%"
            ]
        }]

        response = {
            'recommendations': recommendations,
            'input_parameters': {
                'state': state,
                'season': season,
                'crop': crop,
                'area': area,
                'fertilizer_ratio': round(fertilizer, 2),
                'pesticide_ratio': round(pesticide, 2),
                'rainfall': rainfall
            }
        }
        logger.info(f"Optimization results: {response}")  # Log the results before returning
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error in optimize_yield: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/detect_disease', methods=['POST'])
def detect_disease():
    """Detect crop diseases from image"""
    try:
        if 'image' not in request.files:
            raise ValueError("No image file provided")
            
        image_file = request.files['image']
        if image_file.filename == '':
            raise ValueError("No image selected")
            
        # Get crop type
        crop = request.form.get('crop', '')
        if not crop:
            raise ValueError("No crop type specified")
            
        # TODO: Implement actual disease detection using a trained model
        # For now, return dummy response
        diseases = {
            'Rice': ['Bacterial leaf blight', 'Brown spot', 'Leaf smut'],
            'Wheat': ['Leaf rust', 'Powdery mildew', 'Septoria tritici blotch'],
            'Maize': ['Northern corn leaf blight', 'Gray leaf spot', 'Common rust']
        }
        
        detected_disease = np.random.choice(diseases.get(crop, ['No disease detected']))
        confidence = round(np.random.uniform(0.7, 0.95), 2)
        
        response = {
            'success': True,
            'disease': detected_disease,
            'confidence': confidence,
            'recommendations': [
                'Remove infected plants/parts',
                'Apply appropriate fungicide/pesticide',
                'Improve air circulation',
                'Maintain proper spacing between plants'
            ]
        }
        
        logger.info(f"Disease detection successful: {response}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in detect_disease route: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
