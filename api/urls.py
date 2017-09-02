from django.conf.urls import url, include
from rest_framework import routers
from api import views


router = routers.DefaultRouter()


router.register(r'group', views.GroupViewSet)
router.register(r'pricegroup', views.PriceGroupViewSet)
router.register(r'pricelimit', views.PriceLimitViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'productcategory', views.ProductCategoryViewSet)
router.register(r'quote', views.QuoteViewSet)
router.register(r'transaction', views.TransactionViewSet)
router.register(r'user', views.UserViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]