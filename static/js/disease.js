// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('diseaseForm');
    const dropZone = document.getElementById('dropZone');
    const imageInput = document.getElementById('image');
    const imagePreview = document.getElementById('imagePreview');
    const preview = document.getElementById('preview');

    // Handle drag and drop
    if (dropZone) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });

        function highlight(e) {
            dropZone.classList.add('drop-zone-active');
        }

        function unhighlight(e) {
            dropZone.classList.remove('drop-zone-active');
        }

        dropZone.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            handleFiles(files);
        }
    }

    // Handle file selection
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            handleFiles(this.files);
        });
    }

    function handleFiles(files) {
        if (files.length === 0) return;

        const file = files[0];
        if (!file.type.startsWith('image/')) {
            showToast('Please upload an image file', 'error');
            return;
        }

        // Show image preview
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            imagePreview.style.display = 'block';
            dropZone.querySelector('.drop-zone-prompt').style.display = 'none';
        };
        reader.readAsDataURL(file);
    }

    // Handle form submission
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();

            if (!form.checkValidity()) {
                e.stopPropagation();
                form.classList.add('was-validated');
                return;
            }

            const formData = new FormData();
            formData.append('image', imageInput.files[0]);
            formData.append('crop_type', document.getElementById('cropType').value);
            formData.append('state', document.getElementById('state').value);
            formData.append('district', document.getElementById('district').value);
            formData.append('taluk', document.getElementById('taluk').value);

            try {
                const response = await fetch('/analyze_disease', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    displayResults(data);
                    showToast('Analysis completed successfully', 'success');
                } else {
                    showToast(data.error || 'An error occurred during analysis', 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                showToast('An error occurred while communicating with the server', 'error');
            }
        });
    }
});

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    const resultsContent = document.getElementById('resultsContent');
    
    if (!resultsDiv || !resultsContent) return;

    let html = `
        <div class="alert alert-${data.severity === 'high' ? 'danger' : data.severity === 'medium' ? 'warning' : 'info'} mb-4">
            <h5 class="alert-heading">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Detected Disease: ${data.disease}
            </h5>
            <p class="mb-0">Severity Level: ${data.severity.toUpperCase()}</p>
        </div>

        <div class="row">
            <div class="col-md-6 mb-3">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">
                            <i class="fas fa-medkit text-danger me-2"></i>
                            Treatment Recommendations
                        </h5>
                        <ul class="list-unstyled mb-0">
                            ${data.treatments.map(treatment => `
                                <li class="mb-2">
                                    <i class="fas fa-check text-success me-2"></i>
                                    ${treatment}
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6 mb-3">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">
                            <i class="fas fa-shield-alt text-primary me-2"></i>
                            Prevention Measures
                        </h5>
                        <ul class="list-unstyled mb-0">
                            ${data.prevention.map(measure => `
                                <li class="mb-2">
                                    <i class="fas fa-check text-success me-2"></i>
                                    ${measure}
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    `;

    resultsContent.innerHTML = html;
    resultsDiv.style.display = 'block';
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function loadStates() {
    fetch('/get-states')
        .then(response => response.json())
        .then(data => {
            const stateSelect = document.getElementById('state');
            stateSelect.innerHTML = '<option value="">Select State</option>';
            data.states.forEach(state => {
                const option = document.createElement('option');
                option.value = state;
                option.textContent = state;
                stateSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error loading states:', error);
            showToast('Error loading states', 'error');
        });
}

function loadDistricts() {
    const state = document.getElementById('state').value;
    const districtSelect = document.getElementById('district');
    const talukSelect = document.getElementById('taluk');
    
    districtSelect.disabled = !state;
    talukSelect.disabled = true;
    
    if (state) {
        fetch(`/get-districts/${state}`)
            .then(response => response.json())
            .then(data => {
                districtSelect.innerHTML = '<option value="">Select District</option>';
                data.districts.forEach(district => {
                    const option = document.createElement('option');
                    option.value = district;
                    option.textContent = district;
                    districtSelect.appendChild(option);
                });
                districtSelect.disabled = false;
            })
            .catch(error => {
                console.error('Error loading districts:', error);
                showToast('Error loading districts', 'error');
            });
    }
}

function loadTaluks() {
    const state = document.getElementById('state').value;
    const district = document.getElementById('district').value;
    const talukSelect = document.getElementById('taluk');
    
    talukSelect.disabled = !district;
    
    if (state && district) {
        fetch(`/get-taluks/${state}/${district}`)
            .then(response => response.json())
            .then(data => {
                talukSelect.innerHTML = '<option value="">Select Taluk</option>';
                data.taluks.forEach(taluk => {
                    const option = document.createElement('option');
                    option.value = taluk;
                    option.textContent = taluk;
                    talukSelect.appendChild(option);
                });
                talukSelect.disabled = false;
            })
            .catch(error => {
                console.error('Error loading taluks:', error);
                showToast('Error loading taluks', 'error');
            });
    }
}

function setupImageUpload() {
    const imageUpload = document.getElementById('imageUpload');
    const imagePreview = document.getElementById('imagePreview');
    const noPreview = document.getElementById('noPreview');
    const uploadIcon = document.getElementById('uploadIcon');
    const dropZone = document.getElementById('dropZone');

    // Handle drag and drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleImageSelection(e.dataTransfer.files[0]);
        }
    });

    // Handle file input change
    imageUpload.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            handleImageSelection(this.files[0]);
        }
    });
}

