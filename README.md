# JobPortal

A job listing platform built as a hands-on DevOps learning project.
Each week adds a new tool to the stack — from Git to Kubernetes.

![Week](https://img.shields.io/badge/Week-3%20of%2030-blue)
![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20Java%20%7C%20Maven%20%7C%20Nexus%20%7C%20SonarQube-green)
![CI](https://img.shields.io/badge/CI-Jenkins-orange)

## About

JobPortal is a Python-based web application that continues to evolve with each DevOps milestone.
This repository documents the infrastructure and automation journey used to build, test, secure, and deploy the project.

## Week 3 tools

| Tool        | Purpose                              | Status |
|-------------|--------------------------------------|--------|
| Python 3    | Application language                 | Active |
| Git         | Version control                      | Active |
| GitHub      | Remote repo + PR workflow            | Active |
| Jenkins     | CI — auto pipeline on every push     | Active |
| Maven       | Java build tool + dependency mgmt    | Active |
| Nexus       | Artifact repository (JARs)           | Active |
| SonarQube   | Code quality + security analysis     | Active |
| EC2 Ubuntu  | Hosts all services                   | Active |

### Interactive checklist

- [x] Python 3
- [x] Git
- [x] GitHub
- [x] Jenkins
- [x] Maven
- [x] Nexus
- [x] SonarQube
- [x] EC2 Ubuntu

## Week 3 — Maven + Nexus + SonarQube

### What was built
- Maven build tool integrated for Java application (hello-java/)
- Nexus Repository Manager on EC2:8081 — stores versioned .jar artifacts
- SonarQube code quality analysis on EC2:9000 — Python + Java
- Quality Gate blocks deployment on coverage < 80% or new vulnerabilities
- JUnit test results published in Jenkins UI for both Python and Java
- SKIP_SONAR emergency parameter for incident response

### Updated pipeline flow (9 stages)

```text
git push → webhook → Jenkins
  ├── Checkout         (verify tools: Python, Maven, sonar-scanner)
  ├── Python: Install  (pip install -r requirements.txt)
  ├── Python: Test     (pytest + junit-report.xml + coverage.xml)
  ├── SonarQube: Python (sonar-scanner → SonarQube:9000)
  ├── Quality Gate     (waitForQualityGate — blocks if FAILED)
  ├── Maven: Build     (mvn clean package → target/*.jar)
  ├── Maven: SonarQube (mvn sonar:sonar → hello-java project)
  ├── Maven: Deploy    (mvn deploy → Nexus:8081/maven-snapshots/)
  └── Summary          (print build metadata)
```

### Services running on EC2

| Service    | Port | Purpose                    |
|------------|------|----------------------------|
| Jenkins    | 8080 | CI orchestration           |
| Nexus      | 8081 | Artifact repository        |
| SonarQube  | 9000 | Code quality analysis      |

### Artifact versioning
- hello-java snapshots: Nexus → maven-snapshots → com/jobportal/hello-java/
- Every Jenkins build creates a timestamped snapshot version
- Rolling back: pull older .jar from Nexus by timestamp

### Code quality thresholds (Quality Gate)
- Coverage on new code: >= 80%
- New vulnerabilities: 0
- New bugs: 0
- Maintainability rating: A

## Repository structure

```text
jobportal/
├── app.py               # Python app entry point
├── homepage.py          # Homepage module
├── jobs.py              # Job listing logic
├── auth.py              # Authentication logic
├── categories.py        # Categories module
├── config.py            # Configuration
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
├── test_app.py          # Python unit tests
├── Jenkinsfile          # CI/CD pipeline definition
├── pom.xml              # Root Maven config
├── hello-java/         # Java Maven project
│   ├── pom.xml
│   └── src/
├── coverage.xml        # Coverage report
├── junit-report.xml    # JUnit XML report
├── README.md            # Project documentation
└── .gitignore           # Git ignore file
```

## Build and validation flow

```bash
git push
# Jenkins webhook triggers the pipeline
# Checkout → Python install → pytest → SonarQube → Maven build → Nexus deploy
```

## Notes

This stage marks the transition from simple CI into a more production-like DevOps workflow with automated quality checks, artifact storage, and release readiness controls.

---

## Project status

- [x] Git initialized
- [x] GitHub connected
- [x] Jenkins pipeline active
- [x] Python tests automated
- [x] Maven project built
- [x] Nexus artifact repository active
- [x] SonarQube quality gate active
- [x] EC2 services running


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
