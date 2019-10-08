from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template


def home_page(request):
    title = "Hello there..."
    context = {"title": title, "my_list": [1, 2, 3, 4]}
    return render(request, "home.html", context)

def about_page(request):
    title = "About us"
    context = {"title": title}
    return render(request, "about.html", context)

def contact_page(request):
    title = "Contact us"
    context = {"title": title}
    return render(request, "hello_world.html", context)
