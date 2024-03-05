from django.urls import include, path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("collections", views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(router, r"products", lookup="product")
products_router.register("reviews", views.ReviewViewSet, basename="products-reviews")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(products_router.urls)),
]
