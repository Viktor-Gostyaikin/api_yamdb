from django.urls import include, path
from rest_framework import routers
from .views import ReviewViewSet, CommentViewSet


router = routers.DefaultRouter()

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


v1_patterns = [
    # path('', include('djoser.urls')),
    # path('', include('djoser.urls.jwt')),
    # path('', include(router_v1.urls)),
    # path('api-token-auth/', views.obtain_auth_token),
]
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
