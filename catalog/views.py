from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from catalog.form import ProductForm
from catalog.models import Product, Contact, Category
from catalog.services import ProductService


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    queryset = Product.objects.order_by("pk")
    template_name = "home.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        user = self.request.user
        category_id = self.request.GET.get("category")

        if category_id:
            products = ProductService.get_products_by_category(category_id)

            if user.has_perm("catalog.can_unpublish_product"):
                return products

            return [
                product for product in products
                if product.published or product.owner == user
            ]

        queryset = super().get_queryset()

        if user.has_perm("catalog.can_unpublish_product"):
            return queryset

        return queryset.filter(Q(published=True) | Q(owner=user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = "contacts.html"
    context_object_name = "contacts"

    def post(self, request):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context["message"] = "Данные отправлены"

        return render(request, self.template_name, context)


@method_decorator([cache_page(60 * 15), vary_on_cookie], name="dispatch")
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "product_details.html"
    context_object_name = "product"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.has_perm("catalog.can_unpublish_product"):
            return queryset

        return queryset.filter(
            Q(published=True) | Q(owner=user)
        )


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "product_create.html"
    form_class = ProductForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = "product_update.html"
    form_class = ProductForm
    success_url = reverse_lazy("home")

    def test_func(self):
        product = self.get_object()
        user = self.request.user

        return (
                product.owner_id == user.pk
                or user.has_perm("catalog.change_product")
        )


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "product_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("home")

    def test_func(self):
        product = self.get_object()
        user = self.request.user

        return product.owner_id == user.pk or user.has_perm("catalog.delete_product")


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "catalog.can_unpublish_product"

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.published = False
        product.save()

        return redirect("home")
