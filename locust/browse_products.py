from locust import HttpUser, task, between
from random import randint


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task(3)
    def view_products(self):
        collection_id = randint(3, 6)
        self.client.get(
            f"/store/products/?collection_id={collection_id}", name="/store/products"
        )

    @task(7)
    def view_product(self):
        product_id = randint(1, 1000)
        self.client.get(f"/store/products/{product_id}", name="/store/products/:id")

    @task(1)
    def add_to_cart(self):
        product_id = randint(1, 15)
        self.client.post(
            f"/store/carts/{self.cart_id}/items/",
            name="store/carts/items",
            json={
                "product_id": product_id,
                "quantity": product_id + 1,
            },
        )

    @task
    def playground_hello(self):
        self.client.get("/playground/hello/")

    def on_start(self):
        response = self.client.post(f"/store/carts/")
        result = response.json()
        self.cart_id = result["id"]
