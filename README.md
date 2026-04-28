# Task API

A small FastAPI project for learning backend development, testing, Docker,
Kubernetes, and GitHub Actions.

## What This API Does

The app stores tasks in memory and exposes these endpoints:

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Check that the API is running |
| `GET` | `/tasks` | List all tasks |
| `POST` | `/tasks` | Create a task |
| `PUT` | `/tasks/{task_id}` | Replace a task |
| `DELETE` | `/tasks/{task_id}` | Delete a task |

Tasks are stored in a Python dictionary. This is simple for learning, but it
means data disappears when the app restarts. In a real production app, this
would usually be replaced by a database.

## Run Locally

Create and activate a virtual environment, then install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open the docs:

```text
http://127.0.0.1:8000/docs
```

## Run Tests

```bash
pytest
```

The tests use FastAPI `TestClient`, so they call the app directly without
starting a real web server.

## Run With Docker

Build and run the image manually:

```bash
docker build -t task-api .
docker run -p 8000:8000 task-api
```

Or use Docker Compose:

```bash
docker compose up --build
```

## Kubernetes

The Kubernetes manifests are in `k8s/`.

```bash
kubectl apply -f k8s/
```

The Service is `ClusterIP`, so it is only reachable inside the cluster by
default. For local testing, use port forwarding:

```bash
kubectl port-forward service/task-api 8000:8000
```

Note: this app uses in-memory storage. With `replicas: 2`, each pod has its own
separate task dictionary. That is useful for learning how replicas work, but a
real app should use a shared database so all replicas see the same data.

## CI

GitHub Actions runs the workflow in `.github/workflows/ci.yml` on every push
and pull request. It installs dependencies and runs `pytest` on a clean Ubuntu
runner.
