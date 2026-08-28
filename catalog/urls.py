from django.urls import path

from catalog import views as catalog

urlpatterns = [
    path("", catalog.ProductListView.as_view(), name="home"),
    path("contacts/", catalog.ContactListView.as_view(), name="contacts"),
    path("product_detail/<int:pk>/", catalog.ProductDetailView.as_view(), name="product_detail"),
    path("add_product/", catalog.ProductCreateView.as_view(), name="add_product"),
    path("update_product/<int:pk>/", catalog.ProductUpdateView.as_view(), name="update_product"),
    path("delete_product/<int:pk>/", catalog.ProductDeleteView.as_view(), name="delete_product"),
]
