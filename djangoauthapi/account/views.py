from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from account.serializers import UserRegistrationSerializer,UserLoginViewSerializer,UserProfileViewSerializer,UserChangePasswordSerializer,SendPasswordResetEmailViewSerializer, UserPasswordResetViewSerializer

from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated

# Create your views here.



# Genrate Tokens Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_class = [UserRenderer]
    def post(self, request, formate=None):
        serializer = UserRegistrationSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True): # raise_exception=True if we write then  "serializer.errors" this line will not execute
        # if serializer.is_valid():  
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({"token":token,'msg':'Ragistration Succesfully!'},status = status.HTTP_201_CREATED)

        print(serializer.errors)  # display error  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(APIView):
    # renderer_class = [UserRenderer]
    def post(self,request,formate=None):
        serializer = UserLoginViewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)  # email and password if match then give the user detailed
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({"token":token,'msg':'Login Succesfully!'},status = status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['email or password is not valid']}},status = status.HTTP_404_NOT_FOUND)


        return  Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)




class UserProfileView(APIView):
    renderer_class = [UserRenderer]
    permission_classes = [IsAuthenticated]  # This need token for process
    def get(self,request,formate=None):
        serializer = UserProfileViewSerializer(request.user)   # server process the token and automatic find user and send user data
        return Response (serializer.data, status=status.HTTP_200_OK)
        

        
class UserChangePasswordView(APIView):
    renderer_class = [UserRenderer]
    permission_classes = [IsAuthenticated]  # This need token for process
    def post(self,request,formate=None):
        serializer = UserChangePasswordSerializer(data = request.data, context={'user':request.user})  # also send the user data using context
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Change Successfully!!'},status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class SendPasswordResetEmailView(APIView):
    renderer_class=[UserRenderer]
    def post(self,request,formate=None):
        serializer = SendPasswordResetEmailViewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset link send. Plesae check your Email!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class UserPasswordResetView(APIView):
    renderer_class=[UserRenderer]
    def post(self,request,uid, token, formate=None):
        serializer = UserPasswordResetViewSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        pass
