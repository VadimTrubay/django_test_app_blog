from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, SubscribeView

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
]
