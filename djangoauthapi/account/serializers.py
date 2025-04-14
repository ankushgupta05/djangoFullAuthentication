from rest_framework import serializers
from account.models import User
from account.Utils import Util 
from rest_framework.exceptions import ValidationError


from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserRegistrationSerializer(serializers.ModelSerializer):
    # we are writing this bez we need confirm password field in our Registration Request
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields=['email','name','password','password2','tc']
        extra_kwargs={
            'password':{'write_only':True}
        }

    # Validating Password and Confirm Password while Registration
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")

        return attrs

    def create(self, validate_date):
        return User.objects.create_user(**validate_date)
    


class UserLoginViewSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']



class UserProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']



class UserChangePasswordSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(max_length=255, style={'input_type':'password'},write_only=True)
    password2  = serializers.CharField(max_length=255, style={'input_type':'password'},write_only=True)

    class Meta:
        model = User
        fields = ['password','password2']
        def validate(self,attrs):
            password = attrs.get('password')
            password2 = attrs.get('password2')
            print(password,password2)
            user = self.context.get('user')  # we get data from context
            if password != password2:
                raise serializers.ValidationError("password and Confirm password doesn't match")
            user.set_password(password)
            user.save()
            return attrs



class SendPasswordResetEmailViewSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email']
    
    def validate(self,attrs):
        email = attrs.get('email')
        print('yes\n\n')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded uid :- ',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token : ',token)
            # like = 'http://localhost:3000/api/user/reset/' + uid + '/' + token
            # like = 'http://localhost:5173/api/user/reset/' + uid + '/' + token
            link = f'http://localhost:5173/api/user/reset-password/{uid}/{token}'
            print('Password Reset Link : ',link)

            # code send email
            body = 'Click Follwing Link to Reset Your Password '+ link
            data = {
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email
            }
            print('test1')
            
            try:
                Util.send_email(data)
            except Exception as e:
                print("Email send failed:", e)

            # Util.send_email(data)
            print('test5')
            return attrs
        else:
            raise ValidationError('you are not a Registered User!')


    
class UserPasswordResetViewSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(max_length=255, style={'input_type':'password'},write_only=True)
    password2  = serializers.CharField(max_length=255, style={'input_type':'password'},write_only=True)

    class Meta:
        model = User
        fields = ['password','password2']
    def validate(self,attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            print('uid,token encoded :- ',uid,token)

            if password != password2:
                raise serializers.ValidationError("password and Confirm password doesn't match")

            id = smart_str(urlsafe_base64_decode(uid))
            print('uid Decoded :- ',uid)
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token): # check token with new created token of the same user 
                raise ValidationError('Token is not Valid or Expired!')

            user.set_password(password)
            user.save()
            return attrs

        
        # it provide more security and search more from chatgpt
        except  DjangoUnicodeDecodeError as identifier:  
            PasswordResetTokenGenerator.check_token(user,token)
            raise ValidationError('Token is not Valid or Expired!')