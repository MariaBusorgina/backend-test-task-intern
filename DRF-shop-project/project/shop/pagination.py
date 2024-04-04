from rest_framework.pagination import PageNumberPagination


class CategoryListPagination(PageNumberPagination):
    """Пагинация для списка категорий"""
    page_size = 15


class ProductListPagination(PageNumberPagination):
    """Пагинация для списка продуктов"""
    page_size = 10



