document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!validateRequiredFields()) return;
        
        const formData = {
            country: document.getElementById('country').value,
            state: document.getElementById('state').value,
            district: document.getElementById('district').value,
            taluk: document.getElementById('taluk').value,
            soil_type: document.getElementById('soilType').value,
            ph: parseFloat(document.getElementById('ph').value),
            nitrogen: parseFloat(document.getElementById('nitrogen').value),
            phosphorus: parseFloat(document.getElementById('phosphorus').value),
            potassium: parseFloat(document.getElementById('potassium').value),
            organic_matter: parseFloat(document.getElementById('organic_matter').value)
        };

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            
            if (data.success) {
                updateWeatherInfo(data.weather);
                updatePredictions(data.predictions);
                updateDiseaseInfo(data.disease_info);
            } else {
                showError(data.error || 'Failed to get predictions');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Failed to connect to server');
        }
    });

    // Set up image preview
    const plantImage = document.getElementById('plantImage');
    const imagePreview = document.getElementById('imagePreview');
    
    plantImage.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                imagePreview.classList.remove('d-none');
            }
            reader.readAsDataURL(file);
        }
    });

    // Load initial state
    showSection('predict');

    // Add event listeners for location selection
    document.getElementById('state').addEventListener('change', loadDistricts);
    document.getElementById('district').addEventListener('change', loadTaluks);
    document.getElementById('cropType').addEventListener('change', loadCropInfo);
    
    // Initialize file input for disease analysis
    const fileInput = document.getElementById('diseaseImage');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            if (e.target.files && e.target.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('imagePreview').src = e.target.result;
                    document.getElementById('imagePreviewContainer').classList.remove('d-none');
                };
                reader.readAsDataURL(e.target.files[0]);
            }
        });
    }
});

async function loadDistricts() {
    const state = document.getElementById('state').value;
    const districtSelect = document.getElementById('district');
    const talukSelect = document.getElementById('taluk');
    
    districtSelect.innerHTML = '<option value="">Select District</option>';
    talukSelect.innerHTML = '<option value="">Select Taluk</option>';
    
    if (state) {
        try {
            const response = await fetch(`/get-districts/${state}`);
            const data = await response.json();
            
            if (data.success) {
                data.districts.forEach(district => {
                    const option = document.createElement('option');
                    option.value = district;
                    option.textContent = district;
                    districtSelect.appendChild(option);
                });
                districtSelect.disabled = false;
            }
        } catch (error) {
            console.error('Error loading districts:', error);
            showError('Error loading districts');
        }
    }
    
    districtSelect.disabled = !state;
    talukSelect.disabled = true;
    
    // Update weather information
    await updateLocationWeather();
}

async function loadTaluks() {
    const state = document.getElementById('state').value;
    const district = document.getElementById('district').value;
    const talukSelect = document.getElementById('taluk');
    
    talukSelect.innerHTML = '<option value="">Select Taluk</option>';
    
    if (district) {
        try {
            const response = await fetch(`/get-taluks/${state}/${district}`);
            const data = await response.json();
            
            if (data.success) {
                data.taluks.forEach(taluk => {
                    const option = document.createElement('option');
                    option.value = taluk;
                    option.textContent = taluk;
                    talukSelect.appendChild(option);
                });
                talukSelect.disabled = false;
            }
        } catch (error) {
            console.error('Error loading taluks:', error);
            showError('Error loading taluks');
        }
    }
    
    // Update weather information
    await updateLocationWeather();
}

async function updateLocationWeather() {
    const state = document.getElementById('state').value;
    const district = document.getElementById('district').value;
    
    if (state && district) {
        try {
            const response = await fetch(`/get-weather/${state}/${district}`);
            const data = await response.json();
            
            if (data.success) {
                updateWeatherInfo(data.weather);
            }
        } catch (error) {
            console.error('Error loading weather:', error);
        }
    }
}

