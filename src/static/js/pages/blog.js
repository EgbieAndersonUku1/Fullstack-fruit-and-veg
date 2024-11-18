import splitStringByDelimiter from "../utils/parser.js";
import { validateElement } from "../errors/customErrors.js";
import { calculateDistanceBetweenTwoPoints } from "../utils/distanceUtils.js";
import {addActiveStatusToHeaderTab,  
        hideAllTabSection, 
        removeActiveFromTabs, 
        showTabSection, 
        toggleTabVisibility  } from "../utils/tabUtils.js";


// Spinner and loading elements
const spinner           = document.querySelector(".small-spinner");

// Tab-related elements for navigation
const allTab            = document.getElementById("all-tab");
const celebrateTab      = document.getElementById("celebrate-tab");
const funnyTab          = document.getElementById("funny-tab");
const headers           = document.querySelectorAll("#show-likes .tabs .tab a");
const hundredTab        = document.getElementById("hundred-tab");
const likeTab           = document.getElementById("like-tab");
const loveTab           = document.getElementById("love-tab");
const insightTab        = document.getElementById("insight-tab");
const sparklesTab       = document.getElementById("sparkles-tab");
const tabSections       = document.querySelectorAll(".tab-section");
const tabs              = document.getElementById("tabs");

// Blog and interaction elements
const blogContainer           = document.querySelector(".blog-interactions");
const blogLink                = document.getElementById("num-of-likes-link");
const commentSection          = document.getElementById("comments-section");
const showEmojiLikeContainer  = document.getElementById("show-likes");


// User interaction and reaction elements
const numOfLikes        = document.querySelector(".num-of-likes");
const reactionEmojisDiv = document.querySelector(".user-reactions-choices");
const reactionEmojiPTag = document.querySelector(".reaction-emoji-name p");
const thumbsUpLink      = document.querySelector(".thumbs-up").closest("a");
const thumbsUpIcon      = document.querySelector(".thumb-up-icon");


// Background and UI control elements
const closeIcon            = document.querySelector(".close-icon");
const dimBackgroundElement = document.querySelector(".dim-overlay");


// Constant UI
const ACTIVE_TAB_CLASSNAME   = "tab-active";
const NUM_OF_SECS_TO_DISPLAY = 1000;

const TABS = {
    ALL_EMOJI: "allIcon",
    LIKE_EMOJI : "likeIcon",
    LOVE_EMOJI : "loveIcon",
    INSIGHT_EMOJI: "insightIcon",
    CELEBRATE_EMOJI: "celebrateIcon",
    FUNNY_EMOJI: "funnyIcon",
    SPARKLES_EMOJI: "sparklesIcon",
    HUNDRED_EMOJI: "hundredIcon"
};


// Event listeners
document.addEventListener("DOMContentLoaded", setUp);
blogLink?.addEventListener("click", (e) => handleToggleClick(e));
closeIcon?.addEventListener("click", (e) => handleToggleClick(e, false));


// validate elements
validateElement(numOfLikes, "This is not a valid HTML element");
validateElement(thumbsUpLink, "This is not a valid element ");
validateElement(dimBackgroundElement, "This is not a valid element");

// Event listeners
commentSection?.addEventListener("click", handleComment);
reactionEmojisDiv.addEventListener("click", handleEmojiClick);
thumbsUpLink.addEventListener("click", handleThumbsUpToggle);
tabs?.addEventListener("click", handleReactionTabs);

thumbsUpIcon?.classList.add("bounce");


// const Values
const FLY_CLASS    = "fly";
const EMOJIS_ATTRS = {
   
    celebrateIcon: { color: "green", name: "celebrate" },
    funnyIcon: { color: "pink", name: "funny" },
    hundredIcon: { color: "purple", name: "hundred" },
    insightIcon: { color: "orange", name: "insight" },
    likeIcon: { color: "royalblue", name: "like" },
    loveIcon: { color: "red", name: "love" },
    sparklesIcon: { color: "gold", name: "sparkles" },
};


