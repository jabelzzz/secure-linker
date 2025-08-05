
//Hide div when link is generated
document.addEventListener("DOMContentLoaded", function() {
    const resultContainer = document.querySelector('.result-container');
    if (resultContainer) {
        resultContainer.style.display = 'none';
    }

    // Show the result container when a link is generated

    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        document.getElementById("form-container").hidden = true;
        event.preventDefault(); // Prevent the default form submission
        resultContainer.style.display = 'block'; // Show the result container
    });
});
