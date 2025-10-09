# 🧠 Socratic AI Agent | Experimental Toolbox

**Can we adjust the way we interact with LLMs to help students learn better?**

This repository provides a framework to **deploy and test an experimental AI agent** designed for educational research.
Participants are automatically assigned to either a **control group** or a **test group**.

* The **control group** interacts with a standard LLM agent.
* The **test group** interacts with a **Socratic agent**, which adopts a questioning, reflective approach meant to encourage deeper thinking and active learning.

The goal of this project is to help **teachers, students, and researchers** understand how AI can support skill development and critical thinking — and to explore how **interaction design** influences learning outcomes.

---

## 🚀 Getting Started

### 0. Install the environment

This project uses [**uv**](https://docs.astral.sh/uv/) for dependency management.
If you don’t have it installed yet:

```bash
pip install uv
```

### 1. Create and activate the environment

```bash
uv venv
source .venv/bin/activate
```

### 2. Run the app

Before launching, increase the file descriptor limit (macOS/Linux):

```bash
ulimit -n 20000
```

Then start the Streamlit app:

```bash
streamlit run main.py
```

---

## ⚙️ Running with Load Balancer (optional)

You can use **nginx** for load balancing between worker instances.

1. Install and start nginx:

   ```bash
   brew install nginx
   ```
2. Move the provided config file:

   ```bash
   mv nginx.conf /opt/homebrew/etc/nginx/nginx.conf
   ```
3. Start workers and restart nginx:

   ```bash
   ./start_workers.sh
   brew services restart nginx
   ```
4. Get your local IP:

   ```bash
   ipconfig getifaddr en0
   ```

Others on your local network can then access the app via:

```
http://<your-local-ip>:8501
```

---

## 🌐 TODO

* [ ] Add instructions for deploying on a public web server (e.g. AWS, GCP, or Render)
* [ ] Automate environment setup via a script or Dockerfile

---

## 🧪 Load Testing with Locust

You can run load tests on your deployment to simulate multiple users.

Start Locust:

```bash
locust -f locustfile.py --host http://<your-server-ip>
```

Then open the Locust web UI:

```
http://localhost:8089
```

---

## 🤝 Contributing

Contributions, experiments, and feedback are welcome!
This project is experimental and open-ended — designed to grow with community input on how to best integrate **AI-assisted learning** in educational settings.

---

## 📜 License

This project is open-sourced under the [GNU GPLv3](LICENSE).
