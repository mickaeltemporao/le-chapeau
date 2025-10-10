from locust import HttpUser, TaskSet, task, between
import random
import os

# Load user IDs from file at startup
USER_FILE = "users.txt"  # or users_spb.txt depending on which you use
if os.path.exists(USER_FILE):
    with open(USER_FILE, "r") as f:
        USERS = [line.strip().split(",")[0] for line in f if line.strip()]
else:
    USERS = []


class UserBehavior(TaskSet):
    def on_start(self):
        """Simulate login with a random user from the file."""
        if not USERS:
            raise RuntimeError("No users loaded from file")

        self.username = random.choice(USERS)

        # Step 1: Load login page
        self.client.get("/")

        # Step 2: Post login credentials
        self.client.post(
            "/",
            data={"Entrez votre identifiant": self.username}
        )

    @task(2)
    def chat_interaction(self):
        """Simulate sending a chat prompt."""
        prompts = [
            "Explique-moi la relativité en termes simples.",
            "Quels sont les trois lois de Newton?",
            "Peux-tu m'aider avec un problème de maths?",
            "Donne-moi un exemple de fonction en Python."
        ]
        prompt = random.choice(prompts)

        self.client.post("/", data={"Enter you request here...": prompt})

    @task(1)
    def load_home(self):
        """Occasionally reload home page."""
        self.client.get("/")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # simulate think time between requests

