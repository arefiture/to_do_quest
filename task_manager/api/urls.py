from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from api.views import RegisterView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path(
        'register/', RegisterView.as_view(),
        name='register'
    ),
    path(
        'token/', jwt_views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'token/refresh/', jwt_views.TokenRefreshView.as_view(),
        name='token_refresh'
    )
]
urlpatterns += router.urls
