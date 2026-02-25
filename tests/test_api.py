import unittest
from fastapi.testclient import TestClient
from src.api.server import app

class TestApi(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_stats(self):
        response = self.client.get("/v1/stats")
        self.assertEqual(response.status_code, 200)
        self.assertIn("count", response.json())

    def test_add_and_query_memory(self):
        # Add memory
        response = self.client.post("/v1/memories", json={"content": "API Test Memory"})
        self.assertEqual(response.status_code, 200)
        memory_id = response.json().get("id")
        self.assertIsNotNone(memory_id)

        # Query memory
        response = self.client.post("/v1/query", json={"query": "API Test"})
        self.assertEqual(response.status_code, 200)
        results = response.json().get("results")
        self.assertGreater(len(results), 0)

        # Verify content
        found = any("API Test Memory" in res["content"] for res in results)
        self.assertTrue(found)

if __name__ == '__main__':
    unittest.main()