/**
 * Handles comment interactions using event delegation.
 * Listens for specific events triggered within the comment section, including:
 * 
 * 1. When a control panel is clicked. The control panel contains options:
 *      a. Close Edit
 *      b. Delete Comment
 *      c. Edit
 * 
 * 2. Detects when the "Edit" link is clicked to trigger an edit action.
 * 3. Detects when the "Delete" link is clicked to remove a comment.
 * 
 * Also listens for reply-related actions:
 * - If the click happens within a `.reply-link-div` inside an `.author-comment`, 
 *   it triggers the reply handler.
 * 
 * @param {Event} event - The DOM event object.
 */
function handleComment(event) {
  
    const CONTROL_PANEL = "controlPanel";
    const replyLinkDiv  = event.target.closest(".author-comment .reply-link-div");
    const EDIT_LINK     = "Edit";
    const CLOSE_EDIT    = "Close Edit";
 
    event.preventDefault();

    if (replyLinkDiv) {
        handleReplyLink(event);
    } else if (event.target.dataset.panel === CONTROL_PANEL) {
        handleControlPanel(event);
    } else if (event.target.textContent.trim() === EDIT_LINK) {
        handleEditLink(event);
    }else if (event.target.textContent.trim() === CLOSE_EDIT) {
        handleCloseEdit(event);
    };
   
}


/**
 * Handles actions related to the reply section when the reply link is clicked.
 * 
 * This function is triggered by a click event on a reply link within a comment section.
 * It manages the creation or visibility of the reply form, setting attributes like:
 * - Button name ("Reply")
 * - Placeholder text ("Add a reply...")
 * 
 * If the reply form div is not a valid HTML element, an error message is displayed.
 * The function also toggles the text of the reply link between showing and hiding the reply form.
 * 
 * @param {Event} event - The DOM event object triggered by the click on the reply link.
 */
function handleReplyLink(event) {

    const replyErrorMsg  = "Reply Form Div is not a valid HTML instance";
    const replyFormID    = "reply-form";
    const replyFormAttrs = {buttonName: "Reply", placeholder: "Add a reply..."};

    handleLinkClick(event, replyErrorMsg, replyFormID, replyFormAttrs, toggleReplyLinkText);

};



/**
 * 
 * @param {*} event 
 */
function handleEditLink(event) {

    const editErrorMsg  = "Edit Form Div is not a valid HTML instance";
    const editFormID    = "edit-form";
    const editFormAttrs = {buttonName: "Edit"};
    const editForm      = handleLinkClick(event, editErrorMsg, editFormID, editFormAttrs, toggleEditLinkText);
    const commentID     = splitStringByDelimiter(event.target.id, "-")[2];

    if (!commentID) {
        throw new Error(`Expected a comment ID but received ${commentID}`);
    };

    const commentToEdit = document.getElementById(commentID);
    replaceText(editForm, commentToEdit);
    
};


/**
 * 
 * @param {*} event 
 */
function handleControlPanel(event) {
    event.preventDefault();
    showModal();
    toggleSpinner();
    setTimeout(() => {
        
        const actionBoxID          = event.target.getAttribute("data-action-box-id");
        const controlPanel         = document.getElementById(actionBoxID);
        controlPanel.style.display = "grid";

        toggleSpinner(false);
            
    }, NUM_OF_SECS_TO_DISPLAY);  
};


/**
 * 
 * @param {*} event 
 */
