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
git init, add, commit, push, pull, branch, checkout, merge, rebase,
stash, cherry-pick, log, diff, blame, bisect, tag, revert, reset

### What comes next — Week 2
Jenkins CI: automated pipeline that triggers on every push to GitHub.
Every commit will automatically run tests before merging.
