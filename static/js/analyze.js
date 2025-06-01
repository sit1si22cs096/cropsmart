// Initialize event listeners when the document is ready
document.addEventListener('DOMContentLoaded', function() {
    const analyzeForm = document.getElementById('analyzeForm');
    const imageInput = document.getElementById('image');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');

    // Add event listener for image input change
    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            // Show preview
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                previewContainer.style.display = 'block';
            };
            reader.readAsDataURL(file);
        } else {
            previewContainer.style.display = 'none';
        }
    });

    // Add event listener for form submission
    analyzeForm.addEventListener('submit', function(e) {
        e.preventDefault();
        analyzeDisease();
    });
});

// Function to analyze disease
async function analyzeDisease() {
    const cropType = document.getElementById('cropType').value;
    const imageInput = document.getElementById('image');
    
    if (!cropType || !imageInput.files[0]) {
        showToast('Please select a crop type and upload an image', 'error');
        return;
    }

    // Create form data
    const formData = new FormData();
    formData.append('crop_type', cropType);
    formData.append('image', imageInput.files[0]);

    try {
        const response = await fetch('/api/analyze-disease', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to analyze disease');
        }

        const result = await response.json();
        displayResults(result);
        showToast('Analysis completed successfully', 'success');
    } catch (error) {
        console.error('Error:', error);
        showToast(error.message || 'Error analyzing disease. Please try again.', 'error');
    }
}

// Function to display analysis results
function displayResults(data) {
    const resultsCard = document.getElementById('resultsCard');
    const resultsDiv = document.getElementById('analysisResults');
    
    if (!resultsCard || !resultsDiv) {
        console.error('Results elements not found');
        return;
    }

    // Show the results card
    resultsCard.style.display = 'block';
    
    // Format the results
    let resultsHTML = `
        <div class="alert alert-info mb-4">
            <h5 class="alert-heading">Disease Identified</h5>
            <p class="mb-0">Based on the uploaded image analysis</p>
        </div>
        
        <div class="row">
            <div class="col-md-6 mb-4">
                <div class="card h-100">
                    <div class="card-body">
                        <h6 class="card-title">Disease Name</h6>
                        <p class="mb-1">${data.disease_name}</p>
                        <small class="text-muted">${data.scientific_name}</small>
                    </div>
                </div>
            </div>
            <div class="col-md-6 mb-4">
                <div class="card h-100">
                    <div class="card-body">
                        <h6 class="card-title">Confidence</h6>
                        <div class="progress">
                            <div class="progress-bar bg-${getConfidenceColor(data.confidence)}" 
                                role="progressbar" 
                                style="width: ${data.confidence}%" 
                                aria-valuenow="${data.confidence}" 
                                aria-valuemin="0" 
                                aria-valuemax="100">
                                ${data.confidence}%
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    if (data.symptoms && data.symptoms.length > 0) {
        resultsHTML += `
            <h6 class="mb-3">Symptoms</h6>
            <ul class="list-group list-group-flush mb-4">
                ${data.symptoms.map(symptom => `<li class="list-group-item">${symptom}</li>`).join('')}
            </ul>
        `;
    }

    if (data.treatment && data.treatment.length > 0) {
        resultsHTML += `
            <h6 class="mb-3">Treatment Recommendations</h6>
            <ul class="list-group list-group-flush mb-4">
                ${data.treatment.map(step => `<li class="list-group-item">${step}</li>`).join('')}
            </ul>
        `;
    }
    
    resultsDiv.innerHTML = resultsHTML;
    
    // Scroll to results
    resultsCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Helper function to get color class based on confidence
function getConfidenceColor(confidence) {
    if (confidence >= 80) return 'success';
    if (confidence >= 60) return 'info';
    if (confidence >= 40) return 'warning';
    return 'danger';
}

// Function to show toast notifications
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastBody = toast?.querySelector('.toast-body');
    
    if (!toast || !toastBody) {
        console.error('Toast elements not found');
        return;
    }

    // Reset classes
    toast.className = 'toast';
    
    // Add appropriate class based on type
    const classes = {
        'success': 'bg-success text-white',
        'error': 'bg-danger text-white',
        'warning': 'bg-warning',
        'info': 'bg-info text-white'
    };
    
    toast.classList.add(...(classes[type] || classes.info).split(' '));
    toastBody.textContent = message;
    
    // Show toast
    const bsToast = new bootstrap.Toast(toast, {
        animation: true,
        autohide: true,
        delay: 5000
    });
    bsToast.show();
}
