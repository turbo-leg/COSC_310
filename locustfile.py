from locust import HttpUser, task, between

class FastAPITestUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def test_search_food(self):
        self.client.get("/restaurant/search?query=pizza")

    @task(2)
    def test_get_restaurants(self):
        self.client.get("/restaurants")

    @task(1)
    def test_search_restaurant_by_name(self):
        self.client.get("/restaurants?query=burger")

    @task(1)
    def test_get_menu(self):
        self.client.get("/restaurant/100/menu")