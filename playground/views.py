from django.shortcuts import render


def say_hello(request):
    context = {"name": "Kacper", "result": "queryset_placeholder"}
    return render(request, "hello.html", context)
