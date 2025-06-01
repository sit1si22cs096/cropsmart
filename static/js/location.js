document.addEventListener("DOMContentLoaded", () => {
    const stateDropdown = document.getElementById("state");
    const districtDropdown = document.getElementById("district");
    const talukDropdown = document.getElementById("taluk");

    // Load States
    fetch("/api/states")
        .then(response => response.json())
        .then(data => {
            stateDropdown.innerHTML = '<option value="">Select State</option>';
            data.forEach(state => {
                stateDropdown.innerHTML += `<option value="${state}">${state}</option>`;
            });
            stateDropdown.disabled = false;
        })
        .catch(err => console.error("Error loading states:", err));

    // Load Districts
    stateDropdown.addEventListener("change", () => {
        const selectedState = stateDropdown.value;
        districtDropdown.innerHTML = '<option value="">Select District</option>';
        talukDropdown.innerHTML = '<option value="">Select Taluk</option>';
        districtDropdown.disabled = true;
        talukDropdown.disabled = true;

        if (selectedState) {
            fetch(`/get-districts/${selectedState}`)
                .then(response => response.json())
                .then(data => {
                    data.forEach(district => {
                        districtDropdown.innerHTML += `<option value="${district}">${district}</option>`;
                    });
                    districtDropdown.disabled = false;
                })
                .catch(err => console.error("Error loading districts:", err));
        }
    });

    // Load Taluks
    districtDropdown.addEventListener("change", () => {
        const selectedState = stateDropdown.value;
        const selectedDistrict = districtDropdown.value;
        talukDropdown.innerHTML = '<option value="">Select Taluk</option>';
        talukDropdown.disabled = true;

        if (selectedState && selectedDistrict) {
            fetch(`/get-taluks/${selectedState}/${selectedDistrict}`)
                .then(response => response.json())
                .then(data => {
                    data.forEach(taluk => {
                        talukDropdown.innerHTML += `<option value="${taluk}">${taluk}</option>`;
                    });
                    talukDropdown.disabled = false;
                })
                .catch(err => console.error("Error loading taluks:", err));
        }
    });
});
