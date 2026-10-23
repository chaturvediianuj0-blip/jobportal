# JobPortal

> A job listing platform built as a hands-on DevOps learning project.
> Each week adds production tools to the stack — from Git to Kubernetes.

<p align="center">
  <img src="https://img.shields.io/badge/Week-5%20of%2017-blue" alt="Week 5 of 17">
  <img src="https://img.shields.io/badge/CI-Jenkins-red" alt="CI: Jenkins">
  <img src="https://img.shields.io/badge/Quality-SonarQube-orange" alt="Quality: SonarQube">
  <img src="https://img.shields.io/badge/Artifacts-Nexus-green" alt="Artifacts: Nexus">
  <img src="https://img.shields.io/badge/Container-Docker-2496ED" alt="Container: Docker">
  <img src="https://img.shields.io/badge/Registry-AWS%20ECR-FF9900" alt="Registry: AWS ECR">
  <img src="https://img.shields.io/badge/Cloud-AWS%20ap--south--1-FF9900" alt="Cloud: AWS ap-south-1">
</p>

## Explore

- [Current stack](#current-stack)
- [Architecture](#architecture)
- [Project structure](#project-structure)
- [Pipeline details](#pipeline-details)
- [Docker](#docker)
- [AWS infrastructure](#aws-infrastructure-week-5)
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
| EC2 Ubuntu | t2.large | Hosts Jenkins, Nexus, SonarQube, and Docker | — |
| AWS VPC + EC2 + EBS + AMI | — | `jobportal-vpc`, golden AMI, gp3 volumes | — |
| AWS IAM | — | `ec2-jobportal` instance profile; no access keys | — |
| AWS S3 | — | `jobportal-static` bucket for static assets and uploads | — |
| AWS CloudWatch + SNS | — | CPU alarms and email notifications | — |
| AWS Auto Scaling | — | `jobportal-asg`, 1–3 instances, CPU target tracking | — |

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

<details open>
<summary><strong>AWS infrastructure — Week 5 · ap-south-1</strong></summary>

```text
Internet -> IGW -> VPC jobportal-vpc (10.0.0.0/16)
  public  10.0.1.0/24 (rt-public: 0.0.0.0/0 -> IGW)
          NAT Gateway + EIP, bastion/web EC2, ASG jobportal-asg
          (launch template jobportal-lt -> golden AMI, IAM role, IMDSv2)
  private 10.0.2.0/24 (rt-private: 0.0.0.0/0 -> NAT)
          app EC2; RDS planned for Week 7
Regional: S3 jobportal-static (/static/* public, uploads/ private, tmp/ lifecycle)
          IAM role ec2-jobportal, CloudWatch -> SNS jobportal-alerts -> email
```

The NAT Gateway is created only when needed to manage hourly costs. The S3 bucket name
includes the AWS account identifier; public object access is limited to `static/*`.

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
├── static/                   # CSS, JS, images; served from S3 under /static/*
├── docs/incidents/           # Week 4 incident reports (root cause + fix)
├── docs/architecture/        # Week 5 AWS diagram and service overview
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

## AWS Infrastructure (Week 5)

<details>
<summary><strong>Services, configuration, and operations</strong></summary>

| Component | Configuration |
|-----------|---------------|
| VPC | `jobportal-vpc`, `10.0.0.0/16`, DNS hostnames enabled |
| Subnets | Public `10.0.1.0/24` (auto-assign public IP); private `10.0.2.0/24`; `ap-south-1a` |
| Gateways | Internet Gateway; NAT Gateway + Elastic IP (created only when needed; hourly cost applies) |
| Route tables | `rt-public`: `0.0.0.0/0` → IGW; `rt-private`: `0.0.0.0/0` → NAT; explicit associations |
| Security groups | `w5-public-sg` (SSH/HTTP from admin IP); `w5-private-sg` (SSH from `w5-public-sg`) |
| EC2 | Ubuntu 22.04, IMDSv2 required, cloud-init user data, gp3 root volume |
| EBS | 20 GB gp3 data volume, ext4, mounted by UUID in `fstab` with `nofail` |
| AMI | `jobportal-nginx-golden` (OS + Nginx; data disk kept separate) |
| IAM | `ec2-jobportal` role via instance profile (S3 access + ECR read; no instance access keys) |
| S3 | Account-specific `jobportal-static` bucket; versioning, public `GetObject` only on `static/*`, presigned URLs |
| S3 lifecycle | `tmp/` and noncurrent versions expire after 30 days; incomplete multipart uploads aborted after 7 days |
| Monitoring | CloudWatch CPU alarm (>70%, 2 × 1-minute periods) → SNS `jobportal-alerts` → email |
| Auto Scaling | Launch template `jobportal-lt`; ASG `jobportal-asg` min 1 / max 3; target tracking CPU 60% |
| Operations | Region audit and ordered teardown scripts; rebuild-from-memory practice documented in `docs/architecture/` |

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
| v1.4.0 | TBD | AWS Core — VPC, EC2/EBS/AMI, IAM role, S3, CloudWatch/SNS, Auto Scaling |

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

<details>
<summary><strong>Week 4 — Docker</strong></summary>

Flask app containerised with a multi-stage Dockerfile (non-root), Docker networking,
Compose stack with Postgres + Redis and named volumes, Docker Hub + ECR with git-SHA tags,
Jenkins Docker build + ECR push. Four failure simulations with written incident reports.

**Resume:** *Docker: multi-stage Dockerfile, Docker Compose, networking, ECR image registry.*

</details>

<details open>
<summary><strong>Week 5 — AWS Core · Current</strong></summary>

Custom VPC with public/private subnets, IGW, NAT, and route tables; EC2 with user data
and IMDSv2; EBS volumes and golden AMIs; IAM roles via instance profiles; versioned S3
with prefix-scoped public access, presigned URLs, and lifecycle rules; CloudWatch alarms
→ SNS; Auto Scaling with target tracking. Infrastructure was destroyed and rebuilt from memory.

**Resume:** *AWS: VPC, EC2, EBS, AMI, IAM roles, S3, SNS, CloudWatch, Auto Scaling.*

</details>

<details>
<summary><strong>Week 6 — ECS · Coming next</strong></summary>

Run JobPortal containers on ECS Fargate behind an Application Load Balancer, configure
service auto scaling, retrieve secrets from SSM Parameter Store, and deploy with rolling updates.

</details>

---

<p align="center">
  <em>Learning in public — one production tool at a time.</em>
</p>
