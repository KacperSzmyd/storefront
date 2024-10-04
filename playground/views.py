from django.core.mail import EmailMessage, BadHeaderError
from django.db.models.aggregates import Count
from django.shortcuts import render
from rest_framework.views import APIView
import logging
import requests

logger = logging.getLogger(__name__)


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
class HelloView(APIView):
    def get(self, request):
        try:
            logger.info("Calling httpbin")
            response = requests.get("https://httpbin.org/delay/2")
            logger.info("Recieved the response")
            data = response.json()
        except request.ConnectionError:
            logger.critical("httpbin is offline")

        context = {
            "name": "Kacper",
        }
        return render(request, "hello.html", context)
