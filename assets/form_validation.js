/*
function updateButton() {
    const text = prompt("Enter text");
    button.textContent = `You Entered: ${text}`;
}

const button = document.getElementById("javascript-button");

button.addEventListener("click", updateButton);
*/


window.dash_clientside = Object.assign({}, window.dash_clientside, {
    formValidation: {
        validate_form: function() {
            const form = document.getElementById('add-tournament-form')

            form.addEventListener('submit', event => {
                // prevent default event
                event.preventDefault()

                // if form is not valid
                if (!form.checkValidity()) {
                    event.stopPropagation()
                    // show error fields
                    form.classList.add('was-validated')

                    return dash_clientside.no_update;
                }
                else {
                    // logic for valid form submissions goes here
                    // make formdata object for form
                    const formData = new FormData(form);
                    sendFormDataAsync(formData);
                }
            }, false)
            return dash_clientside.no_update;
        }
    }
})

async function sendFormDataAsync(formData) {
    // send data to endpoint
    try {
        const response = await fetch('/add-tournament/submit', {
           method: "POST",
           body: formData,
        });
        console.log(await response.json());
    } catch(e) {
        console.error(e);
    }
}