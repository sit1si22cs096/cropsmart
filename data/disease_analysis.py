import os
import random
import logging
from PIL import Image
import numpy as np
import torch
from torchvision import models, transforms

# Set up logging
logging.basicConfig(level=logging.INFO)

# Path to the dataset
DATASET_PATH = 'g:/Mini Project/data/archive'

# Load a pre-trained model
model = models.resnet18(weights='DEFAULT')  # Use the latest weights
model.eval()  # Set the model to evaluation mode

# Define the image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Function to analyze disease based on image filename
def analyze_disease(image_filename):
    logging.info(f'Analyzing image: {image_filename}')  # Log the input filename

    # Open the image using PIL
    img = Image.open(image_filename)
    img_array = np.array(img)

    # Example: Analyze the image based on color distribution
    # This is a placeholder for actual image processing logic
    mean_color = img_array.mean(axis=(0, 1))  # Calculate mean color
    logging.info(f'Mean color: {mean_color}')  # Log the mean color

    # Simulated conditions based on image characteristics
    if mean_color[0] > 200:  # Example condition based on red channel
        result = {'disease': 'Powdery Mildew', 'confidence': 90}
    elif mean_color[1] < 100:  # Example condition based on green channel
        result = {'disease': 'Rust', 'confidence': 85}
    else:
        result = {'disease': 'Unknown', 'confidence': 0}

    logging.info(f'Analysis result: {result}')  # Log the result
    return result

# Function to analyze a single image using pre-trained model
def analyze_image(image_path):
    # Load and preprocess the image
    img = Image.open(image_path).convert("RGB")
    img_tensor = transform(img).unsqueeze(0)  # Add batch dimension

    # Perform inference
    with torch.no_grad():
        outputs = model(img_tensor)
    
    # Log raw model outputs
    logging.info(f'Raw model outputs: {outputs}')  # Log the raw outputs

    # Get the predicted class and confidence
    probabilities = torch.nn.functional.softmax(outputs, dim=1)
    confidence, predicted = torch.max(probabilities, 1)
    
    # Map the predicted class index to the corresponding disease name
    class_names = ['Healthy', 'Powdery Mildew', 'Rust', 'Other Disease']  # Updated class names
    predicted_class = class_names[predicted.item()]
    
    return predicted_class, confidence.item() * 100  # Return confidence as a percentage

# Function to compare two images
def compare_images(image1, image2):
    """Calculate similarity between two images."""
    img1 = Image.open(image1).convert("RGB")
    img2 = Image.open(image2).convert("RGB")
    
    img1 = transform(img1)
    img2 = transform(img2)
    
    # Calculate the mean squared error
    mse = np.mean((img1.numpy() - img2.numpy()) ** 2)
    return mse

# Function to analyze similar images
def analyze_similar_images(uploaded_image_path):
    dataset_path = 'g:/Mini Project/data/archive'
    min_mse = float('inf')
    most_similar_image = None

    # Compare uploaded image with images in the dataset
    for filename in os.listdir(dataset_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            dataset_image_path = os.path.join(dataset_path, filename)
            mse = compare_images(uploaded_image_path, dataset_image_path)
            if mse < min_mse:
                min_mse = mse
                most_similar_image = dataset_image_path

    # Analyze the most similar image
    if most_similar_image:
        predicted_class, confidence = analyze_image(most_similar_image)
        logging.info(f'Most similar image: {most_similar_image}, Predicted Disease: {predicted_class}, Confidence: {confidence}%')

# Function to analyze all images in the dataset directory
def analyze_all_images_in_dataset():
    dataset_path = 'g:/Mini Project/data/archive'
    for filename in os.listdir(dataset_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Check for image files
            full_path = os.path.join(dataset_path, filename)
            result = analyze_disease(full_path)  # Analyze each image
            predicted_class, confidence = analyze_image(full_path)  # Analyze each image
            logging.info(f'Pre-trained model result: {predicted_class} with confidence {confidence}%')  # Log the result from pre-trained model

# Example usage
if __name__ == '__main__':
    # Call this function to analyze all images in the dataset
    analyze_all_images_in_dataset()

    # Example usage for image comparison
    uploaded_image_path = 'path_to_your_uploaded_image.jpg'  # Replace with the actual uploaded image path
    analyze_similar_images(uploaded_image_path)
