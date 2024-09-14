from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from core.models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import RegistrationSerializer
class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            try:
                account = serializer.save()
                if account:
                    data['username'] = account.username
                    data['email'] = account.email
                    token = Token.objects.get(user=account).key
                    data['token'] = token
                    data['response'] = "Successfully registered a new user."
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Account creation failed."}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
