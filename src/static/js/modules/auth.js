import PasswordStrengthChecker from "../utils/password.js";
import fetchData from "../utils/fetch.js";
import { saveToLocalStorage, clearStorage } from "../utils/utils.js";
import { getFormEntries } from "../utils/formUtils.js";
import fingerprintDevice from "../utils/browser.js";
import { redirectToNewPage } from "../utils/utils.js";


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

// DOM Element for Register and Login Form
const registerForm                    = document.getElementById("register-form");
const loginForm                       = document.getElementById("login-form")

// DOM Element for display which password field the user is currently using
const activePasswordField   = document.getElementById('current-password-field-name');

// registration user field errors
const usernameErrorField    = document.querySelector(".username-error-field")
const emailErrorField       = document.querySelector(".email-error-field")

// login message field
const loginMsgFElement      = document.getElementById("login-msg");

// spinner element
const spinner               = document.querySelector(".spinner")

// csrf token
const csrfToken             =  document.querySelector('input[name="csrfmiddlewaretoken"]').value;


// form buttons
const loginButtonElement    = document.getElementById("login-btn");
const registerButtonElement = document.getElementById("register-btn");


const passwordStrengthChecker = new PasswordStrengthChecker()


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

// form submissions
registerForm?.addEventListener("submit", handleRegisterFormSubmit);
loginForm?.addEventListener("submit", handleLoginFormSubmit);


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
 * 1. Collects form data and validates password match.
 * 2. Sends requests to validate the password, username, and email.
 * 3. Displays validation messages and submits the form if all validations pass.
 * 
 * @param {Event} e - The form submit event.
 */
async function handleRegisterFormSubmit(e) {
    e.preventDefault();


    const formData =  getFormEntries(registerForm);

    if (!doPasswordMatch(formData.password, formData["confirm_password"]) ) {
        return;
    }

    const resp = await processRegistrationform(formData)    
  
    if (resp) {
        console.log("Registration successful");

        spinner?.classList.remove("show");
        registerForm.submit();
    }
};





/**
 * Asynchronously processes and validates the registration form data.
 *
 * This function handles the registration process by performing asynchronous validation
 * on the provided form data. It validates the password, username, and email by sending
 * requests to the respective validation endpoints. It also manages the button state during
 * the validation process to provide feedback to the user.
 *
 * @param {Object} formData - An object containing the registration form data.
 * @param {string} formData.username - The username to be validated.
 * @param {string} formData.password - The password to be validated.
 * @param {string} formData.email - The email to be validated.
 *
 * @returns {Promise<boolean>} A promise that resolves to a boolean indicating whether
 *                             all validations passed. Returns `true` if the password, 
 *                             email, and username are valid; otherwise, returns `false`.
 *
 * @throws {Error} Throws an error if there is an issue with making the validation requests.
 */
async function processRegistrationform(formData) {
   
    spinner?.classList.add("show");
    setButtonState(true, registerButtonElement, "register", "please wait");

    try {
       
        const passwordValidation = await fetchData({
            url: "authentication/validate/password/",
            csrfToken: csrfToken,
            body: { password: formData.password },

        });

       
        const usernameValidation = await fetchData({
            url: "/authentication/validate/username/",
            csrfToken: csrfToken,
            body: { username: formData.username }
        });


        const emailValidation = await fetchData({
            url: "authentication/validate/email/",
            csrfToken: csrfToken,
            body: { email: formData.email }
        });


        setButtonState(false, registerButtonElement, "register", "please wait");

        const isEmailValid     = handleFieldReport(emailErrorField, emailValidation);
        const isUsernameValid  = handleFieldReport(usernameErrorField, usernameValidation);

    
        return passwordValidation?.IS_VALID && isEmailValid && isUsernameValid;

    } catch (error) {
        spinner?.classList.remove("show");
        setButtonState(true, registerButtonElement, "register", "please wait");
    }
}


