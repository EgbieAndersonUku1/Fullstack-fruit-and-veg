import { redirectToNewPage } from "./utils.js";


const AlertUtils = {
    /**
     * Show a SweetAlert2 alert.
     *
     * @param {Object} options - The options for the alert.
     * @param {string} options.title - The title of the alert.
     * @param {string} options.text - The text content of the alert.
     * @param {string} options.icon - The icon to display in the alert. 
     *                                Available options: 'success', 'error', 'warning', 'info', 'question'.
     * @param {string} options.confirmButtonText - The text for the confirm button.
     */
    showAlert({ title, text, icon, confirmButtonText }) {
        Swal.fire({
            title: title,
            text: text,
            icon: icon,
            confirmButtonText: confirmButtonText
        });
    },

    /**
     * Show a SweetAlert2 alert with redirection upon confirmation.
     *
     * @param {Object} options - The options for the alert.
     * @param {string} options.title - The title of the alert.
     * @param {string} options.text - The text content of the alert.
     * @param {string} options.icon - The icon to display in the alert. 
     *                                Available options: 'success', 'error', 'warning', 'info', 'question'.
     * @param {string} options.confirmButtonText - The text for the confirm button.
     * @param {string} options.redirectUrl - The URL to redirect to upon confirmation.
     */
    showAlertWithRedirect({ title, text, icon, confirmButtonText, redirectUrl }) {
        Swal.fire({
            title: title,
            text: text,
            icon: icon,
            confirmButtonText: confirmButtonText
        }).then((result) => {
            if (result.isConfirmed && redirectUrl) {
                redirectToNewPage(redirectUrl);
            }
        });
    },


    /**
     * Displays a SweetAlert2 confirmation alert. If the action is confirmed,
     * it executes the provided function, then shows a follow-up alert to indicate
     * the outcome of the action.
     *
     * @param {Object} options - The options for the confirmation alert.
     * @param {string} options.title - The title of the confirmation alert.
     * @param {string} options.text - The text content of the confirmation alert.
     * @param {string} options.icon - The icon to display in the confirmation alert.
     *                                Available options: 'success', 'error', 'warning', 'info', 'question'.
     * @param {string} options.confirmButtonText - The text for the confirm button.
     * @param {Object} options.colorButtonOptions - An object containing color options for the buttons.
     * @param {string} options.colorButtonOptions.confirmButtonColor - The color of the confirm button.
     * @param {string} options.colorButtonOptions.cancelButtonColor - The color of the cancel button.
     * @param {Function} options.func - A callback function to execute if the action is confirmed.
     *                                  This function can perform any task, such as making an API call, 
     *                                  updating the UI, or processing data.
     * @param {Object} options.followUpAlertAttrs - An object containing attributes for the follow-up alert 
     *                                              displayed after the action is confirmed and executed.
     * @param {string} options.followUpAlertAttrs.title - The title of the follow-up alert.
     * @param {string} options.followUpAlertAttrs.text - The text content of the follow-up alert.
     * @param {string} options.followUpAlertAttrs.icon - The icon to display in the follow-up alert.
     *                                                   Available options: 'success', 'error', 'warning', 'info', 'question'.
     */
    showConfirmationAlert({ title, text, icon, confirmButtonText, colorButtonOptions, func, followUpAlertAttrs }) {
        Swal.fire({
            title: title,
            text: text,
            icon: icon,
            showCancelButton: true,
            confirmButtonColor: colorButtonOptions.confirmButtonColor,
            cancelButtonColor: colorButtonOptions.cancelButtonColor,
            confirmButtonText: confirmButtonText,
        }).then((result) => {
            if (result.isConfirmed) {
                const funcResult = func();
                console.log(funcResult)
                if (funcResult && typeof funcResult.then === 'function') {
                    // If func() is a promise, wait for it to resolve
                    funcResult.then(() => {
                        this.showAlert({
                            title: followUpAlertAttrs.title,
                            text: followUpAlertAttrs.text,
                            icon: followUpAlertAttrs.icon,
                            confirmButtonText: confirmButtonText,
                        })
                       
                    });
                } else {
                    // If func() is not a promise, immediately show the follow-up alert
                    this.showAlert({
                        title: followUpAlertAttrs.title,
                        text: followUpAlertAttrs.text,
                        icon: followUpAlertAttrs.icon,
                        confirmButtonText: confirmButtonText,
                    })
                }
            }
        });
    }

};

export default AlertUtils;


