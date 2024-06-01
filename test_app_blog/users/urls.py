from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsersViewSet

router = DefaultRouter()
router.register(r'avatar', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
