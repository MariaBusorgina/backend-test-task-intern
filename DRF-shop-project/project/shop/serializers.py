from rest_framework import serializers

from shop.models import Category, Subcategory, Product, BasketItem, Basket


class SubcategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcategory
        fields = ('title', 'slug', 'image',)


class CategorySerializer(serializers.ModelSerializer):
    subcategory = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('title', 'slug', 'image', 'subcategory',)


class ProductSerializer(serializers.ModelSerializer):
    subcategory_title = serializers.CharField(source='subcategory.title')
    category_title = serializers.CharField(source='subcategory.category.title')
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('title', 'slug', 'price', 'images', 'subcategory_title', 'category_title',)

    def get_images(self, obj):
        base_url = 'http://' + self.context.get('request').get_host()
        image_fields = ['image_one', 'image_second', 'image_three']
        images = []
        for field in image_fields:
            image = getattr(obj, field)
            if image:
                images.append(base_url + image.url)
        return images


class BasketItemSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(write_only=True)
    products = ProductSerializer(read_only=True)

    class Meta:
        model = BasketItem
        fields = ('id', 'price', 'quantity', 'product', 'products')
        read_only_fields = ('price', 'products')

    def create(self, validated_data):
        product_id = validated_data.get('product')
        product = Product.objects.get(id=product_id)
        validated_data['product'] = product
        validated_data['price'] = product.price
        instance = BasketItem.objects.create(**validated_data)
        return instance

    def update(self, instance, validate_data):
        quantity = validate_data.get('quantity')
        instance.quantity = quantity
        instance.save()
        return instance


class BasketViewSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    total_price = serializers.ReadOnlyField(source='all_total_price')
    total_quantity = serializers.ReadOnlyField(source='all_total_number')

    class Meta:
        model = Basket
        fields = ('user', 'total_price', 'total_quantity', 'products')

    def get_products(self, obj):
        basket_items = obj.basket_item.all()
        product_titles = [item.product.title for item in basket_items]
        return product_titles





