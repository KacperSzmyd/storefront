from django.db.models.aggregates import Count

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework import status

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


@api_view(["GET", "POST"])
def collection_list(request):
    if request.method == "GET":
        queryset = Collection.objects.annotate(products_count=Count("products")).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(products_count=Count("products")), pk=pk
    )
    if request.method == "GET":
        serializer = CollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        if collection.products.count() > 0:
            return Response(
                {
                    "error": "cannot delete collection due to association to other products"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductList(ListCreateAPIView):
    def get(self, request):
        queryset = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response(
                {
                    "error": "Product cannot be deleted due to beeing associatied with an other item"
                }
            )
        else:
            product.delete
            return Response(status=status.HTTP_204_NO_CONTENT)
