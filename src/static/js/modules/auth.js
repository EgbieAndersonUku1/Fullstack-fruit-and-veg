import PasswordStrengthChecker from "../utils/password.js";
import fetchData from "../utils/fetch.js";

// DOM Elements for Authentication
const loginAuthenticationContainer    = document.querySelector(".login");
const registerAuthenticationContainer = document.querySelector(".register");
const loginLinkElement                = document.getElementById("login");
const registerLinkElement             = document.getElementById("register-link");

// DOM Elements for Closing Windows
const closeLoginIconElement           = document.querySelector(".auth-close-icon");
const closeRegistrationIconElement    = document.getElementById("reg-close-icon");

// DOM Elements for Password Management
const passwordElement                 = document.getElementById("register-password");
const confirmPasswordElement          = document.getElementById("register-confirm-password");

// DOM Elements for Password Strength Indicators
const hasCapitalElement               = document.getElementById('has-capital');
const hasLowercaseElement             = document.getElementById('has-lowercase');
const hasSpecialElement               = document.getElementById('has-special');
const hasNumberElement                = document.getElementById('has-number');
const hasMinLengthElement             = document.getElementById('has-min-length');
const strongPasswordElement           = document.getElementById("is-success");

// DOM Elements for Password Matching
const doPasswordsMatch                = document.getElementById("is-password-a-match");

// DOM Elements for Links and Toggle Password Visibility
const haveAnAccountLink               = document.getElementById("have-an-account-link");
const notRegisteredLink               = document.getElementById("not-registered-link");
const showPasswordElement             = document.getElementById("show-password");
const showPasswordLabelElement        = document.querySelector(".checkbox label");

// DOM Element for Register Form
const registerForm                    = document.getElementById("register-form");


// DOM Element for display which password field the user is currently using
const activePasswordField   = document.getElementById('current-password-field-name');

// registration user field errors
const usernameErrorField    = document.querySelector(".username-error-field")
const emailErrorField       = document.querySelector(".email-error-field")


// csrf token
const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;


const passwordStrengthChecker = new PasswordStrengthChecker()


// Event listeners


// Show the login form and registration form when the corresponding links in the navigation bar are clicked
loginLinkElement?.addEventListener("click", handleLoginClick);
registerLinkElement?.addEventListener("click", handleRegisterClick);

// Close the login and registration forms when the close icons are clicked
closeLoginIconElement?.addEventListener("click", handleLoginCloseIcon);
closeRegistrationIconElement?.addEventListener("click", handleRegistrationCloseIcon);

// Toggle between login and registration forms based on user actions
haveAnAccountLink?.addEventListener("click", handleHaveAnAccountLink);
notRegisteredLink?.addEventListener("click", handleNotRegisteredLink);

// Toggle password visibility when the checkbox is changed
showPasswordElement?.addEventListener("change", handlePasswordToggle);

// form submission
registerForm?.addEventListener("submit", handleRegisterFormSubmit);



/**
 * 1. **Input Event**: Triggered when the user types in the field. This event updates the password strength
 *    indicator and checks if the password and confirm password fields match.
 * 2. **Click Event**: Triggered when the user clicks on the field. This event also updates the password strength
 *    indicator and checks if the password and confirm password fields match.
 * 3. It also updates which field in the UI the user is currently using.
 * 
 */
const passwordFieldMsg        = " Current using password field";
const confirmPasswordFieldMsg = " Current using confirm password field";

passwordElement.addEventListener("input", () => handlePasswordFieldValidation(passwordFieldMsg, confirmPasswordElement, passwordElement))
passwordElement.addEventListener("click", () => handlePasswordFieldValidation(passwordFieldMsg, confirmPasswordElement, passwordElement))
confirmPasswordElement.addEventListener("input", () => handlePasswordFieldValidation(confirmPasswordFieldMsg, passwordElement, confirmPasswordElement))
confirmPasswordElement.addEventListener("click", () => handlePasswordFieldValidation(confirmPasswordFieldMsg, passwordElement, confirmPasswordElement))




