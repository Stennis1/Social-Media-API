from django.urls import path, include 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PostViewSet, CommentViewSet, LikeViewSet
from . import views

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)

# Customized JWT Token authentication views/responses
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/password_reset/', views.password_reset_request, name='password_reset'),
    path('api/reset/<uidb64>/<token>/', views.password_reset_confirm, name='passwword_reset_confirm'),
    path('', include(router.urls)),
]
