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

};

export default AlertUtils;


