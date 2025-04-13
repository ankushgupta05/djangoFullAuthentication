from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from account.serializers import UserRegistrationSerializer,UserLoginViewSerializer
from django.contrib.auth import authenticate
# from account.renderers import UserRenderer
from account.renderers import UserRenderer

# Create your views here.



class UserRegistrationView(APIView):
    renderer_class = [UserRenderer]
    def post(self, request, formate=None):
        serializer = UserRegistrationSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True): # raise_exception=True if we write then  "serializer.errors" this line will not execute
        # if serializer.is_valid():  
            user = serializer.save()
            return Response({'msg':'Ragistration Succesfully!'},status = status.HTTP_201_CREATED)

        print(serializer.errors)  # display error  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(APIView):
    renderer_class = [UserRenderer]
    def post(self,request,formate=None):
        serializer = UserLoginViewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)  # email and password if match then give the user detailed
            if user is not None:
                return Response({'msg':'Login Succesfully!'},status = status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['email or password is not valid']}},status = status.HTTP_404_NOT_FOUND)


        return  Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)