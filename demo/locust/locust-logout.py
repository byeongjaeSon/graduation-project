from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    wait_time = between(0.7, 1.3)

    @task
    def logout(self):
        self.client.post("/logout")
