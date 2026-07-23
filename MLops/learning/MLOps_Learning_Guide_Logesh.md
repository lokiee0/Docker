# MLOps Learning Guide

**Beginner-to-job-ready roadmap for a DevOps learner**  
**Format:** Concepts + commands + hands-on project + weekly plan  
**Recommended environment:** Windows 11 with WSL Ubuntu, Git, Python and Docker Desktop

---

## 1. Purpose of this guide

This guide teaches you how to move a machine learning model from a developer's laptop into a reliable production workflow.

By completing it, you will learn how to:

- organize an ML project using a maintainable folder structure;
- version source code, datasets and model artifacts;
- train and evaluate a model reproducibly;
- track experiments with MLflow;
- expose a model through a FastAPI REST API;
- package the application with Docker;
- test the project automatically using GitHub Actions;
- deploy the container locally and optionally to AWS ECS;
- detect data drift and model-quality problems;
- understand when Kubernetes, Airflow, Kubeflow and feature stores are useful.

> **Important:** MLOps is not a single tool. It is the engineering process used to build, test, release, observe, govern and improve machine learning systems.

---

## 2. What is MLOps?

MLOps means **Machine Learning Operations**. It combines:

- machine learning development;
- data engineering;
- software engineering;
- DevOps and platform engineering;
- monitoring and governance.

A normal software application mainly changes when developers update its code. An ML application can change because of:

1. source-code changes;
2. training-data changes;
3. feature-engineering changes;
4. model-parameter changes;
5. dependency changes;
6. production-data drift;
7. real-world behavior changing over time.

Because of this, an ML system must track more than code.

### 2.1 DevOps and MLOps comparison

| Area | DevOps | MLOps |
|---|---|---|
| Primary artifact | Application package/container | Code, data, features, model and container |
| Version control | Git | Git + data/model versioning |
| Testing | Unit, integration, security | Software tests + data validation + model validation |
| Release trigger | Code change | Code, data, configuration or approved model change |
| Monitoring | CPU, memory, logs, latency, errors | Infrastructure metrics + drift + prediction quality |
| Rollback | Previous application image | Previous application image and previous model version |
| Main goal | Reliable software delivery | Reliable and reproducible ML delivery |

Your DevOps knowledge is directly useful in MLOps. You mainly need to add ML lifecycle, data management, experiment tracking and model monitoring.

---

## 3. Complete MLOps lifecycle

A practical MLOps lifecycle looks like this:

```text
Business problem
      ↓
Data collection and validation
      ↓
Feature engineering
      ↓
Model training and evaluation
      ↓
Experiment tracking
      ↓
Model registration and approval
      ↓
API/container build
      ↓
Automated testing and security checks
      ↓
Deployment
      ↓
Infrastructure and model monitoring
      ↓
Alert, rollback or retrain
```

### 3.1 Artifacts that should be traceable

For every production model, you should be able to answer:

- Which Git commit produced it?
- Which dataset version was used?
- Which parameters were used?
- Which Python and package versions were used?
- What evaluation metrics did it achieve?
- Who approved it?
- Which container image contains it?
- Where is it deployed?
- How is it performing now?

This is called **lineage** or **traceability**.

---

## 4. Prerequisites

You do not need to become a data scientist before learning MLOps. You need enough ML knowledge to understand what is being deployed and monitored.

### 4.1 Required knowledge

Learn these basics first:

- Python functions, classes, exceptions and virtual environments;
- NumPy and pandas basics;
- supervised learning concepts;
- classification versus regression;
- train, validation and test datasets;
- overfitting and underfitting;
- accuracy, precision, recall, F1 and ROC AUC;
- Git branches, commits and pull requests;
- Linux commands and file permissions;
- Docker images, containers, ports, volumes and networks;
- YAML;
- REST APIs and JSON;
- basic CI/CD.

### 4.2 Tools used in this guide

| Purpose | Beginner tool |
|---|---|
| Source control | Git and GitHub |
| Python environment | `venv` and `pip` |
| Data/pipeline versioning | DVC |
| Experiment tracking | MLflow |
| Model serving | FastAPI |
| Packaging | Docker |
| Testing | pytest |
| CI | GitHub Actions |
| Model/data monitoring | Evidently |
| System metrics | Prometheus and Grafana |
| Optional cloud deployment | AWS ECS/Fargate |
| Optional orchestration | Kubernetes, Airflow or Kubeflow |

---

## 5. Free-first learning environment

You can learn the complete foundation without purchasing a cloud server or adding a bank card.

Use:

- WSL Ubuntu on Windows 11;
- Python virtual environments;
- a local DVC remote directory;
- local SQLite for MLflow;
- Docker Desktop with WSL integration;
- GitHub Actions for CI;
- local containers;
- Minikube, kind or k3d later for local Kubernetes.

