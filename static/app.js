// Separate JavaScript code

function handleUploadForm() {
    var form = document.getElementById('upload-form');
    var formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        showMessage(data.message, data.status);
        if (data.status === 'success') {
            form.reset();
        }
    })
    .catch(error => showMessage('An error occurred while processing the request.', 'error'));
}

function showMessage(message, status) {
    var modal = document.getElementById('message-modal');
    var messageText = document.getElementById('message-text');

    messageText.innerHTML = message;

    // Reset modal classes and add appropriate status class
    modal.className = 'modal';
    modal.classList.add(status);

    modal.style.display = 'block';
}

function closeModal() {
    var modal = document.getElementById('message-modal');
    modal.style.display = 'none';
}

document.getElementById('upload-form').addEventListener('click', function () {
    document.body.classList.add('celebrate');

    // Create and append a flower element to the body
    const flower = document.createElement('div');
    flower.className = 'flower';
    flower.style.left = Math.random() * window.innerWidth + 'px';
    flower.style.top = Math.random() * window.innerHeight + 'px';
    document.body.appendChild(flower);

    // Remove the flower element after the bloom animation
    setTimeout(function () {
        flower.remove();
    }, 1000); // Adjust the time to match the duration of the celebration animation
});
