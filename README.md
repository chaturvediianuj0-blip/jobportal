# JobPortal

A job listing platform built as a hands-on DevOps learning project.
Each week adds production tools to the stack — from Git to Kubernetes.

![Week](https://img.shields.io/badge/Week-3%20of%2030-blue)
![CI](https://img.shields.io/badge/CI-Jenkins-red)
![Quality](https://img.shields.io/badge/Quality-SonarQube-orange)
![Artifacts](https://img.shields.io/badge/Artifacts-Nexus-green)

> This project demonstrates a full CI/CD pipeline for a Python and Java application running on EC2, with Jenkins automation, Maven builds, Nexus artifact hosting, and SonarQube quality enforcement.

---

## Current Stack

| Tool        | Version | Purpose                          | Port |
|-------------|---------|----------------------------------|------|
| Python 3    | 3.x     | Application language             | —    |
| Git         | 2.x     | Version control                  | —    |
| GitHub      | —       | Remote repo + PR workflow        | —    |
| Jenkins     | 2.x     | CI orchestration                 | 8080 |
| Maven       | 3.x     | Java build + dependency mgmt     | —    |
| Nexus OSS   | 3.x     | Artifact repository              | 8081 |
| SonarQube   | 10.x    | Code quality + security analysis | 9000 |
| EC2 Ubuntu  | t2.large| Hosts all services               | —    |

---

## Architecture

```text
Developer
    │
    │ git push
    ▼
GitHub (jobportal repo)
    │
    │ webhook HTTP POST
    ▼
Jenkins :8080
    │
    ├─ Checkout         ── clone repo, verify tools
    ├─ Python: Install  ── pip install -r requirements.txt
    ├─ Python: Test     ── pytest + junit-report.xml + coverage.xml
    ├─ SonarQube: Py   ── sonar-scanner → SonarQube:9000
    ├─ Quality Gate    ── waitForQualityGate (blocks if FAILED)
    │       │
    │   [gate FAILED] ── pipeline stops, nothing deployed
    │       │
    │   [gate OK]
    │       │
    ├─ Maven: Build    ── mvn clean package → target/*.jar
    ├─ Maven: SonarQube── mvn sonar:sonar → SonarQube:9000
    ├─ Maven: Deploy   ── mvn deploy → Nexus:8081
    └─ Summary         ── print build metadata
             │
             ▼
    Nexus :8081
    maven-snapshots/
    com/jobportal/hello-java/1.1-SNAPSHOT/
    hello-java-1.1-SNAPSHOT-YYYYMMDD.jar
```

---

## Project Structure

```text
jobportal/
├── app.py                   # Application entry point
├── homepage.py              # Homepage module
├── jobs.py                  # Job listing and search
├── auth.py                  # Authentication (placeholder)
├── categories.py            # Job categories
├── config.py                # Configuration
├── utils.py                 # Utility functions
├── test_app.py              # Python test suite (pytest)
├── requirements.txt         # Python dependencies (incl. pytest-cov)
├── Jenkinsfile              # 9-stage CI pipeline definition
├── sonar-project.properties # SonarQube scanner configuration
├── pom.xml                  # Root Maven placeholder
├── .gitignore               # Python + coverage + Maven ignores
├── README.md                # This file
└── hello-java/              # Java application (Maven project)
    ├── pom.xml              # Maven config: build, Sonar, Nexus deploy
    └── src/
        ├── main/java/com/jobportal/App.java
        └── test/java/com/jobportal/AppTest.java
```

---

## Pipeline Details

### Triggers
Every push to GitHub fires a webhook to Jenkins. No manual steps.
Branch filter: all branches. Deploy stages gated by branch and BUILD_ENV parameter.

### Parameters

| Parameter  | Type    | Default | Purpose                          |
|------------|---------|---------|----------------------------------|
| BUILD_ENV  | choice  | dev     | dev / staging / prod environment |
| SKIP_SONAR | boolean | false   | Emergency bypass for SonarQube   |

### Quality Gate Conditions

| Condition              | Threshold | On       |
|------------------------|-----------|----------|
| Coverage               | >= 80%    | New code |
| New Vulnerabilities    | = 0       | New code |
| New Bugs               | = 0       | New code |
| Maintainability Rating | = A       | New code |

### Credentials (Jenkins credentials store — never in code)

| ID                   | Type          | Used for                    |
|----------------------|---------------|-----------------------------|
| github-pat           | Secret text   | GitHub API token            |
| github-userpass      | Username+Pass | Repo clone authentication   |
| sonar-token          | Secret text   | SonarQube analysis auth     |
| nexus-admin-password | Secret text   | Nexus deploy authentication |

---

## Setup

### Prerequisites
- EC2 Ubuntu t2.large (8GB RAM — Jenkins + Nexus + SonarQube each need RAM)
- Java 17
- Python 3.x
- Maven 3.x
- sonar-scanner CLI

### Run tests locally
```bash
git clone https://github.com/YOUR-USERNAME/jobportal.git
cd jobportal
pip install -r requirements.txt
python3 -m pytest -v
```

### Run Maven build locally
```bash
cd hello-java
mvn clean package
java -jar target/hello-java-1.1-SNAPSHOT.jar
```

---

## Releases

| Version | Date       | Added                                              |
|---------|------------|----------------------------------------------------|
| v0.1.0  | 2026-05-21 | Initial JobPortal — homepage and job listing       |
| v1.0.0  | 2026-05-25 | GitFlow practice — release cycle                   |
| v1.1.0  | 2026-06-01 | Jenkins CI — automated pipeline on every push      |
| v1.2.0  | 2026-09-14 | Maven + Nexus + SonarQube — quality-gated pipeline |

---

## Week-by-Week Progress

### Week 1 — Git + GitHub
Branching strategies (GitFlow, GitHub Flow), PRs, conflict resolution,
git bisect, annotated tags, revert, reset.
Resume: *Proficient in Git/GitHub — GitFlow, PR workflow, release tagging.*

### Week 2 — Jenkins CI
Declarative pipeline, GitHub webhook, parallel stages, credentials store,
build parameters, when conditions, post block patterns.
Resume: *Built Jenkins CI from scratch — webhook trigger, parallel stages, secrets management.*

### Week 3 — Maven + Nexus + SonarQube
Maven build lifecycle, pom.xml, Nexus artifact repository (releases + snapshots),
SonarQube code quality analysis, Quality Gate enforcement, JUnit reporting.
Resume: *Integrated Maven+Nexus+SonarQube into Jenkins — quality-gated pipeline, versioned artifacts.*

### Week 4 — Docker (coming next)
Containerise the Python and Java apps. Build Docker images in Jenkins.
Push images to ECR. Replace .jar deployment with container deployment.