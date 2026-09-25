from django.core.cache import cache

from catalog.models import Product, Category

CACHE_TTL = 60 * 15

class ProductService:

    @staticmethod
    def get_products_by_category(category_id):

        key = f"category_{category_id}"
        products = cache.get(key)

        if products is None:
            products = Product.objects.filter(category_id=category_id).order_by("pk")
            cache.set(key, products, CACHE_TTL)

        return products
