from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    wait_time = between(0.7, 1.3)

    @task
    def login(self):
        self.client.post("/login")
