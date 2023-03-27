from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AdminAPI, RegistrationAPI, TokenAPI,
                    UserMePatchView)


router_v1 = DefaultRouter()
router_v1.register('users', AdminAPI)

urlpatterns = [
    path('v1/users/me/', UserMePatchView.as_view()),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', RegistrationAPI.as_view()),
    path('v1/auth/token/', TokenAPI.as_view()),
]
