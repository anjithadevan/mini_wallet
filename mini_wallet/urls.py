from django.urls import include, path
from rest_framework import routers
from mini_wallet import views

router = routers.DefaultRouter()
router.register(r'wallet/deposits', views.AddvirtualMoneyViewSet)
router.register(r'wallet/withdrawals', views.WithdrawVirtualMoneyViewSet)
router.register(r'init', views.InitializeAccountViewSet, basename='init')

urlpatterns = [
    path('', include(router.urls)),
    path('wallet', views.WalletView.as_view()),
]
