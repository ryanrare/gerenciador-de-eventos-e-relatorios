from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView

from .serializers import UserSerializer
from .models import User

import datetime
import jwt


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            raise AuthenticationFailed('Unable to log in with the data provided')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=360),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response
