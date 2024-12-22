
from rest_framework import serializers
from .models import User
from api.base.utility import check_email, send_email, cheak_username
from rest_framework.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.contrib.auth.password_validation import validate_password



class SignUpSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'id', 
            'auth_status', 
            'email',
            'auth_type'
        )

        extra_kwargs = {
            'auth_status' : {'read_only' : True, 'required' : False}
        }

    
    def create(self, validated_data):
        validated_data['auth_type'] = validated_data.get('auth_type', 'email')
        user = super().create(validated_data)
        code = user.create_code()
        send_email(user.email, code)
        return user
    
    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.token())
        return data

class PersonalDataSerializer(serializers.Serializer):
    
    frist_name = serializers.CharField(write_only = True, required = True)
    last_name = serializers.CharField(write_only = True, required = True)
    username = serializers.CharField(write_only = True, required = True)
    photo = serializers.ImageField(validators = [
      FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'heic', 'heif'])
    ])
    password = serializers.CharField(write_only = True, required = True)
    confirm_password = serializers.CharField(write_only = True, required = True)
    
    def validate(self, data):
        password = data.get('password', None)
        confirm_password = data.get('confirm_password')
        
        if password != confirm_password:
            data = {
                'status': False,
                "message": "the two passwords are not same"
            }
            raise ValidationError(data)
        if password:
            validate_password(password)
            # validate_password(confirm_password)
        
        return data
    
    def validate_username(self, username):
        
        if not cheak_username(username):
            data ={
                "status":False,
                "message" : "The username is unvalid  ",
            }
            raise ValidationError(data)
        
        if  User.objects.filter(username=username).exists():
            
            data = {
                "status":False,
                "message" : "The username is chosen",
            }
            raise ValidationError(data)
            
        return username
    
    def update(self, instance, validated_data):
       
       instance.first_name = validated_data.get('frist_name', instance.first_name)
       instance.last_name = validated_data.get('last_name', instance.last_name)
       instance.username = validated_data.get('username', instance.username)
       instance.password = validated_data.get('password', instance.password)
       
       if validated_data.get('password'):
           instance.set_password(validated_data.get('password'))
           
       instance.photo = validated_data.get('photo', instance.photo)
       if instance.auth_status =='verify_code':
           instance.auth_status = 'complete'
       
       instance.save()
       return instance
