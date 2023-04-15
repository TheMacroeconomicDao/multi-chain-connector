from rest_framework.routers import SimpleRouter

from api.wallet.viewsets import WalletViewSet

router = SimpleRouter()
router.register(r'wallets', WalletViewSet)

urlpatterns = [
    *router.urls
]
