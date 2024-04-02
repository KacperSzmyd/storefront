from django.shortcuts import render
from django.core.cache import cache
from .tasks import notify_customers
import requests


def say_hello(request):
    key = "httpbin_result"
    if cache.get(key) == None:
        response = requests.get("https://httpbin.org/delay/2")
        data = response.json()
        cache.set(key, data)

    context = {
        "name": cache.get(key),
    }
    return render(request, "hello.html", context)
