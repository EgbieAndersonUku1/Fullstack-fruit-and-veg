from types import NoneType
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from typing import Optional
from requests import RequestException

import logging

logger = logging.getLogger("custom_logger")

def send_email(subject:str, 
               from_email:str, 
               to_email:str, 
               email_template:str, 
               text_template:Optional[str]=None, 
               context: dict = None) -> bool:
    """
    Send an email with both HTML and plain text content.

    Args:
        subject (str): The subject of the email.
        from_email (str): The sender's email address.
        to_email (str): The recipient's email address.
        email_template (str): The path to the HTML template file.
        text_template (str, optional): The path to the plain text template file.
        context (dict): The context dictionary for rendering the templates.
     
    Returns:
        None
    """
    
    html_content = render_to_string(email_template, context)
    
    if text_template:
        text_content = render_to_string(text_template, context)
    else:
        text_content = ''

    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        
        resp = msg.send()
        if resp:
            logger.info(f"Successful sent email to user with email: {to_email}")
        else:
            logger.critical(f"Failed to sent email to user with email: {to_email}")
        return resp
    
    except RequestException as e:
        logger.error(f"Network error while sending email to {to_email}: {str(e)}")
        return f"Network error: {str(e)}"
    
    except Exception as e:
        logger.error(f"General error received while trying to sent an email to user with email: {to_email}")
        return f"Failed to send email: {e}"
        
    except NoneType as e:
        logger.error(f"Unspecified error received while sending email to {to_email}: {str(e)}")
        
    return False