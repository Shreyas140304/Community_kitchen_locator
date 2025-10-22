const links = document.querySelectorAll('.sidebar a');
const sections = document.querySelectorAll('.content-section');

links.forEach(link => {
    link.addEventListener('click', function(e) {
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

// function openEditKitchenModal(id) {
//     document.getElementById("editKitchenModal").style.display = "flex";

//     // Fetch data from Flask backend using the ID
//     fetch(`/get_kitchen/${id}`)
//         .then(response => response.json())
//         .then(data => {
//             // Fill form fields
//             document.getElementById("edit-id").value = data.id;
//             document.getElementById("edit-kitchen-name").value = data.kitchen_name;
//             document.getElementById("edit-address").value = data.address;
//             document.getElementById("edit-zip").value = data.zip_code;
//             document.getElementById("edit-service-area").value = data.service_area;
//             document.getElementById("edit-contact-person").value = data.contact_person;
//             document.getElementById("edit-contact-phone").value = data.contact_phone;
//             document.getElementById("edit-contact-email").value = data.contact_email;
//             document.getElementById("edit-directions").value = data.directions;
//             // You can continue for remaining fields similarly
//         });
// }

// function closeEditKitchenModal() {
//     document.getElementById("editKitchenModal").style.display = "none";
// }

// window.onclick = function(event) {
//     if (event.target == document.getElementById("editKitchenModal")) {
//         closeEditKitchenModal();
//     }
// }

// // Handle form submission
// document.getElementById("edit-kitchen-form").addEventListener("submit", function(e) {
//     e.preventDefault();

//     const formData = new FormData(this);

//     fetch('/update_kitchen', {
//         method: 'POST',
//         body: formData
//     }).then(response => {
//         if (response.ok) {
//             alert("Kitchen updated successfully!");
//             closeEditKitchenModal();
//             location.reload();
//         } else {
//             alert("Error updating kitchen");
//         }
//     });
// });

