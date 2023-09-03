from django.urls.conf import path, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import (
    UserCreateView,
    ForgotPasswordView,
    ResetPasswordView
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create/', UserCreateView.as_view(), name='user-create'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    re_path(r'^password-reset/(?P<token>[\w-]+)/$', ResetPasswordView.as_view(), name='password-reset'),

]
