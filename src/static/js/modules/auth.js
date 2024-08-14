const loginAuthenticationContainer    = document.querySelector(".login");
const registerAuthenticationContainer = document.querySelector(".register");
const loginLinkElement                = document.getElementById("login");
const registerLinkElement             = document.getElementById("register-link");
const closeWindowIconElement          = document.querySelector(".auth-close-icon");
const closeRegistrationIconElement    = document.getElementById("reg-close-icon");
const passwordElement                 = document.getElementById("register-password");
const haveAnAccountLink               = document.getElementById("have-an-account-link");
const notRegisteredLink               = document.getElementById("not-registered-link");
const showPasswordElement             = document.getElementById("show-password");
const showPasswordLabelElement        = document.getElementById("show-password-label");

const confirmPasswordElement          = document.getElementById("register-confirm-password");
const hasCapitalElement               = document.getElementById('has-capital');
const hasLowercaseElement             = document.getElementById('has-lowercase');
const hasSpecialElement               = document.getElementById('has-special');
const hasNumberElement                = document.getElementById('has-number');
const hasMinLengthElement             = document.getElementById('has-min-length');
const strongPasswordElement           = document.getElementById("is-success");
const doPasswordsMatch                = document.getElementById("is-password-a-match");
const inputElementField               = document.getElementById('inputField');7



import PasswordStrengthChecker from "../utils/password.js";


const passwordStrengthChecker = new PasswordStrengthChecker()

loginLinkElement?.addEventListener("click", handleLoginClick);
closeWindowIconElement?.addEventListener("click", handleCloseIcon);

registerLinkElement?.addEventListener("click", handleRegisterClick);

closeRegistrationIconElement.addEventListener("click", handleRegistrationCloseIcon);


haveAnAccountLink?.addEventListener("click", handleHaveAnAccountLink);
notRegisteredLink?.addEventListener("click", handleNotRegisteredLink); 


showPasswordElement?.addEventListener("change", handlePasswordToggle);


function handlePasswordToggle(e) {

    e.preventDefault();

    if (!confirmPasswordElement || !passwordElement) {
        throw new Error("The confirm password or password element field couldn't be found!!!");
    };

    if (!showPasswordElement){
        throw new Error("The checkbox element couldn't be found!!!");
    };

    if (showPasswordElement.checked) {
        confirmPasswordElement.type          = "text";
        passwordElement.type                 = "text";
        showPasswordLabelElement.textContent = "Hide password";
    } else {
        confirmPasswordElement.type          = "password";
        passwordElement.type                 = "password";
        showPasswordLabelElement.textContent = "Show password";
        showPasswordElement.checked          = false;
    }
   
}


function handleHaveAnAccountLink(e) {
    e.preventDefault();

    if (!registerAuthenticationContainer) {
        throw new Error("The registration element div wasn't found!!!");
    };

    registerAuthenticationContainer.classList.remove("show");
    loginAuthenticationContainer.classList.add("show");
}


function handleNotRegisteredLink(e) {
    e.preventDefault();

    if (!loginAuthenticationContainer) {
        throw new Error("The login element div wasn't found!!!");
    };

    registerAuthenticationContainer.classList.add("show");
    loginAuthenticationContainer.classList.remove("show");
}



function handleLoginClick(e) {
    e.preventDefault();

    if (!loginAuthenticationContainer) {
        throw new Error("The login container couldnt be found!!");
    }

    loginAuthenticationContainer.classList.add("show");
    registerAuthenticationContainer.classList.remove("show");
}


function handleRegisterClick(e) {
    e.preventDefault();

    if (!registerAuthenticationContainer) {
        throw new Error("The registeration container couldnt be found!!");
    }
    loginAuthenticationContainer.classList.remove("show");
    registerAuthenticationContainer.classList.add("show");
}



function handleCloseIcon(e) {
    e.preventDefault();
    if (!closeWindowIconElement) {
        throw new Error("The login close icon wasn't found!!");
    };

 
    loginAuthenticationContainer.classList.remove("show");
              
}


function handleRegistrationCloseIcon(e) {
    e.preventDefault();
    if (!closeRegistrationIconElement) {
        throw new Error("The registration close icon wasn't found!!");
    };

    registerAuthenticationContainer.classList.remove("show");

}
passwordElement.addEventListener("input", () => {
    passwordStrengthHelper(passwordElement, " Current using password field");
    doPasswordMatch(passwordElement, confirmPasswordElement);
    
})

passwordElement.addEventListener("click", () => {
    passwordStrengthHelper(passwordElement, " Current using password field");
    doPasswordMatch(passwordElement, confirmPasswordElement);
    
})


confirmPasswordElement.addEventListener("input", () => {
    passwordStrengthHelper(confirmPasswordElement, " Current using confirm password field");
    doPasswordMatch(passwordElement, confirmPasswordElement);

})

confirmPasswordElement.addEventListener("click", () => {
    passwordStrengthHelper(confirmPasswordElement, " Current using confirm password field");
    doPasswordMatch(passwordElement, confirmPasswordElement);

})


function passwordStrengthHelper(passwordInputField, msg) {

    const password = passwordInputField.value;
    passwordStrengthChecker.setPassword(password);
    let  isValid;

    const textNode     = inputElementField.childNodes[2];
    textNode.nodeValue = msg;
    inputElementField.classList.add("met");

    const passwordReport = passwordStrengthChecker.checkPasswordStrength();
 
    hasCapitalElement.classList.toggle("met",         passwordReport.HAS_AT_LEAST_ONE_UPPERCASE);
    hasCapitalElement.classList.toggle("opacity-md",  !passwordReport.HAS_AT_LEAST_ONE_UPPERCASE);

    hasLowercaseElement.classList.toggle("met",       passwordReport.HAS_AT_LEAST_ONE_LOWERCASE);
    hasLowercaseElement.classList.toggle("opacity-md",!passwordReport.HAS_AT_LEAST_ONE_LOWERCASE);

    hasSpecialElement.classList.toggle("met",        passwordReport.HAS_AT_LEAST_ONE_SPECIAL_CHARS);
    hasSpecialElement.classList.toggle("opacity-md", !passwordReport.HAS_AT_LEAST_ONE_SPECIAL_CHARS);

    hasNumberElement.classList.toggle("met",         passwordReport.HAS_AT_LEAST_ONE_NUMBER);
    hasNumberElement.classList.toggle("opacity-md",  !passwordReport.HAS_AT_LEAST_ONE_NUMBER);

    hasMinLengthElement.classList.toggle("met", passwordReport.HAS_AT_LEAST_LENGTH_CHARS);
    hasMinLengthElement.classList.toggle("opacity-md", !passwordReport.HAS_AT_LEAST_LENGTH_CHARS);
 
    isValid = passwordStrengthChecker.isValid()
    strongPasswordElement.classList.toggle("met", isValid);
    strongPasswordElement.classList.toggle("opacity-md", !isValid);
}

function doPasswordMatch(passwordInputField, confirmPasswordInputField) {
    const password        = passwordInputField.value;
    const confirmPassword = confirmPasswordInputField.value;

    doPasswordsMatch.classList.toggle("met",  (password && password === confirmPassword));
    doPasswordsMatch.classList.toggle("opacity-md", (password && password !== confirmPasswordElement.value));

}


