from django.shortcuts import render

from catalog.models import Product, Contact


def home(request):
    print(Product.objects.all().order_by("created_at").reverse()[:5])
    return render(request, "home.html")


def contacts(request):
    if request.method == "POST":
        return render(request, "contacts.html", {"message": "Данные отправлены"})
    return render(request, "contacts.html", {"contacts": Contact.objects.all()})