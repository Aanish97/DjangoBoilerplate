import random
import string
from datetime import timedelta, datetime

from django.conf import settings
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer

__all__ = [
    'UserCreateView',
    'ForgotPasswordView',
    'ResetPasswordView',
]


class UserCreateView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):

    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Generate a random password reset token
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        user.reset_password_token = token
        user.save()

        # Send the password reset email
        subject = f"Password Reset from {settings.PROJECT_NAME}"
        message = f"Please click the following link to reset your password: {settings.FRONTEND_URL}/reset-password?token={token}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        return Response({"message": "Password reset instructions sent"}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):

    def post(self, request, token):
        try:
            user = User.objects.get(reset_password_token=token)
        except User.DoesNotExist:
            return Response({"detail": "Invalid reset token."}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('new_password')
        if new_password is None:
            return Response({"detail": "New Password not sent."}, status=status.HTTP_400_BAD_REQUEST)

        if not self.is_reset_token_valid(user):
            user.token_created_at = None
            user.save()
            return Response({"detail": "Reset token has expired."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.reset_password_token = None
        user.token_created_at = None
        user.save()

        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)

    def is_reset_token_valid(self, user, expiration_hours=2):
        """
        Token validation determined based on expiration time here
        """
        if user.token_created_at is None:
            return False

        # Calculate the token expiration time
        expiration_time = user.token_created_at + timedelta(hours=expiration_hours)
        current_time = datetime.now()

        return current_time.time() <= expiration_time.time()




