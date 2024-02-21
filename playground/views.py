from django.db.models.aggregates import Count
from django.shortcuts import render
from store import models


def say_hello(request):
    customers = models.Customer.objects.all().annotate(orders=Count("order__id"))
    context = {"name": "Kacper", "result": customers}
    return render(request, "hello.html", context)
