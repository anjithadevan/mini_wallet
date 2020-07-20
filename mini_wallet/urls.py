from django.urls import include, path
from rest_framework import routers
from mini_wallet import views

router = routers.DefaultRouter()
router.register(r'wallet', views.WalletViewSet)
router.register(r'init', views.InitializeAccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
    ]