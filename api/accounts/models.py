from django.db import models
from django.contrib.auth.models import AbstractUser
from api.base.models import BaseModel
from api.base.enum import AuthType, AuthStatus
from django.core.validators import FileExtensionValidator
import uuid
import random
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
 
class User(AbstractUser, BaseModel):
    
    auth_type = models.CharField(max_length=6, choices=AuthType.choices(), null = True, blank = True)
    auth_status = models.CharField(max_length=25, choices=AuthStatus.choices(), default = 'sentemail')
    email = models.EmailField(null=True, blank=True, unique=True)
    photo =models.ImageField(upload_to="uploads/", null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'heic', 'heif'])
    ])

    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    
    def cheack_username(self):
        if not self.username:
            test_username = f"user-{uuid.uuid4().__str__().split('-')[1]}"
            while User.objects.filter(username = test_username):
                test_username = f"{test_username}{random.randint(0, 9)}"
            self.username = test_username


 
    def cheack_email(self):
        if self.email:
            test_email = self.email.lower()
            self.email = test_email

    def cheack_password(self):
        if not self.password:
            test_pasword = f"'password'{uuid.uuid4().__str__().split('-')[1]}"
            self.password = test_pasword
            
    def hesh_password(self):
        if not self.password.startswith("pbkdf2_sha256"):
            self.set_password(self.password)
        

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            'refresh' : str(refresh)
        }
     
     
    def create_code(self):
        code = "".join([str(random.randint(0, 10) %10) for _ in range(6)]) 
        
        UserConfirmationCode.objects.create(
            user = self, 
            code = code
        )  
        
        return code
    
    
    
    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(*args, **kwargs)
    
    
    def clean(self):

        self.cheack_username()
        self.cheack_email()
        self.cheack_password()
        self.hesh_password()
        

CODE_LIFETIME = 3
     
class UserConfirmationCode(BaseModel):
    
    code = models.CharField(max_length = 6)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'verify_code_user')
    code_lifitime = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default = False)
    
    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        self.code_lifitime = datetime.now() + timedelta(minutes=CODE_LIFETIME)
        super(UserConfirmationCode, self).save(*args, **kwargs)
        
    
        