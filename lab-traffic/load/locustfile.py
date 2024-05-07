import time
from locust import HttpUser, task, between

class HitHomePage(HttpUser):
  wait_time = between(1, 5)
  @task
  def index(self):
    self.client.get("/")