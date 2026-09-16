from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from catalog.form import ProductForm
from catalog.models import Product, Contact


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    queryset = Product.objects.order_by("pk")
    template_name = "home.html"
    context_object_name = "products"
    paginate_by = 6


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = "contacts.html"
    context_object_name = "contacts"

    def post(self, request):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context["message"] = "Данные отправлены"

        return render(request, self.template_name, context)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "product_details.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "product_create.html"
    form_class = ProductForm
    success_url = reverse_lazy("home")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = "product_update.html"
    form_class = ProductForm
    success_url = reverse_lazy("home")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "product_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("home")
