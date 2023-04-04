const form = document.getElementById("contact-form")
const submitFormBtn = document.getElementById('submit-form-btn')
const spinner = document.getElementById('spinner')

spinner.style.display = 'none'

function onSubmit(token) {
    const e = window.event
    if (form.checkValidity()) {
        // Display a spinner while the message is being sent back to the server
        submitFormBtn.style.display = "none";
        spinner.style.display = "block";
        form.submit();
    } else {
        e.preventDefault()
        e.stopPropagation()
    }
    form.classList.add('was-validated');
}