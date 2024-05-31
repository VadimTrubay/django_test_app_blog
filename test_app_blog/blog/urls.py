from django.urls import path
from .views import ArticleViewSet, SubscribeView

urlpatterns = [
    path('articles/', ArticleViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
]


# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ArticleViewSet
#
# router = DefaultRouter()
# router.register(r'articles', ArticleViewSet)
#
# urlpatterns = [
#     path('', include(router.urls)),
# ]
