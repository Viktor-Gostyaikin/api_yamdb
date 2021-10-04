from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

# from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router_v1 = routers.DefaultRouter()

v1_patterns = [
    # path('', include('djoser.urls')),
    # path('', include('djoser.urls.jwt')),
    # path('', include(router_v1.urls)),
    # path('api-token-auth/', views.obtain_auth_token),
]
urlpatterns = [
    path('v1/', include(v1_patterns)),
]