from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from catalog.form import ProductForm
from catalog.models import Product, Contact


def home(request):
    products = Product.objects.all()

    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")
    products_page = paginator.get_page(page_number)

    return render(
        request,
        "home.html",
        {"products": products_page},
    )


def contacts(request):
    if request.method == "POST":
        return render(request, "contacts.html", {"message": "Данные отправлены"})
    return render(request, "contacts.html", {"contacts": Contact.objects.all()})


def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, "product_details.html", {"product": product})


def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ProductForm()

    return render(request, "add_product.html", {"form": form})