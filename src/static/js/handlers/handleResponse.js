import AlertUtils from "../utils/alerts.js";


export default async function handleResponse(response) {
    
    if (typeof response != "object") {
        throw new Error(`The response object must be an object, not type <${typeof response}>`);
    }

    // Check keys in the response object
    if (!("IS_VALID" in response) || !("message" in response)) {
        throw new Error("One or more keys is missing in the response object. Expected keys `isValid` and `message`.");
    }

    const isValid = response.IS_VALID;

    const title             = isValid ? "Successful!" : "Unsuccessful";
    const icon              = isValid ? "success" : "warning";
    const confirmButtonText = isValid ? "Great!!" : "Ok";

    AlertUtils.showAlert({
        title: title,
        text: response.message,
        icon: icon,
        confirmButtonText: confirmButtonText,
    });
    return isValid;
}