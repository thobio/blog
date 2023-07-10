from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import status

# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)
            if not serializer.is_valid():
                return Response(
                    {"data": serializer.errors, "message": "Sonthing Went Worng!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                serializer.save()
                return Response(
                    {"data": {}, "message": "Your accont is created"},
                    status=status.HTTP_201_CREATED,
                )
        except Exception as e:
            return Response(
                {"data": {str(e)}, "message": "Sonthing Went Worng!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if not serializer.is_valid():
                return Response(
                    {"data": serializer.errors, "message": "Sonthing Went Worng!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                response = serializer.get_jwt_token(serializer.data)
                return Response(
                    response,
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return Response(
                {"data": {str(e)}, "message": "Sonthing Went Worng!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
