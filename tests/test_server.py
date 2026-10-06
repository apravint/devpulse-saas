import unittest
from server import app, perform_ai_audit

class TestDevPulseSaaS(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_health_check(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "UP")

    def test_perform_ai_audit_clean(self):
        code = "def add(a, b):\n    return a + b"
        result = perform_ai_audit(code)
        self.assertEqual(result["health_score"], 9.5)
        self.assertEqual(result["total_issues"], 0)

    def test_perform_ai_audit_vulnerability(self):
        code = 'import os\napi_key = "sk_live_12345"\neval("print(1)")'
        result = perform_ai_audit(code)
        self.assertLess(result["health_score"], 8.0)
        self.assertGreater(result["total_issues"], 0)

    def test_api_repos(self):
        response = self.client.get("/api/repos")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("repositories", data)

if __name__ == "__main__":
    unittest.main()