function handleCloseEdit(event) {

    const commentID = splitStringByDelimiter(event.target.id, "-")[2];
    
    if (!commentID) {
        throw new Error(`Expected a comment ID but received ${commentID}`);
    }
    
    const commentToEdit          = document.getElementById(commentID);
    const editForm               = document.getElementById(`edit-${commentID}`);
    const controlPanelToggleIcon = document.getElementById(`control-panel-${commentID}`);
    
    validateElement(editForm, `This is not a valid HTML form - Expected an edit form but received - ${editForm}`, true);
    validateElement(controlPanelToggleIcon, `This is not a valid HTML element - Expected a toggle HTML element but received - ${controlPanelToggleIcon}`);
    
    toggleSpinner();
    
    setTimeout(() => {

        commentToEdit.classList.remove("d-none");
        editForm.classList.remove("d-none");
        removeModal();
        
        controlPanelToggleIcon.style.display = "block";

        // close control panel
        const controlPanel                   = document.getElementById(`action-${commentID}`);
        controlPanel.style.display           = "none";

        // Close the form and change the text button 
        editForm.style.display               = "none";
        event.target.textContent             = "Edit";

        toggleSpinner(false);

       
        }, NUM_OF_SECS_TO_DISPLAY);

};


/**
 * 
 * @param {*} editForm 
 * @param {*} textToReplace 
 */
function replaceText(editForm, textToReplace) {

    [editForm, textToReplace].every((element) => validateElement(element, "This is not a valid HTML element", true));
   
    textToReplace.classList.add("d-none"); 

    const textArea  = editForm.querySelector("textarea");
    let pTagContent = textToReplace.textContent;

    // Remove leading and trailing spaces and normalize whitespace
    pTagContent = pTagContent.replace(/\s+/g, ' ')        // Replace multiple spaces with a single space
                     .replace(/(\n\s*)+/g, '\n')          // Normalize newlines and remove indentation spaces
                     .trim();
    
    textArea.value = pTagContent;
};


/**
 * 
 * @param {*} e 
 * @param {*} errorMsg 
 * @param {*} formID 
 * @param {*} formAttrs 
 * @param {*} toggleLinkFunc 
 * @returns 
 */
function handleLinkClick(e, errorMsg, formID, formAttrs, toggleLinkFunc) {

    e.preventDefault();

    const ANCHOR_TAG = "A";

    if (e.target.nodeName == ANCHOR_TAG) {

        const link      = e.target;
        const formDivID = link.dataset.formElementId;
        const formDiv   = document.getElementById(formDivID);

        validateElement(formDiv, errorMsg, true);

        const formId  = `${formID}${splitStringByDelimiter(formDiv.id)[1]}`;
        const form    = createForm(formId, formAttrs);
        
        if (!form) {
            throw new Error(`Expected a form but received <${form}>`)
        }
        clearElement(formDiv);
        formDiv.appendChild(form);
             
        const show = formDiv.style.display === "" ? true : false;
        toggleForm(formDiv, link, show, toggleLinkFunc);
        return form;
       
    };
    
}


/**
 * 
 * @param {*} form 
 * @param {*} link 
 * @param {*} show 
 * @param {*} toggleLinkTextFunc 
 */
function toggleForm(form, link, show = true, toggleLinkTextFunc) {

    const NUM_OF_SECS_TO_DISPLAY = 1000;

    if (form) {
        spinner.style.display = "block";

        setTimeout(() => {
            spinner.style.display   = "none";
            form.style.display = show ? "block" : "";

            toggleLinkTextFunc(link, show)

        }, NUM_OF_SECS_TO_DISPLAY);
    };
};



/**
 * 
 * @param {*} link 
 * @param {*} showClosMsg 
 */
function toggleEditLinkText(link, showClosMsg=true) {
  
    if (link.textContent === "Edit" && !showClosMsg) {
        link.innerText = "Close Edit";
        return;
    };

    link.innerText = showClosMsg ? "Close Edit" : "Edit";

}


/**
 * 
 * @param {*} replyLink 
 * @param {*} showClosMsg 
 */
function toggleReplyLinkText(replyLink, showClosMsg=true) {
    replyLink.innerText = showClosMsg ? "Close Reply" : "Reply";

}


/**
 * 
 * @param {*} divToClear 
 */
function clearElement(divToClear) {
    divToClear.innerHTML = ""
}


