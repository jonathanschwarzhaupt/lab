# 🧪 Lab: Technology Learning Journey

Welcome to my **lab** - a hands-on, living repository where I explore and document every new technology, tool, and platform I dive into. This isn't a collection of polished demos, but rather an authentic showcase of learning through experimentation.

## 🎯 What This Repository Demonstrates

**Technical Versatility**: Hands-on experience with modern cloud-native and data engineering technologies:

- **Container Orchestration**: Kubernetes manifest management and Docker containerization
- **Infrastructure as Code**: Azure Bicep templates and cloud resource management  
- **Data Engineering**: Apache Airflow 3.0, Apache Iceberg, and modern orchestration tools
- **Python Development**: Modern tooling with uv, Prefect workflows, and data processing
- **Development Environments**: DevContainers, mise tool management, and reproducible setups

**Learning Philosophy**: Embracing the "learning in public" approach - documenting both successes and challenges to build genuine expertise through hands-on experimentation.

**Real-World Application**: All experiments are tested in realistic environments (local K3s clusters, Azure subscriptions, homelab deployments) rather than theoretical examples.

## Table of Contents

1. [Learning Approach](#-learning-approach)
2. [Technology Deep Dives](#-technology-deep-dives)
3. [Getting Started](#-getting-started)
4. [Directory Structure](#-directory-structure)
5. [Current Experiments](#-current-experiments)

## 🚀 Learning Approach

This repository reflects my belief that the best way to understand complex technologies is through hands-on experimentation. Each directory represents a focused learning sprint where I implement realistic scenarios, document both successes and failures, and integrate multiple technologies to understand how they work together in practice.

*Expect rough edges, half-finished projects, and honest documentation - this is learning in progress, not a portfolio of completed solutions.*

## 🔬 Technology Deep Dives

### Docker Containerization & Data Stack

**Location**: `docker/`

**Airflow 3.0 Exploration** (`airflow-docker/`)

- Experimenting with Apache Airflow 3.0's new features, particularly the Assets functionality
- Docker Compose setup for local development and testing
- Focus on understanding modern data orchestration patterns and DAG evolution

**Project Nessie & Apache Iceberg** (`project-nessie/`)

- Hands-on implementation of Apache Iceberg transactional data lake catalog
- Integration with PyIceberg for Python-based data processing
- Testing git-like branching capabilities for data versioning and experimentation
- Requirements include PyArrow, S3FS for cloud storage integration

### Kubernetes & Cloud-Native Applications

**Location**: `kubernetes/`

**Security & Secrets Management** (`1password/`)

- Implementation of 1Password Kubernetes operator for secure secret management
- Exploration of modern secrets management patterns in cloud-native environments

**Application Deployments** (`deployments/`, `homeassistant/`, `linkding/`, `mealie/`)

- Real-world Kubernetes manifest configurations for various applications
- Load balancer configurations, persistent storage management
- Homelab-ready deployments with focus on self-hosted solutions

**Monitoring & Observability** (`monitoring/`)

- Kube-prometheus-stack Helm chart implementation
- Production-ready monitoring setup for Kubernetes clusters
- Integration with homelab infrastructure

### Infrastructure as Code with Azure

**Location**: `bicep-templates/`

**Azure Bicep Learning Path**

- Following Microsoft's 3-part Bicep fundamentals training
- Storage account provisioning with Infrastructure as Code principles
- Focus on declarative infrastructure management and Azure best practices
- Includes deployment automation and resource cleanup strategies

### Python Orchestration & Modern Development

**Location**: `orchestration-prefect/`

**Prefect 3 Workflow Orchestration**

- Exploring Prefect as a modern alternative to traditional DAG-based orchestration
- Python 3.13+ with modern dependency management using `uv`
- Focus on pythonic workflow design without traditional DAG constraints
- Local development setup with both ephemeral and persistent server configurations

## 🛠️ Getting Started

### Prerequisites

- **Tool Management**: Uses `mise` for consistent Python (3.10.11) and kubectl versions
- **Container Runtime**: Docker Desktop or equivalent
- **Kubernetes**: Rancher Desktop recommended for local K3s cluster
- **Cloud Access**: Azure CLI for Bicep experiments

### Quick Start

```bash
# Clone and enter repository
git clone https://github.com/jonathanschwarzhaupt/lab.git
cd lab

# Install development tools
mise install

# Choose your experiment and follow directory-specific instructions
cd <experiment-directory>
```

**DevContainer Support**: Run `devpod up .` from project root for pre-configured environment with kubectl and python.

## 📁 Directory Structure

```bash
lab/
├── bicep-templates/           # Azure Infrastructure as Code
│   └── first-template/        # Basic storage account deployment
├── docker/                    # Container orchestration experiments
│   ├── airflow-docker/        # Apache Airflow 3.0 with Assets
│   └── project-nessie/        # Iceberg catalog with PyIceberg integration
├── kubernetes/                # K8s manifests for Rancher Desktop
│   ├── 1password/            # Secrets management operator
│   ├── deployments/          # Various deployment strategies
│   ├── homeassistant/        # Home automation platform
│   ├── homepage/             # Dashboard application
│   ├── linkding/             # Bookmark management
│   ├── mealie/               # Recipe management
│   └── monitoring/           # Prometheus stack for observability
├── orchestration-prefect/     # Modern Python workflow orchestration
└── scripts/                  # Utility scripts and automation
```

## 🎓 Learning Outcomes & Technical Skills

Through these hands-on experiments, I've developed practical experience with:

**Cloud-Native Architecture**

- Container orchestration with Kubernetes in production-like environments
- Modern secrets management and security practices
- Microservices deployment patterns and service mesh concepts
- Infrastructure monitoring and observability with Prometheus/Grafana

**Data Engineering & Orchestration**

- Modern workflow orchestration beyond traditional DAG patterns
- Data lake architecture with transactional capabilities (Iceberg)
- Version control for data with git-like branching strategies
- Integration of Python data processing tools (PyArrow, PyIceberg)

**Infrastructure as Code**

- Declarative infrastructure management with Azure Bicep
- Resource lifecycle management and cleanup automation
- Cloud resource provisioning with best practices
- DevOps integration patterns for infrastructure deployment

**Modern Development Practices**

- DevContainer and development environment standardization
- Modern Python tooling (uv, mise) for reproducible environments
- Container-first development and deployment strategies
- Documentation-driven development and learning in public

Each experiment demonstrates progression from basic concepts to more complex, integrated solutions that mirror real-world production challenges.
