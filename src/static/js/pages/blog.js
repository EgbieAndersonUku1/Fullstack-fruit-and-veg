import splitStringByDelimiter from "../utils/parser.js";
import { validateElement } from "../errors/customErrors.js";


const spinner        = document.querySelector(".small-spinner");
const commentSection = document.getElementById("comments-section");


commentSection?.addEventListener("click", handleComment);


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
        clearDiv(replyFormDiv);
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
            spinner.style.display = "none";
            replyForm.style.display = show ? "block" : "";

            toggleReplyLinkText(replyLink, show);

        }, NUM_OF_SECS_TO_DISPLAY);
    };
};


function toggleReplyLinkText(replyLink, showClosMsg=true) {
    replyLink.innerText = showClosMsg ? "Close Reply" : "Reply";

}


function clearDiv(divToClear) {
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

    form.id            = attrs.id
    form.action        = attrs.action;
    form.method        = attrs.method || "post";
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

