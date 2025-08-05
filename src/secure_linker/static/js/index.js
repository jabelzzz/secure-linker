// Hide content container when link is generated
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        document.getElementById("content-container").hidden = true;
        document.getElementById("token-container").hidden = false;
        event.preventDefault(); // Prevent the default form submission
    });
});
