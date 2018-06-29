# from models import Message, User
from app import app
import unittest


class WarblerIntegrationTestCase(unittest.TestCase):
    def test_404(self):
        """tests correct rendering of custom 404 page"""
        client = app.test_client()
        result = client.get('/letsgotoafakeroute')
        # test for 404 status code
        self.assertEqual(result.status_code, 404)
        # test for jinja template rendered
        self.assertIn(b'LOOK OUT!!!', result.data)


if __name__ == '__main__':
    unittest.main()