from django.urls import path
from api.accounts.views import SignUpAPIView, VerifyCodeApiView, PersonalDataUpdateApiView

urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    path('verify-code/', VerifyCodeApiView.as_view(), name='verify_code'),
    path('personal-data/', PersonalDataUpdateApiView.as_view(), name='personal_data'),
]