/**
 * Handles the submission of the registration form.
 * 
 * This function performs the following tasks:
 * 1. Prevents the default form submission behavior.
 * 2. Collects form data and validates password match.
 * 3. Sends requests to validate the password, username, and email.
 * 4. Displays validation messages and submits the form if all validations pass.
 * 
 * @param {Event} e - The form submit event.
 */
async function handleRegisterFormSubmit(e) {
    e.preventDefault();

    const formData = new FormData(registerForm);

    const password        = formData.get("password");
    const confirmPassword = formData.get("confirm_password");
    const email           = formData.get("email");
    const username        = formData.get("username");

    // Check if password and confirm password match
    if (!doPasswordMatch(password, confirmPassword)) {
        return;
    }

    // Validate password
    const passwordValidation = await fetchData({
        url: "authentication/validate/password/",
        csrfToken: csrfToken,
        body: { password }
    });

    // Validate username
    const usernameValidation = await fetchData({
        url: "authentication/validate/username/",
        csrfToken: csrfToken,
        body: { username }
    });

    // Validate email
    const emailValidation = await fetchData({
        url: "authentication/validate/email/",
        csrfToken: csrfToken,
        body: { email }
    });

    // Handle validation reports and determine if form can be submitted
    const isEmailValid     = handleFieldReport(emailErrorField, emailValidation);
    const isUsernameValid  = handleFieldReport(usernameErrorField, usernameValidation);

    if (passwordValidation?.IS_VALID && isEmailValid && isUsernameValid) {
        console.log("Registration successful");
        registerForm.submit();
    }
}

/**
 * Updates the UI based on the validation report for a given field.
 * 
 * This function clears any previous error messages and displays new messages 
 * based on the validation report. It also hides or shows the error field as needed.
 * 
 * @param {HTMLElement} fieldElement - The HTML element representing the error field.
 * @param {Object} validationReport - The validation report object containing validation results and messages.
 * @returns {boolean} - Returns `true` if the field is valid, `false` otherwise.
 */
function handleFieldReport(fieldElement, validationReport) {
    if (!fieldElement) {
        return false;
    }

    fieldElement.innerHTML = "";

    const isValid = validationReport?.IS_VALID;
    if (isValid) {
        fieldElement.classList.add("d-none");
    } else {
        fieldElement.classList.remove("d-none");
        fieldElement.textContent = validationReport?.message || "Validation error";
    }

    return isValid;
}




/**
 * Toggles the visibility of the password fields based on the state of the show password checkbox.
 * 
 * This function handles the event triggered when the user interacts with the checkbox to show or hide
 * the password fields. It toggles the type of both the password and confirm password fields between
 * 'text' and 'password', and updates the label text of the checkbox accordingly.
 * 
 * The function performs the following actions:
 * 
 * 1. Checks if the required HTML elements (password fields, checkbox, and label) are present and throws
 *    errors if any of them are missing.
 * 2. If the checkbox is checked, it sets the type of both password fields to 'text' to show the passwords
 *    and updates the label text to "Hide password".
 * 3. If the checkbox is unchecked, it sets the type of both password fields to 'password' to hide the
 *    passwords and updates the label text to "Show password". It also ensures the checkbox is unchecked.
 * 
 * @param {Event} e - The event object representing the user’s action on the checkbox.
 * 
 * @throws {Error} Throws an error if any of the required elements (password fields, checkbox, or label) are not found.
 */
function handlePasswordToggle(e) {
    e.preventDefault();

    if (!confirmPasswordElement || !passwordElement) {
        throw new Error("The confirm password or password element field couldn't be found!!!");
    }

    if (!showPasswordLabelElement) {
        throw new Error("The checkbox label for show password wasn't found!!");
    }

    if (!showPasswordElement) {
        throw new Error("The checkbox element couldn't be found!!!");
    }

    if (showPasswordElement.checked) {
        confirmPasswordElement.type = "text";
        passwordElement.type = "text";
        showPasswordLabelElement.textContent = "Hide password";
    } else {
        confirmPasswordElement.type = "password";
        passwordElement.type = "password";
        showPasswordLabelElement.textContent = "Show password";
        showPasswordElement.checked = false;
    }
}



