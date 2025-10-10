# locustfile_ws.py
from locust import User, task, between
from websocket import create_connection
import random
import json

class StreamlitUser(User):
    wait_time = between(1, 5)

    def on_start(self):
        # Connect once when the user "arrives"
        self.ws = create_connection("ws://your-server-ip/stream")

    @task
    def send_chat_message(self):
        # Example: fake a chat input event (structure depends on Streamlit internals)
        prompt = random.choice([
            "Explique-moi la relativité en termes simples.",
            "Quels sont les trois lois de Newton?",
            "Peux-tu m'aider avec un problème de maths?",
            "Donne-moi un exemple de fonction en Python."
        ])

        # NOTE: You must adapt this payload to match Streamlit’s actual WS protocol
        msg = {
            "type": "input_widget",
            "id": "chat_input",
            "value": prompt,
        }

        # Send message
        self.ws.send(json.dumps(msg))

        # Read one response (discard or log)
        try:
            response = self.ws.recv()
            # print("Got:", response)
        except Exception as e:
            print("WS error:", e)

    def on_stop(self):
        # Close connection when the simulated user leaves
        if self.ws:
            self.ws.close()
