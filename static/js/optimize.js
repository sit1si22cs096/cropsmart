document.addEventListener('DOMContentLoaded', function() {
    const stateSelect = document.getElementById('state');
    const seasonSelect = document.getElementById('season');
    const cropSelect = document.getElementById('crop');
    const optimizeForm = document.getElementById('optimizeForm');
    const resultsDiv = document.getElementById('results');
    const toast = document.getElementById('toast');
    const toastBody = document.getElementById('toastBody');

    function showToast(message, type = 'error') {
        if (toast && toastBody) {
            toast.classList.remove('bg-success', 'bg-danger', 'text-white');
            toast.classList.add(`bg-${type === 'error' ? 'danger' : 'success'}`, 'text-white');
            toastBody.textContent = message;
            const bsToast = new bootstrap.Toast(toast);
            bsToast.show();
        }
    }

    function showLoadingIndicator(show) {
        const submitButton = optimizeForm.querySelector('button[type="submit"]');
        if (submitButton) {
            if (show) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
            } else {
                submitButton.disabled = false;
                submitButton.innerHTML = '<i class="fas fa-search me-2"></i>Get Crop Recommendations';
            }
        }
    }

    function displayOptimizationResults(data) {
        let html = '<div class="card shadow-sm mt-4"><div class="card-body">';
        html += '<h3 class="card-title">Optimization Results</h3>';
        
        if (data.recommendations && data.recommendations.length > 0) {
            data.recommendations.forEach((rec) => {
                html += `
                    <div class="alert alert-success">
                        <h4 class="alert-heading">${rec.crop}</h4>
                        <p><strong>Season:</strong> ${rec.season}</p>
                        <p><strong>Expected Yield:</strong> ${rec.expected_yield} tons</p>
                        <p><strong>Yield Stability:</strong> ${rec.yield_stability}%</p>
                        
                        <h5 class="mt-3">Requirements:</h5>
                        <ul>
                            <li>Area: ${rec.requirements.area}</li>
                            <li>Fertilizer: ${rec.requirements.fertilizer}</li>
                            <li>Pesticide: ${rec.requirements.pesticide}</li>
                            <li>Rainfall: ${rec.requirements.rainfall}</li>
                        </ul>
                        
                        <h5 class="mt-3">Optimization Tips:</h5>
                        <ul>
                            ${rec.optimization_tips.map(tip => `<li>${tip}</li>`).join('')}
                        </ul>
                    </div>`;
            });
        } else {
            html += '<div class="alert alert-warning">No recommendations available.</div>';
        }
        
        html += '</div></div>';
        if (resultsDiv) {
            resultsDiv.innerHTML = html;
            showToast('Recommendations generated successfully!', 'success');
        }
    }

    // Update crops when state or season changes
    async function updateCrops() {
        const state = stateSelect.value;
        const season = seasonSelect.value;
        
        // Clear and disable crop select
        if (cropSelect) {
            cropSelect.innerHTML = '<option value="">Select Crop</option>';
            cropSelect.disabled = true;
        }
        
        if (!state || !season) {
            showToast('Please select both state and season first', 'error');
            return;
        }
        
        try {
            showLoadingIndicator(true);
            const response = await fetch(`/get_crops?state=${encodeURIComponent(state)}&season=${encodeURIComponent(season)}`);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Failed to fetch crops');
            }
            
            if (Array.isArray(data)) {
                if (data.length > 0) {
                    // Sort crops alphabetically
                    data.sort((a, b) => a.localeCompare(b));
                    
                    // Add options to select
                    data.forEach(crop => {
                        const option = document.createElement('option');
                        option.value = crop;
                        option.textContent = crop;
                        cropSelect.appendChild(option);
                    });
                    cropSelect.disabled = false;
                    showToast(`Found ${data.length} crops for ${state} in ${season} season`, 'success');
                } else {
                    showToast('No crops available for selected state and season', 'error');
                }
            }
        } catch (error) {
            console.error('Error fetching crops:', error);
            showToast(error.message, 'error');
        } finally {
            showLoadingIndicator(false);
        }
    }

    // Event listeners for state and season changes
    stateSelect.addEventListener('change', function() {
        cropSelect.innerHTML = '<option value="">Select Crop</option>';
        cropSelect.disabled = true;
        if (this.value) {
            updateCrops();
        }
    });

    seasonSelect.addEventListener('change', function() {
        cropSelect.innerHTML = '<option value="">Select Crop</option>';
        cropSelect.disabled = true;
        if (this.value) {
            updateCrops();
        }
    });

    // Function to handle optimization form submission
    async function handleOptimizeFormSubmit(event) {
        event.preventDefault();
        // Validate input fields
        const inputData = {
            state: document.getElementById('state').value,
            season: document.getElementById('season').value,
            crop: document.getElementById('crop').value,
            area: parseFloat(document.getElementById('area').value),
            rainfall: parseFloat(document.getElementById('rainfall').value),
            fertilizer: parseFloat(document.getElementById('fertilizer').value),
            pesticide: parseFloat(document.getElementById('pesticide').value),
        };
        // Show loading indicator
        showLoadingIndicator(true);
        try {
            const response = await fetch('/api/optimize', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(inputData),
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Optimization failed');
            displayOptimizationResults(data);
        } catch (error) {
            console.error('Error during optimization:', error);
            showToast('Error during optimization: ' + error.message);
        } finally {
            showLoadingIndicator(false);
        }
    }

    optimizeForm.addEventListener('submit', handleOptimizeFormSubmit);
});