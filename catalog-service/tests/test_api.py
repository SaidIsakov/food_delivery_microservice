from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_product_service


client = TestClient(app=app)


def test_get_products_success():

  class MockProductService:
    async def get_products(self):
      return [
        {
          "id": "123e4567-e89b-12d3-a456-426614174000",
           "name": "Test product",
           "category": "Test Category",
           "price": 1000.0,
           "stock": 2
        }
      ]

  app.dependency_overrides[get_product_service] = lambda: MockProductService()

  response = client.get("/products")

  assert response.status_code == 200

  data = response.json()

  assert isinstance(data, list)
  assert len(data) == 1
  assert data[0]["name"] == "Test product"

  app.dependency_overrides.clear()


def test_get_product_by_id():

  class MockProductService:
    async def get_product(self, product_id="123e4567-e89b-12d3-a456-426614174000"):
      return {
          "id": product_id,
          "name": "Test product",
          "category": "Test Category",
          "price": 500.0,
          "stock": 1
        }

  app.dependency_overrides[get_product_service] = lambda: MockProductService()

  response = client.get("/products/123e4567-e89b-12d3-a456-426614174000")

  assert response.status_code == 200
  data = response.json()

  assert data["id"] == "123e4567-e89b-12d3-a456-426614174000"
  assert data["price"] == 500.0

  app.dependency_overrides.clear()
