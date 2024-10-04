from rest_framework import status
from model_bakery import baker
import pytest

from store.models import Product


@pytest.fixture
def create_product(api_client):
    def do_create_product(
        product={
            "title": "",
            "slug": "",
            "unit_price": 0,
            "inventory": 0,
            "collection": "",
        }
    ):
        return api_client.post("/store/products/", product)

    return do_create_product


@pytest.fixture
def update_product(api_client):
    def do_update_product(
        value={
            "title": "a",
            "slug": "a",
            "unit_price": 2,
            "inventory": 2,
            "collection": "1",
        }
    ):
        product = baker.make(Product)

        return api_client.patch(f"/store/products/{product.id}/", value)

    return do_update_product


@pytest.fixture
def delete_product(api_client):
    def do_delete_product():
        product = baker.make(Product)
        return api_client.delete(f"/store/products/{product.id}/")

    return do_delete_product


@pytest.mark.django_db
class TestCreateProduct:

    def test_if_user_is_anonymus_returns_401(self, create_product):
        response = create_product()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_an_admin_returns_403(self, authenticate, create_product):
        authenticate()
        response = create_product()

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_product):
        authenticate(is_staff=True)
        response = create_product()

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, authenticate, create_product):
        authenticate(is_staff=True)
        response = create_product(
            {
                "title": "a",
                "slug": "a",
                "unit_price": 2,
                "inventory": 2,
                "collection": "1",
            }
        )

        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestRetrieveProduct:
    def test_if_product_exists_returns_200(self, api_client):
        product = baker.make(Product)

        response = api_client.get(f"/store/products/{product.id}/")

        assert response.status_code == status.HTTP_200_OK

    def test_if_product_not_exist_return_404(self, api_client):
        response = api_client.get("/store/products/a/")

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateProduct:
    def test_if_user_is_anonymus_returns_401(self, update_product):
        response = update_product()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, update_product):
        authenticate()

        response = update_product()

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, update_product):
        authenticate(is_staff=True)

        response = update_product({"unit_price": 0})
        assert response.data["unit_price"] is not None

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_correct_returns_200(self, authenticate, update_product):
        authenticate(is_staff=True)

        response = update_product()

        assert response.status_code == status.HTTP_200_OK
        assert response.data["unit_price"] == 2


@pytest.mark.django_db
class TestDeleteProduct:
    def test_if_user_is_anonymus_returns_401(self, delete_product):
        respone = delete_product()

        assert respone.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, delete_product):
        authenticate()

        response = delete_product()

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_204(self, authenticate, delete_product):
        authenticate(is_staff=True)

        response = delete_product()

        assert response.status_code == status.HTTP_204_NO_CONTENT
