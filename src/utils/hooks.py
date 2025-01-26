import logging

logger = logging.getLogger('custom_logger')


def process_email_result(result):
    """
    A private function to be called after django-q has executed its task.
    This is the hook function that gets called once the task is completed.

    Parameters:
        - result: The result of the task execution (could be True/False or an exception message).

    Returns:
        - bool: True if email was successfully sent, False otherwise, or a string if error message is returned.
    """
    
    is_sent      = False
    SUCCESS_MSG  = "The user's email processing result:"

    if result is True:
        logger.info(f"{SUCCESS_MSG} Email sent successfully.")
        is_sent = True
        
    elif result is False:
        logger.warning(f"{SUCCESS_MSG} Email sending failed. No specific error message provided.")
        
    # If result is a string (error or message)
    elif isinstance(result, str):
        if "failed" in result.lower() or "error" in result.lower():
            
            logger.error(f"{SUCCESS_MSG} Task failed with message: {result}")
        else:
            
            logger.info(f"{SUCCESS_MSG} Task completed with message: {result}")
            is_sent = True  
        

    else:
        logger.error(f"{SUCCESS_MSG} Unexpected result type: {result}")
    
    return is_sent 
