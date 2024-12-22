from enum import Enum

class AuthType(Enum):
    Google = "google"
    Email = "email"
    
    @classmethod
    def choices(cls):
        return tuple((key.value, key.name) for key in cls)
    
    
class AuthStatus(Enum):
    Sent_email = "sentemail"
    Verify_code = "verify_code"
    Complete = "complete"
    
   
    
    @classmethod
    def choices(cls):
        return tuple((key.value, key.name) for key in cls)