/**
 * Handles the "Have an account? Click here" link in the registration form.
 * 
 * This function is triggered when the user clicks the "Have an account? Click here" link.
 * It hides the registration form, and displays the login form.
 *
 * @param {Event} e - The event object representing the user's click action.
 * @throws {Error} Throws an error if the registration element container is not found.
 */
function handleHaveAnAccountLink(e) {
    e.preventDefault();

    if (!registerAuthenticationContainer) {
        throw new Error("The registration element div wasn't found!!!");
    };

    registerAuthenticationContainer.classList.remove("show");
    loginAuthenticationContainer.classList.add("show");
}



/**
 * Handles the "Not registered - click here? Click here" link in the login form.
 * 
 * This function is triggered when the user clicks the "Not registered? Click here" link.
 * It hides the login form, and displays the registration form.
 *
 * @param {Event} e - The event object representing the user's click action.
 * @throws {Error} Throws an error if the registration element container is not found.
 */
function handleNotRegisteredLink(e) {
    e.preventDefault();

    if (!loginAuthenticationContainer) {
        throw new Error("The login element div wasn't found!!!");
    };

    registerAuthenticationContainer.classList.add("show");
    loginAuthenticationContainer.classList.remove("show");
}



/**
 * Handles the "login" link click event in the navigation bar.
 * 
 * This function is triggered when the user clicks the "login" link in the nav bar.
 * It displays the login form, and hides the registration form if active.
 *
 * @param {Event} e - The event object representing the user's click action.
 * @throws {Error} Throws an error if the login container element is not found.
 */
function handleLoginClick(e) {
    e.preventDefault();

    if (!loginAuthenticationContainer) {
        throw new Error("The login container couldn't be found!!");
    }

    loginAuthenticationContainer.classList.add("show");
    registerAuthenticationContainer.classList.remove("show");
}


/**
 * Handles the "register" link click event in the navigation bar.
 * 
 * This function is triggered when the user clicks the "register" link in the nav bar.
 * It displays the register form, and hides the registration form if active.
 *
 * @param {Event} e - The event object representing the user's click action.
 * @throws {Error} Throws an error if the login container element is not found.
 */
function handleRegisterClick(e) {
    e.preventDefault();

    if (!registerAuthenticationContainer) {
        throw new Error("The registeration container couldnt be found!!");
    }
    loginAuthenticationContainer.classList.remove("show");
    registerAuthenticationContainer.classList.add("show");
}





/**
 * Handles the click event for the close icon on the login form.
 * 
 * This function is triggered when the user clicks the close icon on the login form.
 * This action hides the login form.
 *
 * @param {Event} e - The event object representing the user's click action.
 * @throws {Error} Throws an error if the close icon element is not found.
 */
function handleLoginCloseIcon(e) {
    e.preventDefault();

    if (!closeLoginIconElement) {
        throw new Error("The login close icon wasn't found!!");
    };

    loginAuthenticationContainer.classList.remove("show");
}



/**
 * Handles the click event for the close icon on the register form.
 * 
 * This function is triggered when the user clicks the close icon on the register form.
 * This action hides the register form.
 *
 * @param {Event} e - The event object representing the user's click action.
 * @throws {Error} Throws an error if the close icon element is not found.
 */
function handleRegistrationCloseIcon(e) {
    e.preventDefault();
    if (!closeRegistrationIconElement) {
        throw new Error("The registration close icon wasn't found!!");
    };

    registerAuthenticationContainer.classList.remove("show");

}




