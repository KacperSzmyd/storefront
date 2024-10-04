from django.core.mail import EmailMessage, BadHeaderError
from django.db.models.aggregates import Count
from django.shortcuts import render
from store import models


def say_hello(request):
    try:
        message = EmailMessage(
            "dummy subject",
            "Lorem Ipsum",
            "kacper@storefront.pl",
            ["user1@domain.com", "user2@domain.com"],
        )
        message.attach_file("playground/static/images/randompic.jpg")
        message.send()
    except BadHeaderError:
        pass

    customers = models.Customer.objects.all().annotate(orders=Count("order__id"))
    context = {"name": "Kacper", "result": customers}
    return render(request, "hello.html", context)
