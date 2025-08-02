import unittest
import json
import os
from app.main import app
from app.models import init_db

class URLShortenerTestCase(unittest.TestCase):
    def setUp(self):
        # Reinitialize DB for each test
        if os.path.exists('url_shortener.db'):
            os.remove('url_shortener.db')
        init_db()
        self.client = app.test_client()

    def test_health_check(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'healthy', response.data)

    def test_shorten_url(self):
        response = self.client.post('/shorten', json={'url': 'https://example.com'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('short_code', data)
        self.assertIn('short_url', data)

    def test_redirect_and_stats(self):
        # First shorten a URL
        post_response = self.client.post('/shorten', json={'url': 'https://openai.com'})
        data = post_response.get_json()
        short_code = data['short_code']

        # Simulate redirect
        redirect_response = self.client.get(f'/{short_code}', follow_redirects=False)
        self.assertEqual(redirect_response.status_code, 302)
        self.assertIn('openai.com', redirect_response.headers['Location'])

        # Check stats
        stats_response = self.client.get(f'/stats/{short_code}')
        stats_data = stats_response.get_json()
        self.assertEqual(stats_data['visit_count'], 1)

    def test_invalid_code_redirect(self):
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Invalid short code', response.data)

if __name__ == '__main__':
    unittest.main()