async function analyzeDisease() {
    const state = document.getElementById('state').value;
    const district = document.getElementById('district').value;
    const cropType = document.getElementById('cropType').value;
    const imageFile = document.getElementById('diseaseImage').files[0];

    if (!state || !district || !cropType) {
        showError('Please select state, district, and crop type');
        return;
    }

    if (!imageFile) {
        showError('Please upload an image for disease analysis');
        return;
    }

    const formData = new FormData();
    formData.append('state', state);
    formData.append('district', district);
    formData.append('crop_type', cropType);
    formData.append('image', imageFile);

    try {
        const response = await fetch('/analyze-disease', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (data.success) {
            updateDiseaseAnalysis(data.analysis);
        } else {
            showError(data.error || 'Failed to analyze disease');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to connect to server');
    }
}

function validateRequiredFields() {
    const state = document.getElementById('state').value;
    const district = document.getElementById('district').value;
    const cropType = document.getElementById('cropType').value;
    const soilType = document.getElementById('soilType').value;
    const ph = document.getElementById('ph').value;
    const nitrogen = document.getElementById('nitrogen').value;
    const phosphorus = document.getElementById('phosphorus').value;
    const potassium = document.getElementById('potassium').value;
    const organicMatter = document.getElementById('organic_matter').value;

    if (!state || !district || !cropType || !soilType || !ph || !nitrogen || !phosphorus || !potassium || !organicMatter) {
        showError('Please fill in all required fields');
        return false;
    }
    return true;
}

function showError(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.innerHTML = `
        <i class="fas fa-exclamation-circle me-2"></i>${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the content
    const contentDiv = document.querySelector('.container');
    contentDiv.insertBefore(alertDiv, contentDiv.firstChild);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function updateWeatherInfo(weather) {
    const weatherInfo = document.getElementById('weatherInfo');
    if (!weather) {
        weatherInfo.innerHTML = '<div class="text-center text-muted"><i class="fas fa-info-circle me-2"></i>Weather information not available</div>';
        return;
    }

    weatherInfo.innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <div class="mb-3">
                    <strong>Temperature:</strong> ${weather.temperature.toFixed(1)}°C
                </div>
                <div class="mb-3">
                    <strong>Humidity:</strong> ${weather.humidity.toFixed(1)}%
                </div>
            </div>
            <div class="col-md-6">
                <div class="mb-3">
                    <strong>Season:</strong> ${weather.season.charAt(0).toUpperCase() + weather.season.slice(1)}
                </div>
            </div>
        </div>
    `;
}

function showSection(section) {
    // Update navigation active state
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    document.querySelector(`[onclick="showSection('${section}')"]`).classList.add('active');
    
    // Hide all sections first
    document.getElementById('soilSection').classList.add('d-none');
    document.getElementById('diseaseSection').classList.add('d-none');
    document.getElementById('predictionsSection').classList.add('d-none');
    document.getElementById('optimizationsSection').classList.add('d-none');
    document.getElementById('diseaseAnalysisSection').classList.add('d-none');
    
    // Hide all action buttons
    document.getElementById('predictBtn').classList.add('d-none');
    document.getElementById('optimizeBtn').classList.add('d-none');
    document.getElementById('analyzeBtn').classList.add('d-none');
    
    // Show relevant sections based on selection
    switch(section) {
        case 'predict':
            document.getElementById('soilSection').classList.remove('d-none');
            document.getElementById('predictionsSection').classList.remove('d-none');
            document.getElementById('predictBtn').classList.remove('d-none');
            break;
        case 'optimize':
            document.getElementById('soilSection').classList.remove('d-none');
            document.getElementById('optimizationsSection').classList.remove('d-none');
            document.getElementById('optimizeBtn').classList.remove('d-none');
            break;
        case 'disease':
            document.getElementById('diseaseSection').classList.remove('d-none');
            document.getElementById('diseaseAnalysisSection').classList.remove('d-none');
            document.getElementById('analyzeBtn').classList.remove('d-none');
            break;
    }
}

async function predictYield() {
    if (!validateRequiredFields()) return;
    
    const formData = {
        state: document.getElementById('state').value,
        district: document.getElementById('district').value,
        crop_type: document.getElementById('cropType').value,
        soil_type: document.getElementById('soilType').value,
        ph: parseFloat(document.getElementById('ph').value),
        nitrogen: parseFloat(document.getElementById('nitrogen').value),
        phosphorus: parseFloat(document.getElementById('phosphorus').value),
        potassium: parseFloat(document.getElementById('potassium').value),
        organic_matter: parseFloat(document.getElementById('organic_matter').value)
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        if (data.success) {
            updatePredictions(data.predictions);
        } else {
            showError(data.error || 'Failed to get predictions');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to connect to server');
    }
}

async function optimizeSoil() {
    if (!validateRequiredFields()) return;
    
    const formData = {
        state: document.getElementById('state').value,
        district: document.getElementById('district').value,
        crop_type: document.getElementById('cropType').value,
        soil_type: document.getElementById('soilType').value,
        ph: parseFloat(document.getElementById('ph').value),
        nitrogen: parseFloat(document.getElementById('nitrogen').value),
        phosphorus: parseFloat(document.getElementById('phosphorus').value),
        potassium: parseFloat(document.getElementById('potassium').value),
        organic_matter: parseFloat(document.getElementById('organic_matter').value)
    };

    try {
        const response = await fetch('/optimize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        if (data.success) {
            updateOptimizations(data.optimizations);
        } else {
            showError(data.error || 'Failed to get optimization recommendations');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to connect to server');
    }
}

function updatePredictions(predictions) {
    const predictionsDiv = document.getElementById('predictions');
    if (!predictions) {
        predictionsDiv.innerHTML = '<div class="alert alert-warning">No predictions available</div>';
        return;
    }

    let html = `
        <div class="alert alert-success">
            <h6 class="mb-3">Yield Predictions</h6>
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Estimated Yield:</strong> ${predictions.yield.toFixed(2)} kg/ha</p>
                    <p><strong>Confidence:</strong> ${(predictions.confidence * 100).toFixed(1)}%</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Season:</strong> ${predictions.season}</p>
                    <p><strong>Quality:</strong> ${predictions.quality}</p>
                </div>
            </div>
        </div>
    `;
    
    predictionsDiv.innerHTML = html;
}

function updateOptimizations(optimizations) {
    const optimizationsDiv = document.getElementById('optimizations');
    if (!optimizations) {
        optimizationsDiv.innerHTML = '<div class="alert alert-warning">No optimization recommendations available</div>';
        return;
    }

    let html = `
        <div class="alert alert-info">
            <h6 class="mb-3">Recommended Optimizations</h6>
            <div class="row">
                <div class="col-md-6">
                    <h6>Soil Nutrients</h6>
                    <p><strong>pH Level:</strong> ${optimizations.ph.recommended.toFixed(1)} (${optimizations.ph.action})</p>
                    <p><strong>Nitrogen:</strong> ${optimizations.nitrogen.recommended} kg/ha (${optimizations.nitrogen.action})</p>
                    <p><strong>Phosphorus:</strong> ${optimizations.phosphorus.recommended} kg/ha (${optimizations.phosphorus.action})</p>
                    <p><strong>Potassium:</strong> ${optimizations.potassium.recommended} kg/ha (${optimizations.potassium.action})</p>
                </div>
                <div class="col-md-6">
                    <h6>Additional Recommendations</h6>
                    <ul class="list-unstyled">
                        ${optimizations.recommendations.map(rec => `<li><i class="fas fa-check-circle text-success me-2"></i>${rec}</li>`).join('')}
                    </ul>
                </div>
            </div>
        </div>
    `;
    
    optimizationsDiv.innerHTML = html;
}

function updateDiseaseInfo(diseaseInfo) {
    const diseaseInfoDiv = document.getElementById('diseaseInfo');
    let html = '';
    
    for (const [crop, info] of Object.entries(diseaseInfo)) {
        if (Object.keys(info).length > 0) {
            html += `
                <div class="mb-4">
                    <h5 class="mb-3">${crop.charAt(0).toUpperCase() + crop.slice(1)}</h5>
                    
                    ${info.high_risk ? `
                        <div class="disease-alert mb-3">
                            <h6 class="mb-2"><i class="fas fa-exclamation-triangle me-2"></i>High Risk Alert</h6>
                            <p class="mb-0">Current weather conditions indicate high risk for diseases.</p>
                        </div>
                    ` : ''}
                    
                    <div class="mb-3">
                        <h6 class="mb-2">Potential Diseases:</h6>
                        <ul class="list-unstyled">
                            ${info.diseases.map(disease => `
                                <li><i class="fas fa-dot-circle me-2"></i>${disease}</li>
                            `).join('')}
                        </ul>
                    </div>
                    
                    <div class="optimization-tip">
                        <h6 class="mb-2"><i class="fas fa-lightbulb me-2"></i>Prevention & Optimization:</h6>
                        <ul class="list-unstyled mb-0">
                            ${info.prevention.map(tip => `
                                <li><i class="fas fa-check me-2"></i>${tip}</li>
                            `).join('')}
                        </ul>
                    </div>
                </div>
            `;
        }
    }
    
    diseaseInfoDiv.innerHTML = html || '<div class="text-center text-muted">No disease information available</div>';
}

function updateDiseaseAnalysis(analysis) {
    const diseaseDiv = document.getElementById('diseaseAnalysis');
    if (!analysis || Object.keys(analysis).length === 0) {
        diseaseDiv.innerHTML = '<div class="alert alert-warning">No diseases detected</div>';
        return;
    }

    let html = '<div class="alert alert-info"><h6 class="mb-3">Disease Analysis Results</h6>';

    // Sort diseases by probability
    const diseases = Object.entries(analysis).sort((a, b) => b[1].probability - a[1].probability);

    for (const [disease, info] of diseases) {
        const probability = (info.probability * 100).toFixed(1);
        const severityClass = probability > 70 ? 'danger' : (probability > 40 ? 'warning' : 'success');

        html += `
            <div class="disease-card mb-3">
                <h6 class="text-${severityClass}">
                    ${disease.replace(/_/g, ' ').toUpperCase()}
                    <span class="badge bg-${severityClass} ms-2">${probability}%</span>
                </h6>
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Symptoms:</strong></p>
                        <ul>
                            ${info.symptoms.map(s => `<li>${s}</li>`).join('')}
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Treatment:</strong></p>
                        <ul>
                            ${info.treatment.map(t => `<li>${t}</li>`).join('')}
                        </ul>
                    </div>
                </div>
                <div class="mt-2">
                    <p><strong>Prevention:</strong></p>
                    <ul>
                        ${info.prevention.map(p => `<li>${p}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
    }

    html += '</div>';
    diseaseDiv.innerHTML = html;
}
