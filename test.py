try:
    from app import app
    import unittest
except Exception as e:
    print("some modules may be missing")

class FlaskTest(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/song/1")
        statuscode = response.status_code
        self.assertEqual(statuscode,200)

    def test_audio_content(self):
        tester = app.test_client(self)
        response = tester.get("/song/1")
        statuscode = response.status_code
        self.assertEqual(response.content_type, "application/json")


    def test_audio_body(self):
        tester = app.test_client(self)
        id = 3
        response = tester.get(f"/song/{id}")
        self.assertTrue(b'3' in response.data)

if __name__ == "__main__":
    unittest.main()
