from django.shortcuts import render
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from store.models import Product, OrderItem, Order, Collection


def say_hello(request):
    # query_set = Product.objects.values_list("id", "title", "collection__title")

    number_of_orders = Order.objects.aggregate(count=Count("id"))
    product_1_sold = OrderItem.objects.filter(id=1).aggregate(
        units_sold=Sum("quantity")
    )
    customer_1_orders = Order.objects.filter(customer__id=1).aggregate(
        count=Count("id")
    )
    collection3 = Collection.objects.filter(id=3).aggregate(
        min=Min("product__unit_price"),
        max=Max("product__unit_price"),
        avg=Avg("product__unit_price"),
    )

    context = {
        "name": "Kacper",
        "orders": number_of_orders,
        "product1": product_1_sold,
        "customer1": customer_1_orders,
        "collection": collection3,
    }

    return render(request, "hello.html", context)
