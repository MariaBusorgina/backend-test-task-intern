from django.urls import path, include
from rest_framework import routers

from shop.views import CategoryList, ProductList, BasketItemViewSet, BasketView


router = routers.DefaultRouter()
router.register(r'basket_item', BasketItemViewSet, basename='basket_item')

urlpatterns = [
    path('category/', CategoryList.as_view(), name='category'),
    path('products/', ProductList.as_view(), name='products'),
    path('basket_total/<int:pk>/', BasketView.as_view(), name='basket-detail'),
    path('', include(router.urls)),
]