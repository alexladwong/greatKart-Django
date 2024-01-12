from django.shortcuts import render
from estores.models import *


# Create your views here.
def Home(request):
    products = Products.objects.all().filter(is_available=True)

    context = {
        "products": products,
    }
    return render(request, "store/index.html", context)
