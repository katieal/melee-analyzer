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
            const form = document.getElementById("test-form-html")

            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()

                    form.classList.add('was-validated')

                    return dash_clientside.no_update;
                }

                // logic for valid form submissions goes here

            }, false)
            return dash_clientside.no_update;
        }
    }
})

/*
    function event listener:
    check if form is valid
        if NOT:
            event.PREVENTDEFAULT
            no update, etc
    if form is valid
        allow default to execute

https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Sending_forms_through_JavaScript

 */
