from .serializers import SignUpSerializer, PersonalDataSerializer
from rest_framework.generics import CreateAPIView, UpdateAPIView
from .models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

class SignUpAPIView(CreateAPIView):
    permission_classes = (AllowAny, )
    model = User
    serializer_class = SignUpSerializer


class VerifyCodeApiView(APIView):
    
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')
        self.check_verify_code(user, code)
        data = {
            "status" : True,
            "email": user.email,
            "auth_status" : user.auth_status, 
            "access" : user.token()["access"],
            "refresh" : user.token()["refresh"]
        }
        return Response(data)
        
        
    @staticmethod
    def check_verify_code(user, code):
        verify_code = user.verify_code_user.filter(code_lifitime__gte = datetime.now(), code = code, is_confirmed = False)
        
        if not verify_code.exists():
            
            data = {
                "status": False,
                "message" : "code unvalid"
            }
            print(data)
            raise ValidationError(data) 
        else : 
            verify_code.update(is_confirmed = True)
            
        if user.auth_status == "sentemail" :
            user.auth_status = "verify_code" 
            
            user.save()
            
        return True
            

class PersonalDataUpdateApiView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PersonalDataSerializer
    http_method_names = ['put', 'patch']
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        super(PersonalDataUpdateApiView, self).update(request, *args, **kwargs)
        
        data = {
            'status' : True,
            'message': 'you have registrated successfully',
            'auth_status' : self.request.user.auth_status
            
        }
        
        return Response(data)
    
    def partial_update(self, request, *args, **kwargs):
        super(PersonalDataUpdateApiView, self).partial_update(request, *args, **kwargs)
       
        data = {
            'status' : True,
            'message': 'you have registrated successfully',
            'auth_status' : self.request.user.auth_status
            
        }
        
        return Response(data)
