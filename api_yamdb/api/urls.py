from django.urls import include, path
from rest_framework import routers
from .views import ReviewViewSet, CommentViewSet, UserViewSet


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
]

urlpatterns = [
    path('v1/', include(v1_patterns)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),

]
