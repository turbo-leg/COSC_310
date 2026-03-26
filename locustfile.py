"""
This module connects Locust to the backend for load testing APIs.
"""
from locust import HttpUser, task, between

class FastAPITestUser(HttpUser):
    """
    Locust Test User mimicking frontend browser behaviors for stress testing.
    """
    wait_time = between(1, 3)

    @task(3)
    def test_search_food(self):
        """ Tests requesting the search food endpoint. """
        self.client.get("/restaurant/search?query=pizza")

    @task(2)
    def test_get_restaurants(self):
        """ Tests getting list of all restaurants. """
        self.client.get("/restaurants")

    @task(1)
    def test_search_restaurant_by_name(self):
        """ Tests looking up specifically for 'burger' places. """
        self.client.get("/restaurants?query=burger")

    @task(1)
    def test_get_menu(self):
        """ Tests fetching a known restaurant parameter '100'. """
        self.client.get("/restaurant/100/menu")
