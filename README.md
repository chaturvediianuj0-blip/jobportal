# JobPortal

> A job listing platform built as a hands-on DevOps learning project.
> Each week adds production tools to the stack — from Git to Kubernetes.

<p align="center">
  <img src="https://img.shields.io/badge/Week-4%20of%2017-blue" alt="Week 4 of 17">
  <img src="https://img.shields.io/badge/CI-Jenkins-red" alt="CI: Jenkins">
  <img src="https://img.shields.io/badge/Quality-SonarQube-orange" alt="Quality: SonarQube">
  <img src="https://img.shields.io/badge/Artifacts-Nexus-green" alt="Artifacts: Nexus">
  <img src="https://img.shields.io/badge/Container-Docker-2496ED" alt="Container: Docker">
  <img src="https://img.shields.io/badge/Registry-AWS%20ECR-FF9900" alt="Registry: AWS ECR">
</p>

## Explore

- [Current stack](#current-stack)
- [Architecture](#architecture)
- [Project structure](#project-structure)
- [Pipeline details](#pipeline-details)
- [Docker](#docker)
- [Setup](#setup)
- [Releases](#releases)
- [Week-by-week progress](#week-by-week-progress)

## Current Stack

| Tool | Version | Purpose | Port |
|------|---------|---------|------|
| Python 3 / Flask | 3.11 / 3.0 | Application (REST endpoints) | 5000 |
| Git | 2.x | Version control | — |
| GitHub | — | Remote repo + PR workflow | — |
| Jenkins | 2.x | CI orchestration | 8080 |
| Maven | 3.x | Java build + dependency management | — |
| Nexus OSS | 3.x | Artifact repository | 8081 |
| SonarQube | 10.x | Code quality + security analysis | 9000 |
| Docker + Compose v2 | 24.x+ | Containers, multi-container stack | — |
| PostgreSQL | 15 | Application database (container) | 5432 (internal) |
| Redis | 7 | Cache (container) | 6379 (internal) |
| Docker Hub / AWS ECR | — | Container image registries | — |
| EC2 Ubuntu | t2.large | Hosts all services | — |

## Architecture

<details open>
<summary><strong>CI pipeline — 11 stages</strong></summary>

```text
Developer
   |  git push
   v
GitHub (jobportal repo)
   |  webhook HTTP POST
   v
Jenkins :8080
   |- Checkout            clone repo, capture git SHA
   |- Python: Install     pip install -r requirements.txt
   |- Python: Test        pytest + junit-report.xml + coverage.xml
   |- SonarQube: Python   sonar-scanner -> SonarQube :9000
   |- Quality Gate        waitForQualityGate (blocks if FAILED)
   |- Maven: Build        mvn clean package -> target/*.jar
   |- Maven: SonarQube    mvn sonar:sonar
   |- Maven: Deploy       mvn deploy -> Nexus :8081
   |- Docker: Build       multi-stage -> jobportal:<git-sha>
   |- Docker: Push ECR    -> ACCOUNT.dkr.ecr.ap-south-1.amazonaws.com/jobportal:<git-sha>
   '- Summary             print build metadata
```

</details>

<details open>
<summary><strong>Runtime — Docker Compose</strong></summary>

```text
host :5000 --> jobportal-app :5000   (Flask, non-root appuser)
                  |  DB_HOST=postgres     REDIS_HOST=redis
                  |--> postgres-db :5432 (not published) --> volume postgres-data
                  '--> redis-cache :6379 (not published) --> volume redis-data
```

All services run on the `jobportal-net` Docker network.

</details>

## Project Structure

```text
jobportal/
├── app.py                    # Flask app: /, /jobs, /jobs/search/<kw>, /health, /db-check, /cache-check
├── homepage.py               # Homepage routes and views
├── jobs.py                   # Job listing and search
├── auth.py                   # Authentication
├── categories.py             # Job categories
├── config.py                 # Application configuration
├── utils.py                  # Shared utilities
├── test_app.py               # pytest suite
├── requirements.txt          # Flask, pytest, pytest-cov, psycopg2-binary, redis
├── Dockerfile                # Multi-stage: python:3.11 builder -> python:3.11-slim runtime
├── .dockerignore
├── docker-compose.yml        # App + Postgres + Redis, named volumes, app memory limit
├── .env.example              # Copy to .env; never commit .env
├── Jenkinsfile               # 11-stage CI pipeline
├── sonar-project.properties
├── pom.xml                   # Root Maven placeholder
├── hello-java/               # Java app (Maven): pom.xml, src/main, src/test
├── docs/incidents/           # Week 4 incident reports (root cause + fix)
├── .gitignore
└── README.md
```

## Pipeline Details

### Triggers

Every push to GitHub fires a webhook to Jenkins. No manual steps.

### Parameters

| Parameter | Type | Default | Purpose |
|-----------|------|---------|---------|
| `BUILD_ENV` | choice | `dev` | `dev` / `staging` / `prod` environment |
| `SKIP_SONAR` | boolean | `false` | Emergency bypass for SonarQube |

### Quality Gate Conditions

| Condition | Threshold | Applies to |
|-----------|-----------|------------|
| Coverage | >= 80% | New code |
| New Vulnerabilities | = 0 | New code |
| New Bugs | = 0 | New code |
| Maintainability Rating | = A | New code |

<details>
<summary><strong>Jenkins credentials</strong> (stored securely; never put credentials in code)</summary>

| ID | Type | Used for |
|----|------|----------|
| `github-pat` | Secret text | GitHub API token |
| `github-userpass` | Username + password | Repository clone authentication |
| `sonar-token` | Secret text | SonarQube analysis authentication |
| `nexus-admin-password` | Secret text | Nexus deploy authentication |
| `aws-access-key-id` / `aws-secret-key` | Secret text | ECR push (planned replacement: an IAM role) |

</details>

## Docker

| Item | Value |
|------|-------|
| Base images | `python:3.11` (builder), `python:3.11-slim` (runtime) |
| User | `appuser` (non-root) |
| Image tag | Git commit SHA (immutable); never use `:latest` in production |
| ECR | `jobportal` repo, tag immutability on, scan on push, lifecycle keeps last 10 |
| Compose services | `app` (5000), `postgres` (internal), `redis` (internal) |
| Persistence | Named volumes `postgres-data`, `redis-data` |
| App memory | 256M limit, 128M reservation (measured with `docker stats`) |

<details>
<summary><strong>Failure drills</strong> — documented in <code>docs/incidents/</code></summary>

| # | Failure | Root cause |
|---|---------|------------|
| 01 | App unreachable on :5000 | Compose mapped 5000:8000, while Flask listens on 5000 |
| 02 | `/db-check`: name not known | Postgres was on a different Docker network |
| 03 | Data "gone" after deploy | Volume was mounted at the wrong path |
| 04 | Restart loop, exit 137 | 15M memory limit caused an OOM kill |

</details>

## Setup

### Prerequisites

- EC2 Ubuntu `t2.large` (8GB RAM for Jenkins + Nexus + SonarQube + Docker)
- Java 17, Python 3.11, Maven 3.x, SonarScanner CLI, Docker + Compose v2

<details open>
<summary><strong>Run the full stack</strong></summary>

```bash
git clone https://github.com/YOUR-USERNAME/jobportal.git
cd jobportal
cp .env.example .env      # Fill in real values; do not commit this file
docker compose up -d --build
curl localhost:5000/health
curl localhost:5000/db-check
curl localhost:5000/cache-check
```

</details>

<details>
<summary><strong>Run tests locally</strong></summary>

```bash
pip install -r requirements.txt
python3 -m pytest -v
```

</details>

## Releases

| Version | Date | Added |
|---------|------|-------|
| v0.1.0 | 2026-05-21 | Initial JobPortal — homepage and job listing |
| v1.0.0 | 2026-05-25 | GitFlow practice — release cycle |
| v1.1.0 | 2026-06-01 | Jenkins CI — automated pipeline on every push |
| v1.2.0 | 2026-09-14 | Maven + Nexus + SonarQube — quality-gated pipeline |
| v1.3.0 | TBD | Docker — multi-stage image, Compose stack, ECR, failure drills |

## Week-by-Week Progress

<details>
<summary><strong>Week 1 — Git + GitHub</strong></summary>

Branching strategies (GitFlow, GitHub Flow), PRs, conflict resolution, `git bisect`,
annotated tags, revert, and reset.

**Resume:** *Proficient in Git/GitHub — GitFlow, PR workflow, release tagging.*

</details>

<details>
<summary><strong>Week 2 — Jenkins CI</strong></summary>

Declarative pipeline, GitHub webhook, parallel stages, credentials store,
build parameters, `when` conditions, and `post` block patterns.

**Resume:** *Built Jenkins CI from scratch — webhook trigger, parallel stages, secrets management.*

</details>

<details>
<summary><strong>Week 3 — Maven + Nexus + SonarQube</strong></summary>

Maven build lifecycle, `pom.xml`, Nexus artifact repository (releases + snapshots),
SonarQube code quality analysis, Quality Gate enforcement, and JUnit reporting.

**Resume:** *Integrated Maven + Nexus + SonarQube into Jenkins — quality-gated pipeline, versioned artifacts.*

</details>

<details open>
<summary><strong>Week 4 — Docker · Current</strong></summary>

Flask app containerised with a multi-stage Dockerfile (non-root), Docker networking,
Compose stack with Postgres + Redis and named volumes, Docker Hub + ECR with git-SHA tags,
Jenkins Docker build + ECR push. Four failure simulations with written incident reports.

**Resume:** *Docker: multi-stage Dockerfile, Docker Compose, networking, ECR image registry.*

</details>

<details>
<summary><strong>Week 5 — AWS Core · Coming next</strong></summary>

VPC with public/private subnets, EC2 + EBS + AMI, IAM roles, S3, CloudWatch + SNS,
and Auto Scaling.

</details>

---

<p align="center">
  <em>Learning in public — one production tool at a time.</em>
</p>
