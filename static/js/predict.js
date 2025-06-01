// Constants for API endpoints
const API_ENDPOINTS = {
    predict: '/api/predict'
};

// Function to show loading indicator
function showLoadingIndicator(show) {
    const loadingIndicator = document.getElementById('loadingIndicator');
    const loadingSpinner = document.getElementById('loadingSpinner');
    if (loadingIndicator) loadingIndicator.style.display = show ? 'flex' : 'none';
    if (loadingSpinner) loadingSpinner.style.display = show ? 'block' : 'none';
}

// Function to validate numeric input
function validateNumericInput(value, min, max, fieldName) {
    if (!value) return null;
    const numValue = parseFloat(value);
    if (isNaN(numValue)) {
        throw new Error(`${fieldName} must be a valid number`);
    }
    if (numValue < min || numValue > max) {
        throw new Error(`${fieldName} must be between ${min} and ${max}`);
    }
    return numValue;
}

// Function to format optimal condition
function formatOptimalCondition(condition) {
    if (typeof condition === 'object' && condition !== null) {
        if (condition.min !== undefined && condition.max !== undefined) {
            return `${condition.min} - ${condition.max}`;
        }
    }
    return condition;
}

// Function to get condition unit
function getConditionUnit(key) {
    const units = {
        'temperature': '°C',
        'humidity': '%',
        'rainfall': ' mm',
        'ph': '',
        'water': ' mm/day'
    };
    return units[key.toLowerCase()] || '';
}

// Function to display prediction results
function displayPredictionResults(data) {
    const predictionResult = document.getElementById('prediction-result');
    
    if (!predictionResult) {
        console.error('Prediction result element not found');
        return;
    }
    
    try {
        // Format the predicted yield with 2 decimal places and ensure it's positive
        const yieldValue = Math.max(0.1, data.predicted_yield).toFixed(2);
        
        // Create the result HTML
        let resultHtml = `
            <div class="alert alert-success mb-4">
                <h4 class="alert-heading mb-2">Prediction Results</h4>
                <p class="display-4 mb-0 text-success">${yieldValue} tonnes/acre</p>
            </div>
        `;

        // Add crop information if available
        if (data.crop_info) {
            resultHtml += `<div class='card mb-4'>`;
            resultHtml += `<div class='card-header bg-info text-white'><h5 class='mb-0'>Crop: ${data.crop_info.name || 'Unknown'}</h5></div>`;
            resultHtml += `<div class='card-body'>`;
            if (data.crop_info.description) {
                resultHtml += `<p>Description: ${data.crop_info.description}</p>`;
            }
            if (data.crop_info.optimal_conditions) {
                resultHtml += `<h6>Optimal Conditions:</h6><ul>`;
                for (const [key, value] of Object.entries(data.crop_info.optimal_conditions)) {
                    resultHtml += `<li>${key.replace(/_/g, ' ')}: ${formatOptimalCondition(value)} ${getConditionUnit(key)}</li>`;
                }
                resultHtml += `</ul>`;
            }
            resultHtml += `</div></div>`;
        }

        // Update the prediction result
        predictionResult.innerHTML = resultHtml;
        predictionResult.style.display = 'block';
        
        // Scroll to the results
        predictionResult.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
    } catch (error) {
        console.error('Error displaying prediction results:', error);
    }
}

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing form...');
    
    const form = document.getElementById('yieldPredictionForm');
    if (form) {
        console.log('Form found, adding submit listener...');
        form.addEventListener('submit', handleFormSubmit);
    } else {
        console.error('Prediction form not found!');
    }
});

// Function to handle prediction form submission
async function handleFormSubmit(event) {
    event.preventDefault();
    // Validate input fields
    const inputData = {
        state: document.getElementById('state').value,
        season: document.getElementById('season').value,
        crop: document.getElementById('crop').value,
        area: parseFloat(document.getElementById('area').value),
        fertilizer: parseFloat(document.getElementById('fertilizer').value),
        pesticide: parseFloat(document.getElementById('pesticide').value),
    };
    // Show loading indicator
    showLoadingIndicator(true);
    try {
        const response = await fetch(API_ENDPOINTS.predict, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(inputData),
        });
        const data = await response.json();
        console.log('Prediction data:', data);
        if (!response.ok) throw new Error(data.error || 'Prediction failed');
        displayPredictionResults(data);
    } catch (error) {
        console.error('Error during prediction:', error);
    } finally {
        showLoadingIndicator(false);
    }
}