/**
 * 
 * @param {*} formID 
 * @param {*} formAttrs 
 * @returns 
 */
function createForm(formID, formAttrs={}) {
    
    if (typeof formAttrs === "object" && !("buttonName" in formAttrs)) {
        throw new Error("One or more of the keys for the form attribute is missing. Expect two keys 'buttonName' and 'placeholder' ");
    }

    
     // Array of input field attributes
     const inputFieldsAttrs  = [
        {type: "text", name:"author-name", required:true, id:"reply-author-name", placeholder: "Author's name..."},
        {type: "email", name:"author-email", required:true, id:"reply-author-email", placeholder: "Author's email..."},
        {type: "text", name:"author-website", required:false, id:"reply-author-website", placeholder: "Author's website optional..."}
    ];
    
    const divInputFieldsContainer = createElement({ elementToCreate: "div",
                                                    attrsToSet: {className: ["form-group", "triple-grid"]},
                                                    setterFunc: setFormElementAttributes
                                                  });
    
    const divButtonContainer = createElement({ elementToCreate: "div",
                                                attrsToSet: {className: ["button", "flex-end"]},
                                                setterFunc: setFormElementAttributes
                                            });
    
    
    const form = createElement({ elementToCreate: "form", 
                                 attrsToSet: { id: formID, 
                                              method: "post", 
                                              action: ""  // Todo -Add later when the backend feature is buitl
                                             },
                                 setterFunc: setFormAttributes
                                }
                              );

    const textArea = createElement({ elementToCreate: "textArea",
                                     attrsToSet: {name: "replay-form-textarea",
                                                  id:"replay-form-textarea",
                                                  rows:"10",
                                                  cols:"10",
                                                  placeholder:formAttrs.placeholder || "Add text....",
                                                 },
                                     setterFunc: setFormElementAttributes,
                                 });
    
    const replyButton = createElement({ elementToCreate: "button",
                                        attrsToSet: {type: "submit",
                                                     className: ["text-capitalize",  "button-sm", "comment-btn", "dark-green-bg"],
                                                     innerText: formAttrs.buttonName,
                                                     },
                                               setterFunc: setFormElementAttributes,

                                });
    
  
    inputFieldsAttrs.forEach((inputAttrs) => {

        const inputElement = createElement({ elementToCreate: "input",
                                            attrsToSet: inputAttrs,
                                            setterFunc: setFormElementAttributes,
                                            });

        divInputFieldsContainer.appendChild(inputElement);
     
    });
    

    divButtonContainer.appendChild(replyButton);

    form.appendChild(textArea);
    form.appendChild(divInputFieldsContainer);
    form.appendChild(divButtonContainer);
    return form;

};




/**
 * Sets attributes on a given form element.
 * This function sets the `id`, `action`, and `method` attributes on the form element.
 * If the `method` attribute is not provided in the `attrs` object, it defaults to `"post"`.
 * 
 * @param {HTMLFormElement} form - The form element to which the attributes will be applied.
 * @param {Object} attrs - An object containing the attributes to set on the form.
 * @param {string} attrs.id - The `id` attribute to assign to the form.
 * @param {string} attrs.action - The `action` attribute to assign to the form.
 * @param {string} [attrs.method="post"] - The HTTP method (`GET` or `POST`) for the form submission. Defaults to `"post"`.
 * 
 * @returns {HTMLFormElement} The modified form element with the applied attributes.
 */
function setFormAttributes(form, attrs ) {

    form.id      = attrs.id
    form.action  = attrs.action;
    form.method  = attrs.method || "post";
    return form;
};




