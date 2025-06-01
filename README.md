# Crop Yield Prediction System

A machine learning-based web application for predicting crop yields based on various environmental and agricultural factors.

## Features

- Crop yield prediction based on location, soil, and weather data
- Interactive web interface for data input and visualization
- Support for multiple crops and regions
- Data analysis and visualization tools
- Plant disease identification using CNN

## Technologies Used

- **Backend**: Flask, Python
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning**: Scikit-learn, TensorFlow, Keras
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib

## Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/crop-yield-prediction.git
   cd crop-yield-prediction
   ```

2. Create and activate a virtual environment
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Unix or MacOS
   ```

3. Install the required packages
   ```
   pip install -r requirements.txt
   ```

4. Run the application
   ```
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Project Structure

- `app.py`: Main Flask application file
- `train_model.py`: Script for training the crop yield prediction model
- `data/`: Directory containing data processing scripts and datasets
- `models/`: Directory for storing trained models
- `static/`: Static files (CSS, JavaScript, images)
- `templates/`: HTML templates for the web interface
- `uploads/`: Directory for user-uploaded files

## Usage

1. Navigate to the home page
2. Enter the required information (location, soil type, etc.)
3. Click on "Predict Yield" to get the predicted crop yield
4. Explore other features like disease identification and yield analysis

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