/**
 * Retrieves the value of the specified query parameter from the current URL.
 * 
 * @param {string} params - The name of the query parameter to extract.
 * @returns {string|null} - The value of the query parameter, or null if it does not exist.
 */
function getQueryParams(params) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(params);
}


/**
 * Handles the submission of the login form by processing and validating the form data.
 *
 * This function is triggered when the login form is submitted.  retrieves form data, 
 * and validates it using the `processLoginForm`
 * function. If the validation is successful, the user is redirected to the account page.
 *
 * @param {Event} e - The submit event object from the form submission.
 *
 * @returns {Promise<void>} This function does not return a value but performs actions based
 *                          on the result of the login validation.
 *
 */
async function handleLoginFormSubmit(e) {
    e.preventDefault();

    const formData = getFormEntries(loginForm);

    if (!formData.email && !formData.password) {
        return;
    }

    const resp = await processLoginForm(formData);

    if (resp) {
      
        console.log("You have logged in...");
        const nextUrl = getQueryParams("next");
        const url     = nextUrl ? nextUrl : "/account/landing-page/";
        spinner?.classList.remove("show");
        clearStorage();
        saveToLocalStorage("authenticated", "logged_in");
        redirectToNewPage(url);
        
       
    } else {
        spinner?.classList.remove("show");
    }
      
}



/**
 * Processes and validates the login form data by sending it to the server for authentication.
 *
 * This function manages the login process by sending the provided form data to the server
 * for validation. It handles the state of the login button to provide user feedback during
 * the process. It also processes the server's response to update the UI with validation messages.
 *
 * @param {Object} formData - An object containing the login form data.
 * @param {string} formData.email - The email address entered by the user.
 * @param {string} formData.password - The password entered by the user.
 *
 * @returns {Promise<boolean>} A promise that resolves to a boolean indicating whether
 *                             the login process was successful. Returns `true` if the
 *                             login is successful and the UI is updated accordingly; otherwise, returns `false`.
 *
 */
async function processLoginForm(formData) {
     
    spinner?.classList.add("show");
    setButtonState(true, loginButtonElement, "Login", "please wait...");


    try {
        const validateReport = await fetchData({url: "authentication/login/",
            csrfToken: csrfToken,
            body: { auth: {email:formData.email, password:formData.password, userDeviceInfo: fingerprintDevice() }},
            });

       
        setButtonState(false, loginButtonElement, "Login", "please wait...");
        return handleFieldReport(loginMsgFElement, validateReport);

    } catch (error) {
        setButtonState(false, loginButtonElement, "Login", "please wait...");
        spinner?.classList.remove("show");
        
      
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
 * Updates the state of a button element to indicate loading or completion.
 * 
 * This function changes the button text and disables/enables the button 
 * based on the `isLoading` parameter. It's goal is for providing feedback 
 * to users during asynchronous operations like form submissions or data fetching.
 *
 * @param {boolean} isLoading - Determines the state of the button. If `true`, 
 *                              the button is set to a loading state; if `false`, 
 *                             the button is reset to its default state.
 * @param {HTMLElement} buttonElement - The button element whose state will be updated.
 * @param {string} defaultMsg - The text to display on the button when not loading.
 * @param {string} processingMsg - The text to display on the button while loading.
 *
 * @example
 * // Disables the button and sets the text to "Processing..."
 * setButtonState(true, submitButton, "Submit", "Processing...");
 *
 * @example
 * // Enables the button and sets the text back to "Submit"
 * setButtonState(false, submitButton, "Submit", "Processing...");
 */
function setButtonState(isLoading, buttonElement, defaultMsg = "Submit", processingMsg = "Please wait...") {
    if (!buttonElement) {
        console.error("Invalid button element provided.");
        return;
    }

    if (isLoading) {
        buttonElement.textContent = processingMsg;
        buttonElement.disabled = true;
    } else {
        buttonElement.textContent = defaultMsg;
        buttonElement.disabled = false;
    }
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
 * It displays the register form, and hides the login form if active.
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



