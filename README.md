# JobPortal

A job listing platform built as a learning project across a 30-week DevOps plan.
Each week adds a new tool to the stack — from Git to Kubernetes.

![Week](https://img.shields.io/badge/Week-1%20of%2030-blue)
![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20Git%20%7C%20GitHub-green)

## About

JobPortal is a Python-based web application that will grow from a simple Flask app
to a full Django application deployed on Kubernetes by Week 15.

This repository documents the entire DevOps journey:
- Week 1: Git + GitHub (version control foundation)
- Week 2: Jenkins CI (automated pipeline) — coming soon
- Week 3: Maven + SonarQube + Nexus — coming soon
- Week 4: Docker — coming soon
- ...continues through Week 15

## Current Stack — Week 1

| Tool        | Purpose                        | Status   |
|-------------|-------------------------------|----------|
| Python      | Application language           | Active   |
| Git         | Version control                | Active   |
| GitHub      | Remote repository + PR workflow| Active   |
| EC2 Ubuntu  | Development environment        | Active   |

## Project Structure

```
jobportal/
├── app.py          # Main application entry point
├── homepage.py     # Homepage module
├── jobs.py         # Job listing module
├── config.py       # Configuration
├── utils.py        # Utility functions
├── .gitignore      # Python + env ignores
└── README.md       # This file
```

## Setup

### Prerequisites
- Python 3.x
- Git
- EC2 Ubuntu instance (or any Linux machine)

### Clone and Run
```bash
git clone https://github.com/YOUR-USERNAME/jobportal.git
cd jobportal
python app.py
```

## Git Workflow

This project follows GitHub Flow:

1. Create a feature branch from main
   git checkout -b feature/your-feature

2. Make commits with Conventional Commits format
   git commit -m 'feat(jobs): add job listing endpoint'

3. Push branch and open Pull Request on GitHub
   git push origin feature/your-feature

4. PR is reviewed and merged using Squash and Merge

5. Delete the feature branch after merge

### Branch Protection
- main is protected: no direct push allowed
- All changes go through Pull Requests
- CI must pass before merge (from Week 2 onwards)

## Releases

| Version | Date       | What was added              |
|---------|------------|-----------------------------|
| v0.1.0  | 2026-05-21 | Initial JobPortal — homepage and job listing stub |

Releases are tagged using annotated Git tags:
```bash
git tag -a v0.1.0 -m 'Release description'
git push origin v0.1.0
```

## Week 1 — Git + GitHub

### What I built
- Initialized repository and connected to GitHub
- Practiced branching: feature branches, PRs, squash merge
- Resolved merge conflicts manually
- Used git stash to save work during context switches
- Set up .gitignore for Python project
- Tagged first release v0.1.0 as annotated tag
- Used git blame and git bisect for debugging practice

### Commands I can use confidently
```bash
git init, add, commit, push, pull, branch, checkout, merge, rebase,
stash, cherry-pick, log, diff, blame, bisect, tag, revert, reset
```

### What comes next — Week 2
Jenkins CI: automated pipeline that triggers on every push to GitHub.
Every commit will automatically run tests before merging.

A job listing platform built as a hands-on DevOps learning project.
Each week adds a new tool to the stack — from Git to Kubernetes.

![Week](https://img.shields.io/badge/Week-2%20of%2030-blue)
![CI](https://img.shields.io/badge/CI-Jenkins-red)
![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20Git%20%7C%20Jenkins-green)

## Current Stack

| Tool       | Purpose                          | Status |
|------------|----------------------------------|--------|
| Python 3   | Application language             | Active |
| Git        | Version control                  | Active |
| GitHub     | Remote repo + PR workflow        | Active |
| Jenkins    | CI — auto pipeline on every push | Active |
| EC2 Ubuntu | Hosts app + Jenkins server       | Active |

## Project Structure

```text
jobportal/
├── app.py          # Application entry point
├── homepage.py     # Homepage module
├── jobs.py         # Job listing and search
├── auth.py         # Authentication (placeholder)
├── categories.py   # Job categories
├── config.py       # Configuration
├── utils.py        # Utility functions
├── test_app.py     # Test suite (pytest)
├── requirements.txt# Python dependencies
├── Jenkinsfile     # CI pipeline definition
├── .gitignore      # Python + env ignores
└── README.md       # This file
```

## CI/CD Pipeline

### Architecture

```text
Developer pushes code
        │
        ▼
   GitHub repo
        │ webhook (HTTP POST on every push)
        ▼
  Jenkins on EC2:8080
        │
        ├── Stage 1: Checkout
        │     └── verify code, print build metadata
        │
        ├── Stage 2: Install
        │     └── pip install -r requirements.txt
        │
        ├── Stage 3: Quality Checks (parallel)
        │     ├── Unit Tests    → pytest -v --tb=short
        │     └── Syntax Check  → py_compile all modules
        │
        ├── Stage 4: Deploy Info (dev/staging on main only)
        │     └── when { allOf { branch main; env != prod } }
        │
        └── Stage 5: Prod Gate (prod only)
              └── approval gate placeholder
```

### Pipeline Features

- **Auto-trigger** — GitHub webhook fires on every push, zero manual steps
- **Parallel stages** — Unit Tests and Syntax Check run simultaneously
- **Parameters** — BUILD_ENV (dev/staging/prod), RUN_FULL_TESTS
- **Credentials** — GitHub PAT in Jenkins credentials store, masked in logs
- **when conditions** — deploy stages gated by branch and environment
- **Timeout** — 20-minute pipeline timeout prevents hung builds
- **Build retention** — last 10 builds kept, older auto-deleted
- **Concurrent builds** — disabled, builds run in order
- **post block** — regression/fixed notifications, workspace cleanup

### Jenkinsfile location

Pipeline definition: [Jenkinsfile](./Jenkinsfile)
Jenkins job: Pipeline from SCM — reads Jenkinsfile from this repo on every build

## Setup

### Prerequisites
- Python 3.x
- Git
- EC2 Ubuntu t2.medium (Jenkins needs 2 vCPU, 4GB RAM minimum)

### Run locally
```bash
git clone https://github.com/YOUR-USERNAME/jobportal.git
cd jobportal
pip install -r requirements.txt
python3 -m pytest -v
python3 app.py
```

### Jenkins setup
```text
Jenkins URL    : http://<EC2-PUBLIC-IP>:8080
Job name       : jobportal-pipeline
Job type       : Pipeline (from SCM)
Trigger        : GitHub webhook → GitHub hook trigger for GITScm polling
Credentials    : github-pat (secret text), github-userpass (username+password)
```

## Git Workflow

This project follows GitHub Flow:

1. Branch from main: `git checkout -b feature/your-feature`
2. Commit with Conventional Commits: `feat(jobs): add filter by salary`
3. Push and open PR: `git push origin feature/your-feature`
4. PR triggers Jenkins CI — all tests must pass
5. Squash merge to main after approval
6. Delete feature branch

Branch protection on main: no direct push, CI must pass before merge.

## Releases

| Version | Date       | What was added                                    |
|---------|------------|---------------------------------------------------|
| v0.1.0  | 2026-05-21 | Initial JobPortal — homepage and job listing      |
| v1.0.0  | 2026-05-25 | GitFlow practice — feature branches, release cycle|
| v1.1.0  | 2026-06-01 | Jenkins CI — automated pipeline on every push     |

## Week-by-Week Progress

### Week 1 — Git + GitHub
Branching strategies, PRs, conflict resolution, git bisect, tags, revert, reset.
Resume line: *Proficient in Git/GitHub — GitFlow, GitHub Flow, PR workflow, release tagging.*

### Week 2 — Jenkins CI
Declarative pipeline, GitHub webhook, parallel stages, credentials store, build parameters.
Resume line: *Built Jenkins CI pipeline from scratch — webhook trigger, parallel test stages, secrets management.*

### Week 3 — Coming next
Maven build tool, Nexus artifact repository, SonarQube code quality analysis.
