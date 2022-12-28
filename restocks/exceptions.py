class LoginException(Exception):

    """
    Base Exception for possible login attempt errors.
    """

class SessionException(Exception):
    
    """
    Base Exception for possible errors while logged in.
    """
    
class RequestException(Exception):
    
    """
    Base Exception for general request errors.
    """