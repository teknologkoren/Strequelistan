from django.conf.urls import url, include
from rest_framework import routers
from api.views import UserViewSet, GroupViewSet, TransactionViewSet, PriceGroupViewSet, ProductViewSet, ProductCategoryViewSet, PriceLimitViewSet



router = routers.DefaultRouter()


router.register(r'user', UserViewSet)
router.register(r'group', GroupViewSet)
router.register(r'transaction', TransactionViewSet)
router.register(r'pricegroup', PriceGroupViewSet)
router.register(r'product', ProductViewSet)
router.register(r'productcategory', ProductCategoryViewSet)
router.register(r'pricelimit', PriceLimitViewSet)




urlpatterns = [

    url(r'^', include(router.urls)),

    ]