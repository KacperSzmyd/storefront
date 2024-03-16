from django.urls import include, path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("collections", views.CollectionViewSet)
router.register("carts", views.CartViewSet)
router.register("customers", views.CustomerViewSet)
router.register("orders", views.OrderViewSet, basename="orders")

products_router = routers.NestedDefaultRouter(router, r"products", lookup="product")
products_router.register("reviews", views.ReviewViewSet, basename="products-reviews")

carts_router = routers.NestedDefaultRouter(router, r"carts", lookup="cart")
carts_router.register("items", views.CartItemViewSet, basename="cart-items")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(products_router.urls)),
    path("", include(carts_router.urls)),
]
