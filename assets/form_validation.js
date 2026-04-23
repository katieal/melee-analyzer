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
            const infoForm = document.getElementById('add-tournament-info-form')
            const websiteForm = document.getElementById('add-tournament-website-form')
            const bracketForm = document.getElementById('add-tournament-bracket-form')

            // Listener for Info form
            infoForm.addEventListener('submit', event => {
                event.preventDefault()
                // if form is not valid
                if (!infoForm.checkValidity()) {
                    // show error fields
                    infoForm.classList.add('was-validated')
                    // show form submission error alert
                    dash_clientside.set_props('invalid-form-alert', {is_open: true})

                    event.stopPropagation()
                    return dash_clientside.no_update;
                }
                else { // if form submission is valid
                    // make form data object for form
                    let formData = new FormData(infoForm);
                    // store data in dcc.store
                    storeFormData('info', formData)
                }
            }, false)

            // Listener for Website form
            websiteForm.addEventListener('submit', event => {
                event.preventDefault()
                // if form is not valid
                if (!websiteForm.checkValidity()) {
                    // show error fields
                    websiteForm.classList.add('was-validated')
                    // show form submission error alert
                    dash_clientside.set_props('invalid-form-alert', {is_open: true})

                    event.stopPropagation()
                    return dash_clientside.no_update;
                }
                else { // if form submission is valid
                    // store data in dcc.store
                    storeFormData('website', new FormData(websiteForm));
                }
            }, false)

            // Listener for Bracket form
            bracketForm.addEventListener('submit', event => {
                event.preventDefault()
                // if form is not valid
                if (!bracketForm.checkValidity()) {
                    // show error fields
                    bracketForm.classList.add('was-validated')
                    // show form submission error alert
                    dash_clientside.set_props('invalid-form-alert', {is_open: true})

                    event.stopPropagation()
                    return dash_clientside.no_update;
                }
                else { // if form submission is valid
                    // store data in dcc.store
                    storeFormData('bracket', new FormData(bracketForm));
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

function storeFormData(formName, formData) {
    // build a dict with form data
    const data = {}

    for (const entry of formData.entries()) {
        data[entry[0]] = entry[1]
    }
    //data['completed_forms'][formName] = true

    //const data = new Map();
    //for (const entry of formData.entries()) {
    //    data.set(entry[0], entry[1])
    //}


    //console.log(data)

    // save new data to 'submitted_data' key in form store
    const patch = new dash_clientside.Patch;
    //patch.merge(['submitted_data'], data);
    patch.merge([], data);
    dash_clientside.set_props('form-store', {data: patch.build()});
}