function handleImageSelection(file) {
    const imagePreview = document.getElementById('imagePreview');
    const noPreview = document.getElementById('noPreview');
    const reader = new FileReader();
    
    reader.onload = function(e) {
        imagePreview.src = e.target.result;
        imagePreview.classList.remove('d-none');
        noPreview.classList.add('d-none');
    }
    
    reader.readAsDataURL(file);
}

async function analyzeDisease() {
    if (!validateForm()) {
        return;
    }

    const imageUpload = document.getElementById('imageUpload');
    const state = document.getElementById('state').value;
    const district = document.getElementById('district').value;
    const taluk = document.getElementById('taluk').value;
    const cropType = document.getElementById('cropType').value;

    if (!imageUpload.files || !imageUpload.files[0]) {
        showToast('Please select an image to analyze', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('image', imageUpload.files[0]);
    formData.append('state', state);
    formData.append('district', district);
    formData.append('taluk', taluk);
    formData.append('crop_type', cropType);

    try {
        const response = await fetch('/analyze_disease', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const analysis = await response.json();
        console.log(analysis); // Log the response data
        displayAnalysisResults(analysis);
        showToast('Analysis completed successfully', 'success');
    } catch (error) {
        console.error('Error:', error);
        showToast('Error analyzing disease: ' + error.message, 'error');
    }
}

function displayAnalysisResults(analysis) {
    const resultsContainer = document.getElementById('analysisResults');
    
    if (!analysis.success) {
        resultsContainer.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-circle me-2"></i>
                ${analysis.error || 'An error occurred during analysis'}
            </div>
        `;
        return;
    }

    const disease = analysis.disease;
    const severity = analysis.severity || 'medium';
    const treatments = analysis.treatments || [];
    const prevention = analysis.prevention || [];

    let html = `
        <div class="mb-4">
            <div class="d-flex align-items-center mb-3">
                <div class="treatment-number bg-${getSeverityClass(severity)} me-3">
                    <i class="fas fa-bug"></i>
                </div>
                <div>
                    <h5 class="mb-1">Disease Detected</h5>
                    <p class="mb-0 text-capitalize">${disease}</p>
                </div>
            </div>
            <div class="progress mb-2" style="height: 10px;">
                <div class="progress-bar bg-${getSeverityClass(severity)}" 
                     role="progressbar" 
                     style="width: ${getSeverityPercentage(severity)}%" 
                     aria-valuenow="${getSeverityPercentage(severity)}" 
                     aria-valuemin="0" 
                     aria-valuemax="100">
                </div>
            </div>
            <p class="text-muted mb-0">
                Severity Level: <span class="text-${getSeverityClass(severity)} text-capitalize">${severity}</span>
            </p>
        </div>
    `;

    // Treatments Section
    if (treatments.length > 0) {
        html += `
            <div class="mb-4">
                <h5 class="mb-3">
                    <i class="fas fa-prescription-bottle-alt text-primary me-2"></i>
                    Recommended Treatments
                </h5>
                <div class="timeline">
        `;

        treatments.forEach((treatment, index) => {
            html += `
                <div class="timeline-item">
                    <div class="timeline-marker bg-primary"></div>
                    <div class="timeline-content">
                        <h6 class="mb-2">Step ${index + 1}</h6>
                        <p class="mb-0">${treatment}</p>
                    </div>
                </div>
            `;
        });

        html += `
                </div>
            </div>
        `;
    }

    // Prevention Section
    if (prevention.length > 0) {
        html += `
            <div class="mb-4">
                <h5 class="mb-3">
                    <i class="fas fa-shield-alt text-success me-2"></i>
                    Prevention Tips
                </h5>
                <ul class="list-group list-group-flush">
        `;

        prevention.forEach(tip => {
            html += `
                <li class="list-group-item">
                    <i class="fas fa-check text-success me-2"></i>
                    ${tip}
                </li>
            `;
        });

        html += `
                </ul>
            </div>
        `;
    }

    resultsContainer.innerHTML = html;
}

function getSeverityClass(severity) {
    switch (severity.toLowerCase()) {
        case 'low':
            return 'success';
        case 'medium':
            return 'warning';
        case 'high':
            return 'danger';
        default:
            return 'primary';
    }
}

function getSeverityPercentage(severity) {
    switch (severity.toLowerCase()) {
        case 'low':
            return 33;
        case 'medium':
            return 66;
        case 'high':
            return 100;
        default:
            return 50;
    }
}

function validateForm() {
    const state = document.getElementById('state').value;
    const district = document.getElementById('district').value;
    const taluk = document.getElementById('taluk').value;
    const cropType = document.getElementById('cropType').value;

    if (!state || !district || !taluk || !cropType) {
        showToast('Please fill in all location and crop details', 'error');
        return false;
    }

    return true;
}

function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}
