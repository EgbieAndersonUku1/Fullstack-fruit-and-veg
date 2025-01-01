import { getItemFromLocalStorage } from "../utils/utils.js";
import fetchData from "../utils/fetch.js";

// Event listeners
document.addEventListener("visibilitychange", handleVisibilityChange);



/**
 * Detects when a user switches tabs and checks if the user is authenticated in another tab.
 * If the user is logged in, the function automatically logs them into the currently visible tab.
 * 
 * @param {Event} e - The event object triggered by the visibility change of the document.
 * 
 * @example
 * // Assume the user opens multiple tabs of the home page but is not logged in any of them
 * // Further assume they pick a single tab and log into it and then switches over to another tab,
 * // the function will log them in automatically.
 */
async function handleVisibilityChange(e) {
    if (document.visibilityState === "visible") {

        const resp = getItemFromLocalStorage("authenticated");

        if (resp === "logged_in") {
            
            try {
               const url  = "authentication/check/session/";
               const data = await fetchData({url:url, method: "GET"});
              
               handleResponse(data);
               
            } catch (error) {
                
                if (error.message === "Failed to fetch" || error.message.includes("NetworkError"))  {
                    window.location.reload();
                }
                // Reload if the error message regarding 'undefined body' appears for a GET request
                if (error.message.includes("The body must be an object not type undefined") && error.config?.method === "GET") {
                   handleResponse();
                }

                console.error(`Fetch error: ${error.message} : request: ${error.config?.method}`);

            }
        } 
    }
}


function handleResponse(data=null) {
    if (data) {

        if (data.IS_LOGGED_IN) {
            window.location.reload();
        }      
    } else {
        window.location.reload()
    }
}