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
        validate_info_form: function() {
            const form = document.getElementById('add-tournament-info-form')

            form.addEventListener('submit', event => {
                // if form is not valid
                if (!form.checkValidity()) {
                    // show error fields
                    form.classList.add('was-validated')
                    // show form submission error alert
                    dash_clientside.set_props('invalid-form-alert', {is_open: true})

                    event.preventDefault()
                    event.stopPropagation()
                    return dash_clientside.no_update;
                }
                else {
                    // logic for valid form submissions goes here
                    // make formdata object for form
                    const formData = new FormData(form);
                    sendFormDataAsync(formData, '/add-tournament/submit-info');

                    event.preventDefault()
                    event.stopPropagation()
                    //return dash_clientside.no_update;
                }
            }, false)
            return dash_clientside.no_update;
        },
        clear_validation: function(clicks) {
            const form = document.getElementById('add-tournament-form')
            form.classList.remove('was-validated')
        }
    }
})

async function sendFormDataAsync(formData, url) {
    // send data to endpoint
    try {
        const response = await fetch(url, {
           method: "POST",
           body: formData,
        });
        console.log(await response.json());
    } catch(e) {
        console.error(e);
    }
}