from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import ReviewViewSet, CommentViewSet, UserViewSet, GetTokenView, create_auth_user


router_v1 = routers.DefaultRouter()


router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register(r'users', UserViewSet)


v1_patterns = [
    path('', include(router_v1.urls)),
    path('auth/signup/', create_auth_user, name='signup'),
    path('auth/token/', GetTokenView.as_view(), name='token_obtain_pair'),
]
urlpatterns = [
    path('v1/', include(v1_patterns)),
]
