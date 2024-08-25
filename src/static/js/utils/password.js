/**
 * A utility class for checking the strength of passwords.
 */
class PasswordStrengthChecker {
    /**
     * Creates an instance of PasswordStrengthChecker.
     * @param {string} password - The password to be checked. Default empty string
     * @param {number} [defaultPasswordLength=8] - The default minimum length of the password.
     */
    constructor(password="", defaultPasswordLength = 8) {
        this.password = password;
        this.defaultPasswordLength = defaultPasswordLength;
    }

    setPassword(password) {
        this.password = password;
    }
    
    setDefaultPasswordLength(length) {
        this.defaultPasswordLength = length
    }

    /**
     * Checks if the password contains at least one special character.
     * @param {string} password - The password to be checked.
     * @returns {boolean} True if the password contains at least one special character, otherwise false.
     */
    containsAtLeastOneSpecialChar() {
        return /[!@#$%^&*()£_+\-=\[\]{};':"\\|,.<>\/?]+/.test(this.password);
    }

    /**
     * Checks if the password contains at least a specified number of characters.
     * @param {string} password - The password to be checked.
     * @param {number} [length=this.defaultPasswordLength] - The minimum length required for the password.
     * @returns {boolean} True if the password meets the minimum length requirement, otherwise false.
     */
    containsAtLeastLengthChars() {

        if(!this.password) {
            return false;
        }
        return this.password.length >= this.defaultPasswordLength;
    }

    /**
     * Checks if the password contains at least one digit.
     * @param {string} password - The password to be checked.
     * @returns {boolean} True if the password contains at least one digit, otherwise false.
     */
    containsNumber() {
        return /\d/.test(this.password);
    }

    /**
     * Checks if the password contains at least one lowercase letter.
     * @param {string} password - The password to be checked.
     * @returns {boolean} True if the password contains at least one lowercase letter, otherwise false.
     */
    containsLowercaseChars() {
        return /[a-z]/.test(this.password);
    }

    /**
     * Checks if the password contains at least one uppercase letter.
     * @param {string} password - The password to be checked.
     * @returns {boolean} True if the password contains at least one uppercase letter, otherwise false.
     */
    containsUppercaseChars() {
        return /[A-Z]/.test(this.password);
    }

 

    /**
     * Checks the strength of the password based on various criteria.
     * @returns {Object} An object containing password strength indicators.
     */
    checkPasswordStrength() {
        const passwordObj = {};

        passwordObj.HAS_AT_LEAST_ONE_SPECIAL_CHARS = this.containsAtLeastOneSpecialChar();
        passwordObj.HAS_AT_LEAST_LENGTH_CHARS = this.containsAtLeastLengthChars();
        passwordObj.HAS_AT_LEAST_ONE_NUMBER = this.containsNumber();
        passwordObj.HAS_AT_LEAST_ONE_LOWERCASE = this.containsLowercaseChars();
        passwordObj.HAS_AT_LEAST_ONE_UPPERCASE = this.containsUppercaseChars();

        passwordObj.IS_PASSWORD_STRONG =
            passwordObj.HAS_AT_LEAST_ONE_SPECIAL_CHARS &&
            passwordObj.HAS_AT_LEAST_LENGTH_CHARS &&
            passwordObj.HAS_AT_LEAST_ONE_NUMBER &&
            passwordObj.HAS_AT_LEAST_ONE_LOWERCASE &&
            passwordObj.HAS_AT_LEAST_ONE_UPPERCASE;
        
        return passwordObj;
    }


  
}

export default PasswordStrengthChecker;