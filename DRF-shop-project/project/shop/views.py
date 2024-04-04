from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Category, Product, Basket, BasketItem
from .pagination import CategoryListPagination, ProductListPagination
from .serializers import CategorySerializer, ProductSerializer, BasketItemSerializer, \
    BasketViewSerializer


class CategoryList(ListAPIView):
    """Просмотр всех категорий с подкатегориями"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryListPagination


class ProductList(ListAPIView):
    """Просмотр продуктов"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductListPagination


class BasketItemViewSet(ModelViewSet):
    """Добавление, изменение (изменение количества), удаление продукта в корзине"""
    queryset = BasketItem.objects.all()
    serializer_class = BasketItemSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return BasketItem.objects.filter(basket__user=user)

    def create(self, request, *args, **kwargs):
        """Добавить продукт"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        basket = get_object_or_404(Basket, user=request.user)
        serializer.validated_data['basket'] = basket
        product_id =request.data['product']
        existing_item = basket.basket_item.filter(product_id=product_id).first()
        if existing_item:
            existing_item.quantity += serializer.validated_data['quantity']
            existing_item.save()
            serializer = self.get_serializer(existing_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """Изменить количество продукта в корзине"""
        partial = True
        instance = self.get_object()
        if int(request.data['quantity']) <= 0:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Очистить корзину"""
        queryset = self.get_queryset()
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BasketView(RetrieveAPIView):
    """Просмотр состава корзины с подсчетом общего количества товаров и общей стоимости"""
    queryset = Basket.objects.all()
    serializer_class = BasketViewSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return Basket.objects.filter(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)



