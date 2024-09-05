document.addEventListener("DOMContentLoaded", function() {
    const testimonialsContainer = document.querySelector('.testimonials.container');

    fetch('testimonials.html')
        .then(response => response.text())
        .then(data => {
            testimonialsContainer.innerHTML += data;
        })
        .catch(error => console.error('Error loading testimonials:', error));
});
