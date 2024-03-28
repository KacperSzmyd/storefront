from django.shortcuts import render
from .tasks import notify_customers


def say_hello(request):
    notify_customers.delay('Hello')
    context = {"name": "Kacper"}
    return render(request, "hello.html", context)
