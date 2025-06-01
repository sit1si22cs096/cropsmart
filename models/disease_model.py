import numpy as np
from sklearn.ensemble import RandomForestClassifier
from skimage.feature import hog
from skimage.transform import resize
from skimage.color import rgb2gray
from skimage.exposure import equalize_hist
from data.disease_data import PLANT_DISEASES
from data.crop_data import get_crop_diseases

class PlantDiseaseModel:
    def __init__(self):
        self.model = None
        self.initialize_model()
    
    def extract_features(self, image):
        # Resize image to a standard size
        img_resized = resize(image, (128, 128))
        
        # Convert to grayscale for texture features
        img_gray = rgb2gray(img_resized)
        img_gray = equalize_hist(img_gray)
        
        # Extract HOG features for texture
        hog_features = hog(img_gray, orientations=9, pixels_per_cell=(8, 8),
                          cells_per_block=(2, 2), feature_vector=True)
        
        # Extract color features
        color_features = []
        for channel in range(3):  # RGB channels
            channel_mean = np.mean(img_resized[:, :, channel])
            channel_std = np.std(img_resized[:, :, channel])
            color_features.extend([channel_mean, channel_std])
        
        # Combine features
        features = np.concatenate([hog_features, color_features])
        return features
    
    def initialize_model(self):
        self.model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
        
        # Generate synthetic training data based on disease profiles
        X_train = []
        y_train = []
        
        for disease, info in PLANT_DISEASES.items():
            # Generate 50 samples per disease
            for _ in range(50):
                # Create synthetic feature vector
                hog_features = np.random.uniform(0, 1, 324)  # HOG features
                
                # Color features based on disease profile
                color_features = []
                for channel in ['r', 'g', 'b']:
                    range_min, range_max = info['color_profile'][channel]
                    mean = np.random.uniform(range_min, range_max)
                    std = np.random.uniform(0, 0.2)
                    color_features.extend([mean, std])
                
                # Combine features
                features = np.concatenate([hog_features, color_features])
                X_train.append(features)
                y_train.append(disease)
        
        # Train the model
        self.model.fit(np.array(X_train), np.array(y_train))
    
    def predict(self, image, weather_info=None, crop_type=None):
        # Extract features from the image
        features = self.extract_features(image)
        
        # Get base predictions
        probabilities = self.model.predict_proba([features])[0]
        
        # Get crop-specific diseases if crop_type is provided
        crop_diseases = get_crop_diseases(crop_type) if crop_type else None
        
        # Create response dictionary with weather context
        diseases = {}
        for disease, prob in zip(self.model.classes_, probabilities):
            # Skip if disease is not relevant for the crop
            if crop_diseases and disease not in crop_diseases:
                continue
                
            if prob > 0.1:  # Only include diseases with >10% probability
                seasonal_factor = 1.0
                disease_info = PLANT_DISEASES[disease]
                
                # Adjust probability based on weather if available
                if weather_info:
                    # Adjust based on season
                    if weather_info['season'] in disease_info['seasons'] or 'all' in disease_info['seasons']:
                        seasonal_factor = 1.2
                    
                    # Adjust based on humidity
                    if weather_info['humidity'] > 70 and disease in ['powdery_mildew', 'rust']:
                        seasonal_factor *= 1.1
                
                adjusted_prob = min(1.0, prob * seasonal_factor)
                
                diseases[disease] = {
                    'probability': float(adjusted_prob),
                    'symptoms': disease_info['symptoms'],
                    'treatment': disease_info['treatment'],
                    'prevention': disease_info['prevention']
                }
        
        return diseases
