# 🎓 Le Chapeau 🎓
### An A/B Testing Platform for Socratic AI in Education

**Can we adjust the way we interact with LLMs to help students learn better?**

**Le Chapeau** is a turnkey experimental platform designed for educational and behavioral researchers. It lets teachers and researchers deploy a controlled web chat application where participants are assigned to different AI interaction paradigms (e.g. standard direct assistant vs. Socratic questioning tutor), while automatically logging interactions with **real-time disk persistence** and **salted deterministic anonymization**.

---

## 🔬 Experimental Conditions

Participants are assigned to one of three groups:

* **Group A (Control)**: Interacts with the baseline LLM without additional pedagogical scaffolding.
* **Group B (Assist)**: Interacts with a helpful, direct instructional assistant.
* **Group C (Mentor / Socratic)**: Interacts with a **Socratic agent** that refuses to simply hand over answers, instead using guided questions, step-by-step scaffolding, and reflective prompts to foster deep learning.

---

## 🚀 Quick Start for Researchers

### 1. Requirements
* macOS or Linux
* An OpenAI API Key

### 2. Configure API Key
Create a `.streamlit/secrets.toml` file or set the environment variable:

```bash
mkdir -p .streamlit
echo 'OPENAI_API_KEY = "sk-..."' > .streamlit/secrets.toml
```

*(Alternatively: `export OPENAI_API_KEY="sk-..."`)*

---

### Option A: Interactive Assistant (Recommended)

Run the guided setup script:

```bash
./deploy.sh
```

This will automatically configure limits, verify dependencies, and print the local access link to share with students (e.g., `http://192.168.1.50:8501`).

---

### Option B: Docker Compose

If you or your university sysadmin prefer running via Docker:

```bash
# Start container in the background
docker compose up -d --build

# View logs
docker compose logs -f

# Stop container
docker compose down
```

> **Data Safety Guarantee**: All study data (`data/`), configurations (`config/`), and secrets (`.streamlit/`) are mounted directly from your host machine. Containers can be rebuilt or stopped at any time without losing student rosters or conversation logs.

---

### Option C: Direct Python Execution with `uv`

Install [uv](https://docs.astral.sh/uv/) if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Sync environment and launch:
```bash
uv sync
uv run chapeau
```

Or run Streamlit directly:
```bash
uv run streamlit run src/chapeau/app.py
```

---

## 👥 Participant Management & Roster

The participant list is managed in `data/users.txt`:

```text
# Format: email_or_identifier,group
alice.dupont@etu.u-bordeaux.fr,a
bob.martin@etu.u-bordeaux.fr,b
claire.bernard@etu.u-bordeaux.fr,c
```

### Auto-Enrollment (Optional)
If you want students not on the roster to be automatically admitted during an open lecture, set the environment variable:

```bash
export CHAPEAU_AUTO_ENROLL=true
```

When enabled, any unknown student logging in will be assigned to the least-populated group to maintain balanced sample cohorts, and their assignment will be automatically recorded in `data/users.txt`.

---

## 📊 Data Persistence & Anonymized CSV Export

### Zero Data Loss
Every chat interaction is written **in real time** to `data/logs/chat_logs.jsonl`. Even if a student abruptly closes their browser or the server restarts, all interactions are safely saved to disk.

### Exporting to CSV with Salted Anonymization
To generate a research-ready CSV for your statistical analysis (R, Python, Stata, Excel):

```bash
uv run chapeau export
```

This exports to `data/exports/chapeau_interactions.csv`.

#### Consistent Cross-Study Anonymization
To comply with IRB/GDPR standards without breaking longitudinal research:
- Personal student emails are converted into a **salted deterministic UUIDv5**.
- If a student participates in multiple experiments using the same study salt (`config/salt.txt`), they will have the **exact same UUID across all studies**, allowing researchers to track student progress over time without revealing personal identifying details.
- To export un-anonymized data (e.g. for grading purposes):
  ```bash
  uv run chapeau export --no-anonymize
  ```

---

## 🏫 High-Concurrency Classroom Deployment

When hosting 100+ concurrent students simultaneously during a lecture, use the multi-worker cluster with Nginx:

1. **Start 4 background worker instances:**
   ```bash
   ./scripts/start_workers.sh
   ```
2. **Apply the provided Nginx configuration:**
   Copy [config/nginx.conf](config/nginx.conf) to your Nginx directory (e.g., `/etc/nginx/nginx.conf` or `/opt/homebrew/etc/nginx/nginx.conf`), and reload Nginx:
   ```bash
   sudo systemctl reload nginx
   ```
3. **Stop workers after the session:**
   ```bash
   ./scripts/stop_workers.sh
   ```

---

## 📦 Python Package Usage

You can also use `chapeau` directly as a Python library:

```python
import chapeau
from chapeau.prompts import assist, mentor, get_prompt_for_group
from chapeau.export import export_logs_to_dataframe, anonymize_user_id
from chapeau.auth import StudyAuth

# Authenticate a student
auth = StudyAuth()
is_valid, group = auth.authenticate("student@etu.u-bordeaux.fr")

# Load and anonymize study logs into a pandas DataFrame
df = export_logs_to_dataframe(anonymize=True)
print(df.head())
```

---

## 📚 Citation

If you use **Le Chapeau** in your academic research or teaching experiments, please cite it using the metadata from `CITATION.cff`:

```bibtex
@software{temporao2026chapeau,
  author       = {Mickael Tempor{\~a}o},
  title        = {Le Chapeau: An A/B Testing Platform for Socratic AI in Education},
  year         = {2026},
  version      = {0.1.0},
  url          = {https://github.com/mickaeltemporao/paper-socrates}
}
```

---

## 📄 License

This project is licensed under the GNU General Public License v3 ([LICENSE](LICENSE)).