/**
 * Validates and updates the UI for password and confirm password fields.
 * 
 * This function performs two main tasks:
 * 1. Updates the password strength indicator for the specified field using the provided message.
 * 2. Checks if the password and confirm password fields match and updates the UI accordingly.
 * 
 * @param {string} fieldMessage - A message to display in the UI related to the strength of the password field being checked.
 * @param {HTMLElement} passwordField - The HTML element representing the main password input field.
 * @param {HTMLElement} fieldToCheck - The HTML element representing the field being checked (e.g., confirm password field).
 */
function handlePasswordFieldValidation(fieldMessage, passwordField, fieldToCheck) {
   
    passwordStrengthHelper(fieldToCheck, fieldMessage);
    doPasswordMatch(passwordField.value, fieldToCheck.value);
}




/**
 * Updates the visual feedback for the strength of a password input field.
 * 
 * This function assesses the strength of the password entered in `passwordInputField` and updates
 * various UI elements to reflect the password's strength criteria. It checks for uppercase letters, 
 * lowercase letters, special characters, numbers, and minimum length requirements. It also updates 
 * the provided message `msg` in the relevant UI element.
 *
 * @param {HTMLElement} passwordInputField - The HTML element representing the password input field.
 * @param {string} msg - A message to display in the UI related to the password strength status.
 * 
 * @returns {void} - This function does not return any value but modifies the DOM to reflect password strength.
 * 
 * @throws {Error} - Throws an error if necessary elements or properties are not available.
 */
function passwordStrengthHelper(passwordInputField, msg) {
    const password = passwordInputField.value;
    passwordStrengthChecker.setPassword(password);
    let isValid;

    const textNode = activePasswordField.childNodes[2];
    textNode.nodeValue = msg;
    activePasswordField.classList.add("met");

    const passwordReport = passwordStrengthChecker.checkPasswordStrength();

    hasCapitalElement.classList.toggle("met", passwordReport.HAS_AT_LEAST_ONE_UPPERCASE);
    hasCapitalElement.classList.toggle("opacity-md", !passwordReport.HAS_AT_LEAST_ONE_UPPERCASE);

    hasLowercaseElement.classList.toggle("met", passwordReport.HAS_AT_LEAST_ONE_LOWERCASE);
    hasLowercaseElement.classList.toggle("opacity-md", !passwordReport.HAS_AT_LEAST_ONE_LOWERCASE);

    hasSpecialElement.classList.toggle("met", passwordReport.HAS_AT_LEAST_ONE_SPECIAL_CHARS);
    hasSpecialElement.classList.toggle("opacity-md", !passwordReport.HAS_AT_LEAST_ONE_SPECIAL_CHARS);

    hasNumberElement.classList.toggle("met", passwordReport.HAS_AT_LEAST_ONE_NUMBER);
    hasNumberElement.classList.toggle("opacity-md", !passwordReport.HAS_AT_LEAST_ONE_NUMBER);

    hasMinLengthElement.classList.toggle("met", passwordReport.HAS_AT_LEAST_LENGTH_CHARS);
    hasMinLengthElement.classList.toggle("opacity-md", !passwordReport.HAS_AT_LEAST_LENGTH_CHARS);

    isValid = passwordReport.IS_PASSWORD_STRONG;
    strongPasswordElement.classList.toggle("met", isValid);
    strongPasswordElement.classList.toggle("opacity-md", !isValid);
}



/**
 * Checks if the provided password and confirm password match and updates the UI accordingly.
 * 
 * This function compares the `password` and `confirmPassword` values to determine if they match. It updates
 * the visual feedback in the UI by toggling classes based on whether the passwords are the same or not.
 * 
 * @param {string} password - The value of the password input field.
 * @param {string} confirmPassword - The value of the confirm password input field.
 * 
 * @returns {boolean} Returns `true` if the password and confirm password match, otherwise `false`.
 */
function doPasswordMatch(password, confirmPassword) {
    doPasswordsMatch.classList.toggle("met", (password && password === confirmPassword));
    doPasswordsMatch.classList.toggle("opacity-md", (password && password !== confirmPassword));
    return password === confirmPassword;
}


