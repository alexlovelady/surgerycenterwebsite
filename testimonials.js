document.addEventListener("DOMContentLoaded", function() {
    // Select the container where testimonials should be loaded
    const testimonialsContainer = document.querySelector('.testimonials.container');

    // Load the testimonials from the external HTML file
    fetch('testimonials.html')
        .then(response => response.text())
        .then(data => {
            testimonialsContainer.innerHTML += data; // Append the loaded testimonials to the container
        })
        .catch(error => console.error('Error loading testimonials:', error));
});
