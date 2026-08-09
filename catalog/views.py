from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def contacts(request):
    if request.method == "POST":
        return render(request, "contacts.html", {"message": "Данные отправлены"})
    return render(request, "contacts.html")