AWS is an optional final deployment exercise. Always delete cloud resources after practice to avoid charges.

---

## 6. Initial workstation setup

### 6.1 Install basic Linux packages in WSL

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git make curl
```

Check the installation:

```bash
python3 --version
pip3 --version
git --version
make --version
docker --version
```

For Docker on Windows, install Docker Desktop and enable WSL integration for your Ubuntu distribution.

### 6.2 Configure Git

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

### 6.3 Create a working directory

```bash
mkdir -p ~/workspace
cd ~/workspace
mkdir mlops-iris-project
cd mlops-iris-project
```

### 6.4 Create and activate a Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Windows PowerShell without WSL:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

---

## 7. Recommended project structure

```text
mlops-iris-project/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   └── iris.csv
├── models/
│   └── model.joblib
├── reports/
│   └── data_drift.html
├── scripts/
│   └── prepare_data.py
├── src/
│   ├── __init__.py
│   ├── api.py
│   ├── monitor.py
│   └── train.py
├── tests/
│   └── test_api.py
├── .dockerignore
├── .gitignore
├── dvc.yaml
├── Dockerfile
├── Makefile
├── metrics.json
├── params.yaml
├── README.md
└── requirements.txt
```

### Why this structure is useful

- `data/` stores datasets used by the pipeline.
- `models/` stores exported model artifacts.
- `scripts/` contains data-preparation jobs.
- `src/` contains reusable application code.
- `tests/` verifies expected behavior.
- `reports/` stores monitoring and evaluation reports.
- `.github/workflows/` stores CI/CD workflows.
- `params.yaml` separates parameters from source code.
- `dvc.yaml` describes the reproducible ML pipeline.

---

## 8. Build the beginner end-to-end project

The project will train an Iris flower classifier, track the experiment, expose predictions through an API, package it as a container and generate a drift report.

### 8.1 Create `requirements.txt`

```text
pandas
scikit-learn
joblib
pyyaml
mlflow
fastapi
uvicorn[standard]
pydantic
pytest
httpx
dvc
evidently
ruff
```

Install dependencies:

```bash
pip install -r requirements.txt
```

After the project works, create a reproducible lock-style snapshot:

```bash
pip freeze > requirements-lock.txt
```

Do not blindly use a very old lock file forever. Review and test dependency upgrades.

### 8.2 Create `.gitignore`

```gitignore
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
mlflow.db
mlruns/
.DS_Store
.env
reports/*.html
```

Do not commit secrets, `.env` files, cloud keys or access tokens.

### 8.3 Create `params.yaml`

```yaml
train:
  test_size: 0.20
  random_state: 42

model:
  max_iter: 300
```

### 8.4 Create `scripts/prepare_data.py`

```python
from pathlib import Path

from sklearn.datasets import load_iris


def main() -> None:
    output_path = Path("data/iris.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    dataset = load_iris(as_frame=True)
    dataframe = dataset.frame.rename(columns={"target": "label"})
    dataframe.to_csv(output_path, index=False)

    print(f"Saved {len(dataframe)} rows to {output_path}")


if __name__ == "__main__":
    main()
```

Run it:

```bash
python scripts/prepare_data.py
```

### 8.5 Create `src/train.py`

```python
import json
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
from mlflow.models import infer_signature
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

DATA_PATH = Path("data/iris.csv")
MODEL_PATH = Path("models/model.joblib")
METRICS_PATH = Path("metrics.json")
PARAMS_PATH = Path("params.yaml")


def load_params() -> dict:
    with PARAMS_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def main() -> None:
    params = load_params()
    dataframe = pd.read_csv(DATA_PATH)

    features = dataframe.drop(columns=["label"])
    target = dataframe["label"]

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=params["train"]["test_size"],
        random_state=params["train"]["random_state"],
        stratify=target,
    )

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(max_iter=params["model"]["max_iter"]),
            ),
        ]
    )

    # SQLite gives a simple local database-backed MLflow store.
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("iris-classification")

    with mlflow.start_run():
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)

        accuracy = accuracy_score(y_test, predictions)
        weighted_f1 = f1_score(y_test, predictions, average="weighted")

        mlflow.log_params(
            {
                "test_size": params["train"]["test_size"],
                "random_state": params["train"]["random_state"],
                "max_iter": params["model"]["max_iter"],
            }
        )
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("weighted_f1", weighted_f1)

        signature = infer_signature(x_train, model.predict(x_train))
        mlflow.sklearn.log_model(
            sk_model=model,
            name="model",
            registered_model_name="iris-classifier",
            signature=signature,
            input_example=x_train.head(3),
        )

        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, MODEL_PATH)

        metrics = {
            "accuracy": round(float(accuracy), 6),
            "weighted_f1": round(float(weighted_f1), 6),
        }
        METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

        print(f"Model saved to {MODEL_PATH}")
        print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
```

Run the training job:

```bash
python -m src.train
```

Expected outputs:

- `models/model.joblib`;
- `metrics.json`;
- `mlflow.db`;
- a new MLflow experiment run and registered-model version.

### 8.6 Start the MLflow UI

```bash
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --host 127.0.0.1 \
  --port 5000
```

Open:

```text
http://127.0.0.1:5000
```

Check:

- run parameters;
- accuracy and F1 metrics;
- model artifact;
- model signature;
- registered-model version;
- relationship between run and model.

For team use, deploy a central MLflow server with PostgreSQL, remote artifact storage, authentication, HTTPS and backups. Do not expose an unsecured local MLflow server to the public internet.

---

## 9. Data and pipeline versioning with DVC

Git is ideal for source code, but large or frequently changing datasets should not be stored directly in normal Git history.

DVC stores small metadata files in Git while the actual data can live in:

- a local directory;
- an SSH server;
- Amazon S3;
- Google Cloud Storage;
- Azure Blob Storage;
- another supported remote.

### 9.1 Initialize DVC

```bash
dvc init
git add .dvc .dvcignore
git commit -m "Initialize DVC"
```

### 9.2 Free local DVC remote

Create storage outside the Git repository:

```bash
mkdir -p ../mlops-dvc-storage
dvc remote add -d local-storage ../mlops-dvc-storage
git add .dvc/config
git commit -m "Configure local DVC remote"
```

This is enough for learning. Cloud storage is not required.

### 9.3 Track an existing dataset directly

For a dataset that already exists:

```bash
dvc add data/iris.csv
git add data/iris.csv.dvc data/.gitignore
git commit -m "Track Iris dataset with DVC"
dvc push
```

Restore it later:

```bash
dvc pull
```

### 9.4 Use a DVC pipeline

Create `dvc.yaml`:

```yaml
stages:
  prepare:
    cmd: python scripts/prepare_data.py
    deps:
      - scripts/prepare_data.py
    outs:
      - data/iris.csv

  train:
    cmd: python -m src.train
    deps:
      - data/iris.csv
      - src/train.py
      - params.yaml
    params:
      - train.test_size
      - train.random_state
      - model.max_iter
    outs:
      - models/model.joblib
    metrics:
      - metrics.json
```

If you previously used `dvc add data/iris.csv`, remove that direct tracking before making the same file a pipeline output. A file should not be owned by two DVC definitions.

Run the pipeline:

```bash
dvc repro
```

View the pipeline:

```bash
dvc dag
```

Compare metrics:

```bash
dvc metrics show
dvc metrics diff
```

Push tracked artifacts:

```bash
dvc push
git add dvc.yaml dvc.lock params.yaml metrics.json .gitignore
git commit -m "Create reproducible training pipeline"
git push
```

### 9.5 DVC learning exercise

1. Run the pipeline with `max_iter: 300`.
2. Commit the result.
3. Change `max_iter` to `500`.
4. Run `dvc repro`.
5. Compare metrics using `dvc metrics diff`.
6. Checkout the earlier Git commit.
7. Run `dvc pull` to restore the matching data/model artifacts.

This demonstrates reproducibility across code, parameters and artifacts.

---

## 10. Serve the model with FastAPI

Create `src/api.py`:

```python
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

MODEL_PATH = Path("models/model.joblib")
model = None


class PredictionRequest(BaseModel):
    sepal_length: float = Field(gt=0)
    sepal_width: float = Field(gt=0)
    petal_length: float = Field(gt=0)
    petal_width: float = Field(gt=0)


@asynccontextmanager
async def lifespan(_: FastAPI):
    global model
    if not MODEL_PATH.exists():
        raise RuntimeError("Model file is missing. Run the training pipeline first.")
    model = joblib.load(MODEL_PATH)
    yield
    model = None


app = FastAPI(
    title="Iris MLOps API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict:
    return {"status": "healthy", "model_loaded": model is not None}


@app.post("/predict")
def predict(payload: PredictionRequest) -> dict:
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")

    row = pd.DataFrame(
        [
            {
                "sepal length (cm)": payload.sepal_length,
                "sepal width (cm)": payload.sepal_width,
                "petal length (cm)": payload.petal_length,
                "petal width (cm)": payload.petal_width,
            }
        ]
    )

    prediction = int(model.predict(row)[0])
    probabilities = model.predict_proba(row)[0].tolist()

    return {
        "predicted_class": prediction,
        "class_probabilities": probabilities,
        "model_version": "1.0.0",
    }
```

Run the API:

```bash
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

Open API documentation:

```text
http://127.0.0.1:8000/docs
```

Test with curl:

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

### Production API requirements

A production inference service should normally include:

- health and readiness endpoints;
- structured logs;
- request validation;
- authentication and authorization when needed;
- rate limiting;
- request IDs for traceability;
- timeouts;
- model version in responses or logs;
- latency and error metrics;
- safe handling of personal or sensitive information;
- canary, shadow or blue/green deployment support.

---

## 11. Test the API

Create `tests/test_api.py`:

```python
from fastapi.testclient import TestClient

from src.api import app


def test_health_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["model_loaded"] is True


def test_prediction_endpoint() -> None:
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }

    with TestClient(app) as client:
        response = client.post("/predict", json=payload)

    assert response.status_code == 200
    result = response.json()
    assert result["predicted_class"] in [0, 1, 2]
    assert len(result["class_probabilities"]) == 3


def test_invalid_input_is_rejected() -> None:
    payload = {
        "sepal_length": -1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }

    with TestClient(app) as client:
        response = client.post("/predict", json=payload)

    assert response.status_code == 422
```

Run:

```bash
pytest -v
```

### Types of tests used in MLOps

| Test type | Example |
|---|---|
| Unit test | Data-cleaning function removes invalid values |
| Data test | Required columns exist and null rate is acceptable |
| Model test | Accuracy is above an agreed threshold |
| API test | `/predict` rejects invalid JSON |
| Integration test | API loads the approved model artifact |
| Container test | Container starts and health endpoint responds |
| Security test | Image and dependencies are scanned |
| Performance test | P95 inference latency stays below target |
| Drift test | Production feature distribution remains acceptable |

Do not promote a model only because its Python script completed successfully.

---

## 12. Containerize the inference API

Create `.dockerignore`:

```dockerignore
.git
.github
.venv
__pycache__
.pytest_cache
.ruff_cache
mlflow.db
mlruns
reports
*.pyc
```

Create `Dockerfile`:

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY models ./models

USER appuser

EXPOSE 8000

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build the image:

```bash
docker build -t iris-mlops-api:1.0.0 .
```

Run it:

```bash
docker run --rm -p 8000:8000 --name iris-api iris-mlops-api:1.0.0
```

Check health:

```bash
curl http://127.0.0.1:8000/health
```

Inspect:

```bash
docker ps
docker logs iris-api
docker inspect iris-api
```

### Container best practices

- use a small, trusted base image;
- pin and regularly update dependencies;
- run as a non-root user;
- never bake secrets into the image;
- use immutable version tags such as Git SHA or release version;
- scan the image for vulnerabilities;
- add health checks at the platform level;
- keep training and inference images separate when their dependencies differ.

---

## 13. Automate common commands with Make

Create `Makefile`:

```makefile
PYTHON := .venv/bin/python
PIP := .venv/bin/pip

.PHONY: setup prepare train test lint api mlflow docker-build docker-run clean

setup:
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

prepare:
	$(PYTHON) scripts/prepare_data.py

train:
	$(PYTHON) -m src.train

test:
	$(PYTHON) -m pytest -v

lint:
	$(PYTHON) -m ruff check .

api:
	$(PYTHON) -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000

mlflow:
	.venv/bin/mlflow server --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000

docker-build:
	docker build -t iris-mlops-api:1.0.0 .

docker-run:
	docker run --rm -p 8000:8000 iris-mlops-api:1.0.0

clean:
	rm -rf .pytest_cache .ruff_cache __pycache__ src/__pycache__ tests/__pycache__
```

Typical workflow:

```bash
make setup
make prepare
make train
make test
make docker-build
make docker-run
```

---

## 14. Continuous integration with GitHub Actions

Create `.github/workflows/ci.yml`:

```yaml
name: MLOps CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  test-and-build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v6

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Lint
        run: ruff check .

      - name: Prepare data
        run: python scripts/prepare_data.py

      - name: Train and evaluate model
        run: python -m src.train

      - name: Enforce model-quality threshold
        run: |
          python - <<'PY'
          import json
          from pathlib import Path

          metrics = json.loads(Path("metrics.json").read_text())
          minimum_accuracy = 0.90

          if metrics["accuracy"] < minimum_accuracy:
              raise SystemExit(
                  f"Accuracy {metrics['accuracy']} is below {minimum_accuracy}"
              )
          PY

      - name: Run tests
        run: pytest -v

      - name: Build container image
        run: docker build -t iris-mlops-api:${{ github.sha }} .
```

### What this pipeline guarantees

A pull request cannot be considered ready unless:

- dependencies install correctly;
- linting passes;
- data preparation runs;
- model training completes;
- model quality meets the threshold;
- API tests pass;
- the Docker image builds.

### CI versus continuous training versus CD

- **CI:** tests code, data logic, model logic and build output.
- **Continuous training:** retrains when approved new data or a schedule triggers it.
- **Continuous delivery:** prepares an approved model/container for release.
- **Continuous deployment:** automatically deploys after all controls pass.

Do not automatically retrain and deploy on every incoming data row. Retraining should be controlled and validated.

---

## 15. Model monitoring with Evidently

Application monitoring and model monitoring are different.

### 15.1 Application metrics

Monitor:

- request count;
- error rate;
- CPU and memory;
- container restarts;
- inference latency;
- queue depth;
- timeout rate.

Prometheus can collect time-series metrics, while Grafana can visualize dashboards and alerts.

### 15.2 Model and data metrics

Monitor:

- input schema violations;
- missing-value rate;
- out-of-range values;
- feature drift;
- prediction drift;
- target drift;
- accuracy, precision, recall or error after labels arrive;
- fairness or bias metrics where applicable;
- business outcome metrics.

### 15.3 Drift definitions

- **Data drift:** input feature distribution changes.
- **Prediction drift:** model output distribution changes.
- **Target drift:** target/label distribution changes.
- **Concept drift:** the relationship between inputs and correct outputs changes.

Drift is a warning signal, not automatic proof that the model is bad. Investigate business context and model performance.

### 15.4 Create `src/monitor.py`

```python
from pathlib import Path

import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset, DataSummaryPreset

REFERENCE_PATH = Path("data/iris.csv")
REPORT_PATH = Path("reports/data_drift.html")


def main() -> None:
    reference = pd.read_csv(REFERENCE_PATH).drop(columns=["label"])

    # Simulated production batch for learning.
    current = reference.sample(n=60, random_state=7).copy()
    current["sepal length (cm)"] = current["sepal length (cm)"] + 0.8

    report = Report(
        [
            DataDriftPreset(),
            DataSummaryPreset(),
        ]
    )
    snapshot = report.run(
        current_data=current,
        reference_data=reference,
    )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    snapshot.save_html(REPORT_PATH)
    print(f"Saved monitoring report to {REPORT_PATH}")


if __name__ == "__main__":
    main()
```

Run:

```bash
python -m src.monitor
```

Open:

```text
reports/data_drift.html
```

### 15.5 Production monitoring design

A production design can use this flow:

```text
Prediction API
   ├── emits application metrics → Prometheus → Grafana/Alertmanager
   ├── writes structured logs → log platform
   └── stores request features, prediction and model version
                                  ↓
                       Scheduled monitoring job
                                  ↓
                    Evidently quality/drift report
                                  ↓
                    Alert or retraining decision
```

Do not log passwords, tokens, raw personal information or sensitive features without a valid reason and proper controls.

---

## 16. Model registry and promotion workflow

A model registry should not merely store files. It should support a controlled lifecycle.

Example:

```text
Candidate model
      ↓ automated validation
Validation passed
      ↓ human/business approval when required
Champion model
      ↓ deployment
Production
      ↓ monitoring
Rollback or replacement
```

Useful model metadata:

- model name and version;
- training run ID;
- Git commit SHA;
- data version;
- metrics;
- owner;
- approval status;
- intended use;
- limitations;
- deployment environment;
- creation date;
- model signature;
- tags such as `validation=passed`.

Prefer registry aliases or tags such as `candidate` and `champion` instead of hard-coding a numeric model version throughout application code.

---

## 17. Deployment choices

### 17.1 Local Docker

Use first. It is free and teaches image construction, ports, logs and health checks.

### 17.2 Virtual machine

Good for learning basic deployment:

- provision Linux server;
- install container runtime;
- pull versioned image;
- run behind Nginx;
- configure HTTPS;
- add monitoring and backups.

### 17.3 AWS ECS with Fargate

ECS is useful when you want managed container orchestration without managing Kubernetes.

High-level steps:

1. create an ECR repository;
2. authenticate Docker to ECR;
3. tag and push the image;
4. create an ECS cluster;
5. create a task definition with CPU, memory, image and port;
6. create a Fargate service;
7. configure VPC subnets and security groups;
8. optionally add an Application Load Balancer;
9. configure CloudWatch logs;
10. deploy a new task-definition revision for each release;
11. verify health and roll back if needed;
12. delete resources after practice.

Use IAM roles instead of embedding AWS access keys inside containers.

### 17.4 Kubernetes

Learn Kubernetes after you are comfortable with Docker, APIs, CI/CD and monitoring.

For a model API, understand:

- Pod;
- Deployment;
- Service;
- ConfigMap;
- Secret;
- Ingress;
- readiness and liveness probes;
- resource requests and limits;
- horizontal pod autoscaling;
- rolling update and rollback;
- namespace and RBAC.

Kubernetes solves container orchestration. It does not automatically solve data versioning, experiment tracking, model approval or drift monitoring.

---

## 18. Advanced tools and when to learn them

Do not try to learn every MLOps product at the same time.

| Tool/category | Learn it when... |
|---|---|
| Airflow | You need scheduled workflows with dependencies and retries |
| Prefect/Dagster | You want Python-oriented workflow orchestration |
| Kubeflow Pipelines | Your organization runs ML workflows on Kubernetes |
| Argo Workflows | You need Kubernetes-native workflow execution |
| KServe | You need Kubernetes-native model serving and autoscaling |
| BentoML | You need a model-serving framework and packaging workflow |
| Feast | Online and offline features must remain consistent |
| Great Expectations | You need formal data-quality expectations and validation suites |
| LakeFS/DVC | You need reproducible dataset versions |
| MLflow | You need experiments, model lineage and registry workflows |
| Prometheus/Grafana | You need infrastructure and service observability |
| OpenTelemetry | You need standardized metrics, logs and traces |
| Terraform | You need reproducible cloud infrastructure |
| Helm | You need reusable Kubernetes application packages |
| Vault/cloud secrets manager | You need controlled secret storage and rotation |

### Suggested order

```text
Python + ML basics
        ↓
Git + testing + project structure
        ↓
DVC + MLflow
        ↓
FastAPI + Docker
        ↓
GitHub Actions
        ↓
Monitoring
        ↓
Cloud deployment
        ↓
Kubernetes + orchestration
        ↓
Feature store + advanced governance
```

---

## 19. Ten-week MLOps learning roadmap

Study for approximately 60–90 minutes on weekdays and build on weekends.

### Week 1 — Python and ML fundamentals

Learn:

- pandas DataFrames;
- data cleaning;
- train/test split;
- classification and regression;
- overfitting;
- accuracy, precision, recall, F1 and ROC AUC;
- scikit-learn pipelines.

Build:

- one notebook or Python script that trains an Iris classifier;
- save the model using `joblib`;
- write metrics to JSON.

Completion check:

- you can explain why test data must not be used for training;
- you can explain why accuracy alone can be misleading.

### Week 2 — Software engineering for ML

Learn:

- Python modules and packages;
- project structure;
- logging;
- configuration files;
- pytest;
- linting with Ruff;
- Git branching and pull requests.

Build:

- move notebook logic into `src/` modules;
- add tests;
- add `params.yaml`;
- add a Makefile.

Completion check:

- another developer can clone the repository and run it from the README.

### Week 3 — Data and pipeline versioning

Learn:

- why Git alone is not enough for datasets;
- DVC cache, metadata and remote storage;
- DVC stages, dependencies, outputs and parameters;
- `dvc repro`, `dvc push`, `dvc pull` and `dvc metrics diff`.

Build:

- track the dataset and model pipeline;
- configure a local DVC remote;
- reproduce an earlier experiment from Git and DVC.

Completion check:

- you can restore matching code, data and model artifacts from an old commit.

### Week 4 — Experiment tracking and registry

Learn:

- experiment, run, parameter, metric, artifact and model;
- model signature and input example;
- registry version, tag and alias;
- SQLite for local learning;
- PostgreSQL and object storage for team usage.

Build:

- log at least three experiments in MLflow;
- compare metrics;
- register the best model;
- mark one version as the champion using an alias or tag.

Completion check:

- you can identify the exact run that created a registered model.

### Week 5 — Model API

Learn:

- REST, JSON and HTTP status codes;
- FastAPI and Pydantic;
- model loading;
- request validation;
- health and readiness endpoints.

Build:

- `/health` and `/predict` endpoints;
- positive and negative tests;
- structured prediction response containing model version.

Completion check:

- invalid data returns a controlled client error instead of crashing the service.

### Week 6 — Docker

Learn:

- image layers;
- Dockerfile instructions;
- ports and networks;
- environment variables;
- non-root containers;
- image tags;
- registry push/pull;
- vulnerability scanning.

Build:

- inference image;
- local container deployment;
- health verification;
- versioned tag based on release or Git SHA.

Completion check:

- the API works on another machine with only Docker installed.

### Week 7 — CI/CD

Learn:

- workflow triggers;
- jobs and steps;
- secrets;
- branch protection;
- artifacts;
- build once, promote the same image;
- rollback strategy.

Build:

- GitHub Actions workflow for lint, train, validate, test and build;
- quality gate for model accuracy;
- optional image push only from protected main branch or release tag.

Completion check:

- a bad model or failing API test blocks the pipeline.

### Week 8 — Deployment

Choose one:

- local Docker Compose;
- Linux VM;
- AWS ECS/Fargate;
- local Kubernetes.

Learn:

- environment configuration;
- secrets;
- health checks;
- load balancing;
- rolling deployment;
- rollback;
- logs.

Build:

- deploy one immutable image;
- call `/predict` remotely or through the local cluster;
- deploy a second version and roll back.

Completion check:

- you can prove which image and model version are running.

### Week 9 — Monitoring

Learn:

- RED metrics: rate, errors and duration;
- resource monitoring;
- structured logging;
- data quality;
- drift;
- delayed ground truth;
- alert thresholds.

Build:

- Evidently drift report;
- service metrics dashboard;
- alert rule for API errors or latency;
- documented retraining decision process.

Completion check:

- you know whether a problem is infrastructure, API, data or model related.

### Week 10 — Portfolio and interview preparation

Improve the project:

- architecture diagram;
- screenshots of MLflow, CI and monitoring;
- threat and failure analysis;
- model card;
- rollback documentation;
- cost notes;
- README setup commands;
- short demo video.

Completion check:

- you can explain the project from commit to production prediction in five minutes.

---

## 20. Portfolio project after the Iris project

Build a more realistic **customer churn prediction platform**.

### Features to implement

- CSV or database ingestion;
- data validation;
- feature pipeline;
- two or more model experiments;
- DVC data/pipeline versions;
- MLflow tracking and registry;
- minimum metric gate;
- FastAPI prediction endpoint;
- Docker image;
- CI pipeline;
- optional ECS deployment;
- Prometheus service metrics;
- Evidently drift report;
- scheduled monitoring job;
- Slack or email alert;
- rollback to previous champion model.

### Architecture

```text
GitHub repository
      │
      ├── Git code/config
      ├── DVC metadata ───────────────┐
      │                               │
      │                         DVC artifact storage
      │
      └── GitHub Actions
              ├── lint/test
              ├── train/evaluate
              ├── quality gate
              ├── MLflow logging/registration
              ├── Docker build/scan
              └── deploy approved image
                          │
                    Prediction API
                     ├── metrics/logs
                     └── prediction records
                              │
                       monitoring pipeline
                              │
                         alert/retrain
```

---

## 21. Security checklist for MLOps

MLOps systems often contain sensitive datasets and powerful cloud credentials.

### Source and dependency security

- protect the main branch;
- require pull-request review;
- scan dependencies;
- scan container images;
- pin critical production dependencies;
- generate an SBOM when possible;
- sign release artifacts when possible.

### Secret security

- never store secrets in Git;
- use GitHub Secrets, AWS Secrets Manager, Vault or equivalent;
- prefer short-lived credentials and workload identity/OIDC;
- rotate credentials;
- apply least privilege.

### Data security

- classify data;
- encrypt data at rest and in transit;
- restrict dataset access;
- avoid logging personal data;
- define retention and deletion policies;
- record who trained and approved a model.

### API security

- use HTTPS;
- authenticate clients where needed;
- validate input;
- limit request size;
- rate limit;
- avoid detailed internal errors in public responses;
- keep dependencies updated.

### ML-specific risks

- training-data poisoning;
- model theft;
- adversarial or malformed input;
- feature leakage;
- unfair or biased outcomes;
- silent model degradation;
- deploying an unapproved model.

---

## 22. Reliability and rollback design

A production release should include:

- immutable image tag;
- model version or alias;
- configuration version;
- health checks;
- deployment record;
- rollback command or automated rollback;
- database/data compatibility check;
- monitoring during rollout.

### Rollback examples

**Application rollback:** deploy the previous container image tag.

**Model rollback:** point the deployment to the previous approved model alias/version.

**Full rollback:** restore the previous image, model and compatible feature configuration.

A model rollback can fail if the old model expects a different input schema. Version API and feature contracts carefully.

---

## 23. Common beginner mistakes

1. Starting with Kubeflow before understanding a simple Python training pipeline.
2. Calling a notebook in production without tests or packaging.
3. Storing large datasets directly in Git.
4. Tracking model accuracy but not dataset or code version.
5. Using `latest` as the only Docker image tag.
6. Deploying automatically without a quality gate.
7. Monitoring CPU but not drift or prediction quality.
8. Retraining automatically without validating new data.
9. Logging secrets or personal data.
10. Building a different image for each environment instead of promoting one tested image.
11. Having no rollback procedure.
12. Choosing tools before defining the problem and workflow.

---

## 24. Daily practice plan

### Monday — Learn

Read one concept and write five notes in your own words.

### Tuesday — Implement

Add one small feature to the project.

### Wednesday — Test

Write tests and intentionally create one failure.

### Thursday — Automate

Move a manual command into Make, DVC or CI.

### Friday — Observe

Review logs, metrics, experiments or drift reports.

### Saturday — Project

Work on the full pipeline for two or three focused hours.

### Sunday — Review

Document what worked, what failed and what you will do next.

---

## 25. MLOps interview questions

Practice answering these without reading notes:

1. What problem does MLOps solve?
2. How is MLOps different from DevOps?
3. Why is Git not enough for ML data?
4. What is the difference between an MLflow run and a registered model?
5. How do you reproduce a model trained three months ago?
6. What checks should run before model deployment?
7. What is data drift?
8. What is concept drift?
9. Does drift always mean that the model is inaccurate?
10. How would you roll back a model?
11. How do you connect a model version to a Docker image?
12. What is the difference between CI, continuous training and CD?
13. How do you protect training data and credentials?
14. What should an inference API health check verify?
15. Why should a container run as non-root?
16. When would you use Kubernetes instead of ECS?
17. How do you monitor a model when labels arrive late?
18. What is training-serving skew?
19. Why use a model signature?
20. What information belongs in a model card?

---

## 26. Definition of done for your first MLOps project

Mark each item only when it works.

### Repository

- [ ] Clear README
- [ ] Reproducible project structure
- [ ] `.gitignore` and no committed secrets
- [ ] Configuration outside source code
- [ ] Requirements file

### Data and training

- [ ] Dataset version is traceable
- [ ] Training is a repeatable command
- [ ] Parameters are recorded
- [ ] Metrics are recorded
- [ ] Model artifact is versioned

### MLflow

- [ ] Runs appear in UI
- [ ] Parameters and metrics are logged
- [ ] Model signature is logged
- [ ] Model is registered
- [ ] Candidate/champion process is documented

### Testing

- [ ] Unit tests pass
- [ ] Data checks pass
- [ ] Model quality threshold passes
- [ ] API tests pass
- [ ] Container builds successfully

### Delivery

- [ ] Versioned Docker image
- [ ] Non-root container
- [ ] CI workflow
- [ ] Deployment instructions
- [ ] Rollback instructions

### Monitoring

- [ ] Health endpoint
- [ ] Error and latency monitoring plan
- [ ] Drift report
- [ ] Model version included in logs or responses
- [ ] Alert/retraining decision documented

### Security

- [ ] No embedded secrets
- [ ] Least-privilege deployment role
- [ ] Dependency/image scanning plan
- [ ] Sensitive-data logging reviewed

---

## 27. Commands cheat sheet

### Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/prepare_data.py
python -m src.train
pytest -v
```

### DVC

```bash
dvc init
dvc remote add -d local-storage ../mlops-dvc-storage
dvc repro
dvc dag
dvc metrics show
dvc metrics diff
dvc push
dvc pull
```

### MLflow

```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
```

### FastAPI

```bash
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
docker build -t iris-mlops-api:1.0.0 .
docker run --rm -p 8000:8000 iris-mlops-api:1.0.0
docker ps
docker logs <container-name>
docker stop <container-name>
```

### Git

```bash
git status
git add .
git commit -m "Describe the change"
git push origin main
```

---

## 28. Recommended official learning references

Use official documentation as the main source because commands and APIs change over time.

- DVC documentation: <https://dvc.org/doc>
- MLflow documentation: <https://mlflow.org/docs/latest/>
- MLflow tracking server: <https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/>
- FastAPI tutorial: <https://fastapi.tiangolo.com/tutorial/>
- FastAPI with Docker: <https://fastapi.tiangolo.com/deployment/docker/>
- Docker documentation: <https://docs.docker.com/>
- GitHub Actions documentation: <https://docs.github.com/actions>
- Evidently documentation: <https://docs.evidentlyai.com/>
- Prometheus overview: <https://prometheus.io/docs/introduction/overview/>
- Kubernetes concepts: <https://kubernetes.io/docs/concepts/>
- AWS ECS getting started: <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/getting-started.html>

---

## 29. Your immediate next steps

Complete these in order:

1. Create the project folder and virtual environment.
2. Add the files from Sections 8–13.
3. Run data preparation and model training.
4. Open MLflow and inspect the run.
5. run the API locally and test `/predict`.
6. run pytest.
7. build and run the Docker image.
8. initialize DVC with a local remote.
9. add the GitHub Actions workflow.
10. generate the Evidently drift report.
11. push the completed project to GitHub.
12. write a README containing architecture, setup, screenshots and rollback steps.

Do not move to Kubernetes until this complete pipeline works and you can explain every component.

---

## 30. Final learning principle

The best way to learn MLOps is to repeat this cycle:

```text
Build manually
      ↓
Make it reproducible
      ↓
Test it
      ↓
Automate it
      ↓
Deploy it
      ↓
Monitor it
      ↓
Improve it
```

A strong MLOps engineer understands both the ML artifact and the production system around it.
