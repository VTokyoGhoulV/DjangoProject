from django.urls import path

from catalog import views as catalog

urlpatterns = [
    path("", catalog.ProductList.as_view(), name="home"),
    path("contacts/", catalog.ContactView.as_view(), name="contacts"),
    path("product_detail/<int:pk>/", catalog.ProductDetail.as_view(), name="product_detail"),
    path("add_product/", catalog.CreateProduct.as_view(), name="add_product"),
]
