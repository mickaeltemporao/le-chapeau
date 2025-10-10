# 🧠 Socratic AI Agent | Experimental Toolbox

**Can we adjust the way we interact with LLMs to help students learn better?**

This repository provides a framework to **deploy and test an experimental AI agent** designed for educational research.
Participants are automatically assigned to either a **control group** or a **test group**.

* The **control group** interacts with a standard LLM agent.
* The **test group** interacts with a **Socratic agent**, which adopts a questioning, reflective approach meant to encourage deeper thinking and active learning.

The goal of this project is to help **teachers, students, and researchers** understand how AI can support skill development and critical thinking — and to explore how **interaction design** influences learning outcomes.

---

## 🚀 Getting Started

### 0. Install `uv`

[`uv`](https://docs.astral.sh/uv/) is a fast Python package and environment manager.

Install via your preferred package manager:

**macOS / Linux (Homebrew):**

```bash
brew install uv
```

**Using pipx (recommended cross-platform):**

```bash
pipx install uv
```

You can verify the installation with:

```bash
uv --version
```

---

### 1. Set up the environment

Create a virtual environment (if one doesn’t exist) and install dependencies:

```bash
uv venv
uv sync
```

Then activate the environment:

```bash
source .venv/bin/activate
```

---

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
   pacman install nginx
   ```
2. Move the provided config file:

   ```bash
   sudo mv nginx.conf /opt/homebrew/etc/nginx/nginx.conf
   ```
3. Start workers and restart nginx:

   ```bash
   ./start_workers.sh
   systemctl restart nginx
   ```
Others on your local network can then access the app via:

```
http://<your-local-ip>:8501
```

---

## 🌐 TODO

* [ ] Fix paths for new folder structure
* [ ] Add deployment instructions for a public web host (AWS, GCP, Render, etc.)
* [ ] Add Dockerfile for containerized deployment
* [ ] Include auto-sync step in startup script

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
