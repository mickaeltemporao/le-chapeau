# locustfile_static.py
from locust import HttpUser, task, between

class StaticUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def load_homepage(self):
        # Simulate loading the main page
        self.client.get("/")