/**
 * Sets attributes and properties on a given form element.
 * This function iterates through the `attrs` object and applies each property to the `element`.
 * It handles special cases like setting the `innerText` property or adding multiple classes 
 * to the element's class list. For other attributes, it uses `setAttribute` to apply them 
 * to the element.
 * 
 * @param {HTMLElement} element - The form element to which the attributes and properties will be applied.
 * @param {Object} attrs - An object where keys are attribute names or property names and values are the values to set.
 * @param {string} [attrs.innerText] - If present, this will set the `innerText` property of the element.
 * @param {string|Array} [attrs.className] - A single class name or an array of class names to be added to the element.
 * 
 * @returns {HTMLElement} The modified element with the applied attributes and properties.
 */
function setFormElementAttributes(element, attrs) {
    for (let key in attrs) {
        if (attrs.innerText) {
            element.innerText = attrs.innerText; 
        }
        if (key === "className") {
            if (Array.isArray(attrs.className)) {
                attrs.className.forEach(className => element.classList.add(className));
            } else {
                element.className = attrs.className;
            }
        } else if (key in element) {
            element.setAttribute(key, attrs[key]);
        }
    };

    return element;
}



/**
 * Creates a new HTML element and applies attributes or settings to it using a setter function.
 * This function creates an element based on the provided `elementToCreate` type, 
 * applies attributes using `attrsToSet`, and then applies additional settings 
 * via the provided `setterFunc`. If an error occurs during element creation or setting, 
 * it is caught and logged to the console.
 * 
 * @param {Object} params - The parameters for creating the element.
 * @param {string} params.elementToCreate - The type of the HTML element to create (e.g., "div", "span").
 * @param {Object} [params.attrsToSet={}] - An object containing attributes to set on the element (optional).
 * @param {Function} params.setterFunc - A function that applies additional settings to the element.
 * 
 * @returns {HTMLElement|undefined} The created and modified element, or `undefined` if an error occurs.
 */
function createElement({elementToCreate, attrsToSet={}, setterFunc}) {
    const element = document.createElement(elementToCreate);
  
    try {
        return setterFunc(element, attrsToSet);
    } catch (error) {
        console.error(`Something went wrong creating element - ${JSON.stringify(error.message)}`);
        
    }
}



/**
 * Handles the click event on an emoji or link element, triggering a "fly" animation 
 * and updating the like count.
 * The function calculates the distance from the clicked emoji to the base (left-hand side) of the blog container, 
 * ensuring the flying emoji lands precisely at the container's base. This works regardless of the emoji’s
 * initial position in the row, so each one always lands in the same spot on the container
 * It also updates the displayed emoji and like count.
 * 
 * @param {Event} e - The click event object triggered by clicking on an emoji or link.
 */
function handleEmojiClick(e) {
    e.preventDefault();

    if (e.target.nodeName === "IMG" || e.target.nodeName === "A") {
        removeFlyClass();
 
        const reactionEmoji    = e.target.closest("img");
        const distanceToTravel = calculateDistanceBetweenTwoPoints(blogContainer, reactionEmoji);

        if (distanceToTravel) {
            const offset            = 40;
            const reactionEmojiName = reactionEmoji.dataset.emoji;
          
            reactionEmoji.classList.add(FLY_CLASS); 
            setReactionEmoji(reactionEmojiName);
            reactionEmoji.style.setProperty('--distance-x', `${-distanceToTravel + offset}px`);
            updateLikes();

        } else {
            clearElement(reactionEmojiPTag);
        }
       
    }
}


/**
 * Removes the "fly" class from all reaction emoji elements.
 * This function selects all elements with the class `reaction-icon` and 
 * removes the `FLY_CLASS` class from each of them which effectively stops any 
 * ongoing "fly" animation or effect applied to the reaction icons.
 */
function removeFlyClass() {
    const reactionEmojis = document.querySelectorAll(".reaction-icon");

    reactionEmojis.forEach((reactionEmoji) => {
        reactionEmoji.classList.remove(FLY_CLASS);
    });
}



