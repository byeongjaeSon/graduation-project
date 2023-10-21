from locust import HttpUser, task, between, TaskSet

class UserBehavior(HttpUser):
    wait_time = between(0.7, 1.3)

    @task
    def signUp(self):
        self.client.post("/sign-up")
