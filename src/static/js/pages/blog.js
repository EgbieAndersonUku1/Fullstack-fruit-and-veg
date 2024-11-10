import splitStringByDelimiter from "../utils/parser.js";
import { validateElement } from "../errors/customErrors.js";
import { calculateDistanceBetweenTwoPoints } from "../utils/distanceUtils.js";


const spinner           = document.querySelector(".small-spinner");
const commentSection    = document.getElementById("comments-section");
const blogContainer     = document.querySelector(".blog-interactions");
const reactionEmojisDiv = document.querySelector(".user-reactions-choices");
const reactionEmojiPTag = document.querySelector(".reaction-emoji-name p");
const numOfLikes        = document.querySelector(".num-of-likes");
const thumbsUpLink      = document.querySelector(".thumbs-up").closest("a");
const thumbsUpIcon      = document.querySelector(".thumb-up-icon");


// validate elements
validateElement(numOfLikes, "This is not a valid HTML element");
validateElement(thumbsUpLink, "This is not a valid element ");


// Event listeners
commentSection?.addEventListener("click", handleComment);
reactionEmojisDiv.addEventListener("click", handleEmojiClick);
thumbsUpLink.addEventListener("click", handleThumbsUpToggle);


thumbsUpIcon?.classList.add("bounce");


// const values
const FLY_CLASS = "fly";

const EMOJIS_ATTRS = {
    likeIcon: { color: "royalblue", name: "like" },
    loveIcon: { color: "red", name: "love" },
    insightIcon: { color: "orange", name: "insight" },
    funnyIcon: { color: "pink", name: "funny" },
    celebrateIcon: { color: "green", name: "celebrate" },
    sparklesIcon: { color: "gold", name: "sparkles" },
    hundredIcon: { color: "purple", name: "hundred" }
};


function handleComment(e) {
   const replyLinkDiv = e.target.closest(".author-comment .reply-link-div");
     
    if (replyLinkDiv) {
        handleReplyLinkClick(e); 
    };
}


function handleReplyLinkClick(e) {
    e.preventDefault();

    const ANCHOR_TAG = "A";

    if (e.target.nodeName == ANCHOR_TAG) {

        const replyLink = e.target;

        const replyFormDivID = replyLink.dataset.replyBoxId;
        const replyFormDiv   = document.getElementById(replyFormDivID);

        validateElement(replyFormDiv, "Reply Form Div is not a valid HTML instance", true);

        const replyFormId  = `reply-form${splitStringByDelimiter(replyFormDiv.id)[1]}`;
        const replyForm    = createReplyForm(replyFormId);
        
        if (!replyForm) {
            throw new Error(`Expected a reply form but received <${replyForm}>`)
        }
        clearElement(replyFormDiv);
        replyFormDiv.appendChild(replyForm);
             
        const show = replyFormDiv.style.display === "" ? true : false;
        toggleReplyForm(replyFormDiv, replyLink, show);
        
    }
    
}


function toggleReplyForm(replyForm, replyLink, show = true) {

    const NUM_OF_SECS_TO_DISPLAY = 1000;

    if (replyForm) {
        spinner.style.display = "block";

        setTimeout(() => {
            spinner.style.display   = "none";
            replyForm.style.display = show ? "block" : "";

            toggleReplyLinkText(replyLink, show);

        }, NUM_OF_SECS_TO_DISPLAY);
    };
};


function toggleReplyLinkText(replyLink, showClosMsg=true) {
    replyLink.innerText = showClosMsg ? "Close Reply" : "Reply";

}


function clearElement(divToClear) {
    divToClear.innerHTML = ""
}


function createReplyForm(formID) {
 
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
                                                  placeholder:"Add a reply..",
                                                 },
                                     setterFunc: setFormElementAttributes,
                                 });
    
    const replyButton = createElement({ elementToCreate: "button",
                                        attrsToSet: {type: "submit",
                                                     className: ["text-capitalize",  "button-sm", "comment-btn", "dark-green-bg"],
                                                     innerText: "reply"
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


function setFormAttributes(form, attrs ) {

    form.id      = attrs.id
    form.action  = attrs.action;
    form.method  = attrs.method || "post";
    return form;
};


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


function createElement({elementToCreate, attrsToSet={}, setterFunc}) {
    const element = document.createElement(elementToCreate);
  
    try {
        return setterFunc(element, attrsToSet);
    } catch (error) {
        console.error(`Something went wrong creating element - ${JSON.stringify(error.message)}`);
        
    }
}


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


function removeFlyClass() {
    const reactionEmojis = document.querySelectorAll(".reaction-icon");

    reactionEmojis.forEach((reactionEmoji) => {
        reactionEmoji.classList.remove(FLY_CLASS);
    });
}


function setReactionEmoji(identifier) {
    clearElement(reactionEmojiPTag);
    const identifierObject = EMOJIS_ATTRS[identifier];
  

    if (identifierObject !== "undefined") {

        reactionEmojiPTag.innerText   = identifierObject["name"];
        const color                   = identifierObject["color"];
        reactionEmojiPTag.style.color = color;
    }
   
}


function updateLikes() {
    const numOfLikesString = numOfLikes?.lastChild?.textContent;

    if (numOfLikesString) {
       
        const likesString = numOfLikesString.split(" ")[1];
        const likes = parseInt(likesString, 10);
    
        if (!isNaN(likes)) {
           
            const updatedLikes = likes + 1;
          
            numOfLikes.lastChild.textContent = updatedLikes === 1 ? ` ${updatedLikes} like` : ` ${updatedLikes} likes`;
            console.log(numOfLikesString);
        }
    }
}


function handleThumbsUpToggle(e) {
    e.preventDefault();

    spinner.style.display        = "block";
    const NUM_OF_SECS_TO_DISPLAY = 1000;

    setTimeout(() => {

        spinner.style.display           = "none";
        const status                    = reactionEmojisDiv.style.display;
        reactionEmojisDiv.style.display = status === "grid" ? "" : "grid";
        thumbsUpLink.style.color        = status === "grid" ? "black"  : "blue";
        
        if (status === "grid") {
            clearElement(reactionEmojiPTag);
        }
    }, NUM_OF_SECS_TO_DISPLAY);
}