/**
 * Sets the reaction emoji based on the provided identifier.
 * This function clears the current reaction emoji text, retrieves the corresponding 
 * emoji data (name and color) from the `EMOJIS_ATTRS` object using the given identifier, 
 * and then updates the content and style of the `reactionEmojiPTag` element to display 
 * the emoji name with the specified color.
 * 
 * @param {string} identifier - The identifier for the emoji, used to look up the 
 *                              corresponding emoji data in the `EMOJIS_ATTRS` object.
 */
function setReactionEmoji(identifier) {
    clearElement(reactionEmojiPTag);
    const identifierObject = EMOJIS_ATTRS[identifier];
  
    if (identifierObject !== "undefined") {

        reactionEmojiPTag.innerText   = identifierObject["name"];
        const color                   = identifierObject["color"];
        reactionEmojiPTag.style.color = color;
    }
   
}


/**
 * Updates the like count displayed on the page by incrementing it by 1 each time it is clicked.
 * This function also updates the text content to reflect the new like count.
 * It also handles singular and plural forms for the word "like."
 */
function updateLikes() {
    const numOfLikesString = numOfLikes?.lastChild?.textContent;

    if (numOfLikesString) {
       
        const likesString = splitStringByDelimiter(numOfLikesString, " ")[1];
        const likes       = parseInt(likesString, 10);
    
        if (!isNaN(likes)) {
           
            const updatedLikes = likes + 1;
            numOfLikes.lastChild.textContent = updatedLikes === 1 ? ` ${updatedLikes} like` : ` ${updatedLikes} likes`;
        }
    }
}



/**
 * Handles the thumbs up toggle interaction, showing or hiding the reaction emojis.
 * The first clicks show the reaction emojis  and the second click hides it
 * 
 * @param {Event} e - The click event object triggered by the thumbs-up link.
 */
function handleThumbsUpToggle(e) {
    e.preventDefault();

    spinner.style.display = "block";
    toggleSpinner();
    setTimeout(() => {

     
        toggleSpinner(false);
        const status                    = reactionEmojisDiv.style.display;
        reactionEmojisDiv.style.display = status === "grid" ? "" : "grid";
        thumbsUpLink.style.color        = status === "grid" ? "black"  : "blue";
        
        if (status === "grid") {
            clearElement(reactionEmojiPTag);
            
        }
    }, NUM_OF_SECS_TO_DISPLAY);
}


/**
 * Initializes the reaction tabs by setting the default active tab and hiding others.
 * This function hides all tab sections, removes the active status from all header tabs, 
 * and then shows the "All" tab section and marks the first header tab as active.
 */
function setUp() {

    hideAllTabSection(tabSections);
    removeActiveFromTabs(headers, ACTIVE_TAB_CLASSNAME);
       
    showTabSection(allTab);
    const firstTab = headers[0]
    addActiveStatusToHeaderTab(firstTab, ACTIVE_TAB_CLASSNAME);
};


/**
 * Handles the click event on reaction emoji tabs, toggling the visibility of emoji-specific
 * reaction tabs and setting the active tab based on the selected emoji.
 * 
 * @param {Event} e - The click event object triggered by selecting an emoji tab.
 */
