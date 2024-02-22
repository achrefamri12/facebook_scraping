# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 16:48:11 2024

@author: User
"""

import requests
import unittest

class TestScrapingEndpoint(unittest.TestCase):
    def test_scrape_page(self):
        base_url = "http://localhost:8000"
        
        page_name = "elyadata"
        
        response = requests.get(f"{base_url}/scrape/{page_name}")
        
        self.assertEqual(response.status_code, 200)
        
        response_json = response.json()
        
        self.assertIn("page_info", response_json)
        self.assertIn("posts", response_json)
        self.assertIn("photos", response_json)
        
      

if __name__ == "__main__":
    unittest.main()
