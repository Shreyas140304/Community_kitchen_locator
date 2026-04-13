const links = document.querySelectorAll('.sidebar a');
const sections = document.querySelectorAll('.content-section');

links.forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault();

        // Remove active class from all links
        links.forEach(l => l.classList.remove('active'));
        // Add active class to clicked link
        this.classList.add('active');

        const page = this.dataset.page;

        // Hide all sections
        sections.forEach(section => section.classList.remove('active'));
        // Show the selected section
        document.getElementById(page).classList.add('active');
    });
});



// accessing data for edit-kitchen

function openEditKitchenModal(id) {
    document.getElementById("editKitchenModal").style.display = "flex";

    // Fetch data from Flask backend using the ID
    fetch(`/get_kitchen/${id}`)
        .then(response => response.json())
        .then(data => {
            // Fill form fields
            document.getElementById("edit-id").value = data.id;
            document.getElementById("edit-kitchen-name").value = data.kitchen_name;
            document.getElementById("edit-address").value = data.address;
            document.getElementById("edit-zip").value = data.zip;
            document.getElementById("edit-service-area").value = data.service_area;
            document.getElementById("edit-contact-person").value = data.contact_Name;
            document.getElementById("edit-contact-phone").value = data.phone_num;
            document.getElementById("edit-contact-email").value = data.contact_email;
            document.getElementById("edit-directions").value = data.directions;
            document.getElementById("edit-days").value = data.days;
            document.getElementById("edit-meal-time").value = data.meal_time;
            document.getElementById("edit-frequency").value = data.frequency;
            document.getElementById("edit-special-hours").value = data.special_hours;
            document.getElementById("edit-meal-types").value = data.meal_types;
            document.getElementById("edit-audience").value = data.audience;
            document.getElementById("edit-capacity").value = data.capacity;
            document.getElementById("edit-sts").value = data.sts.toLowerCase();

            // ✅ Handle multi-value checkboxes: meal_types
            const mealTypes = JSON.parse(data.meal_types || '[]');
            document.querySelectorAll('input[name="meal_types"]').forEach(input => {
                input.checked = mealTypes.includes(input.value);
            });

            // ✅ Handle multi-value checkboxes: audience
            const audience = JSON.parse(data.audience || '[]');
            document.querySelectorAll('input[name="audience"]').forEach(input => {
                input.checked = audience.includes(input.value);
            });

            const days = JSON.parse(data.days || '[]');
            document.querySelectorAll('input[name="days"]').forEach(input => {
                input.checked = days.includes(input.value);
            });
        });
}

function closeEditKitchenModal() {
    document.getElementById("editKitchenModal").style.display = "none";
}

window.onclick = function (event) {
    if (event.target == document.getElementById("editKitchenModal")) {
        closeEditKitchenModal();
    }
}

// Handle form submission
document.getElementById("edit-kitchen-form").addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    fetch('/edit_kitchen', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            alert("Kitchen updated successfully!");
            closeEditKitchenModal();
            location.reload();
        } else {
            alert("Error updating kitchen");
        }
    });
});