function handleReactionTabs(e) {

    e.preventDefault();
    const IMG_TAG = "IMG";
   
    if (e.target.nodeName === IMG_TAG) {
        const emoji = e.target.dataset.emoji;
        console.log(emoji);
        removeActiveFromTabs(headers, ACTIVE_TAB_CLASSNAME);
    
        switch (emoji) {
            case TABS.ALL_EMOJI:
                toggleTabVisibility(allTab, [likeTab, loveTab, insightTab, celebrateTab, funnyTab, sparklesTab, hundredTab], headers[0], ACTIVE_TAB_CLASSNAME);
                break;
            case TABS.LIKE_EMOJI:
                toggleTabVisibility(likeTab, [loveTab, insightTab, celebrateTab, funnyTab, sparklesTab, hundredTab, allTab], headers[1], ACTIVE_TAB_CLASSNAME);
                break;
            case TABS.LOVE_EMOJI:
                toggleTabVisibility(loveTab, [likeTab, insightTab, celebrateTab, funnyTab, sparklesTab, hundredTab, allTab], headers[2], ACTIVE_TAB_CLASSNAME);
                break;
            case TABS.INSIGHT_EMOJI:
                toggleTabVisibility(insightTab, [likeTab, loveTab, celebrateTab, funnyTab, sparklesTab, hundredTab, allTab], headers[3], ACTIVE_TAB_CLASSNAME);
                break;
            case TABS.CELEBRATE_EMOJI:
                toggleTabVisibility(celebrateTab, [likeTab, loveTab, insightTab, funnyTab, sparklesTab, hundredTab, allTab], headers[4], ACTIVE_TAB_CLASSNAME);
                break;
            case TABS.FUNNY_EMOJI:
                toggleTabVisibility(funnyTab, [likeTab, loveTab, insightTab, celebrateTab, sparklesTab, hundredTab, allTab], headers[5], ACTIVE_TAB_CLASSNAME);
                break;
            case TABS.SPARKLES_EMOJI:
                toggleTabVisibility(sparklesTab, [likeTab, loveTab, insightTab, celebrateTab, funnyTab, hundredTab, allTab], headers[6], ACTIVE_TAB_CLASSNAME);
                break;
            case TABS.HUNDRED_EMOJI:
                toggleTabVisibility(hundredTab, [likeTab, loveTab, insightTab, celebrateTab, funnyTab, sparklesTab, allTab], headers[7], ACTIVE_TAB_CLASSNAME);
                break;
          
        }
    }
};



/**
 * Handles the click event to toggle the reaction view and dim the screen,
 * and whether or not to display the reaction view container based on the show parameter
 * 
 * @param {Event} e - The click event object that triggered this function.
 * @param {boolean} [show=true] - Determines whether to show (true) or hide (false) 
 *                                the reaction container and whether to dim the screen. 
 *                                Defaults to true (show and dim).
 */
function handleToggleClick(e, show = true) {
    e.preventDefault();
    toggleSpinner();

    setTimeout(() => {
        toggleSpinner(false);
        showReactionContainer(show);
        toggleLightSwitch(show);
    }, NUM_OF_SECS_TO_DISPLAY);
}


/**
 * Toggles the visibility of the loading spinner.
 * This function controls whether the spinner element is displayed or hidden 
 * based on the 'show' parameter.
 * 
 * @param {boolean} [show=true] - Determines whether to show (true) or hide (false) 
 *                                the spinner. Defaults to true (show).
 */
function toggleSpinner(show = true) {
    spinner.style.display = show ? "block" : "none";
}


/**
 * Toggles the visibility of the emoji reaction container.
 * This function controls whether the reaction (likes) container is shown or hidden 
 * by adding or removing the "d-none" class, which controls its display.
 * 
 * @param {boolean} [show=true] - Determines whether to show (true) or hide (false) 
 *                                the reaction container. Defaults to true (show).
 */
function showReactionContainer(show=true) {
    if (show) {
        showEmojiLikeContainer.classList.remove("d-none");
        return;
    };

    showEmojiLikeContainer.classList.add("d-none");
  
}


/**
 * Toggles the background dimming effect.
 * This function controls whether the screen is dimmed or undimmed by setting the 
 * display of the dim background element.
 * 
 * @param {boolean} [dim=true] - Determines whether to dim (true) or undim (false) 
 *                               the background. Defaults to true (dim).
 */
function toggleLightSwitch(dim = true) {
    dimBackgroundElement.style.display = dim ? "block" : "none";
}



/**
 * Removes the scroll bar from the window which effectively
 * stops scrolling
 */
function showModal() {
    document.body.classList.add('modal-open'); 
}



/**
 * Adds the scroll bar in the current browser window which effectively
 * allows the user to scroll
 */
function removeModal() {
    document.body.classList.remove('modal-open'); 
}


