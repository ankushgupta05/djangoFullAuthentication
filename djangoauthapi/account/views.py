from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.



class UserRegistrationView(APIView):
    def get(self, request, formate=None):
        print('ankushgupta')
        return Response({'msg':'Ragistration Succesfully!'})

