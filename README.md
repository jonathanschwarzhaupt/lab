# Lab

Welcome to my **lab**, a hands-on, living repository where I thinker with and document every new technology, tool, and platform I dive into - no polished demos, just experiments and lessons learnt.

## Table of contents

1. Overview
2. Getting started
3. Directory structure
4. Current experiments

## Overview

This repo is not a tutorial, the primary goal is to track my own progress and showcase the messiness of experimentation.

So, expect rough edges, half-finished projects, and honest notes.

## Getting started

1. Clone this repository

```bash
git clone https://github.com/jonathanschwarzhaupt/lab.git
cd lab
```

2. Dive into any directory. Each one contains its own `readme.md` or instructions
3. Spin up relevant environments locally (Docker compose, K3s via Rancher Desktop, etc.)

Optional: If you use devpods and devcontainers, you can run `devpod up .` from the project root and will have tools like `kubectl` and `az-cli` available.

## Directory structure

```bash
lab/
├── docker/            # Docker Compose experiments & OSS integrations
│   ├── airflow-docker/
│   └── project-nessie/
├── kubernetes/        # Kubernetes manifests tested on local K3s (Rancher Desktop)
│   ├── 1password/     
│   ├── deployments/   
│   ├── homeassistant/
│   ├── homepage/      
│   ├── linkding/      
│   ├── mealie/         
│   └── monitoring/    
├── bicep/             # Infrastructure as code experiments using Bicep and Azure
```

## Experiments

- Docker
  - airflow-docker: Running Airflow 3.0 in docker to test out the new features like `Assets`
  - project-nessie: Run the Iceberg transactional, git-like catalogue to test out integration with pyiceberg and git-like branching
- Kubernetes
  - 1password: Bootstrap the 1password operator for seamless password integration. Potential to integrate in my homelab
  - deployments: Deployment manifests
  - homeassistant: Manifests related to [Homeassistant](https://www.home-assistant.io/)
  - linkding: Manifests related to [Linkding](https://github.com/sissbruecker/linkding). Runs in my homelab
  - mealie: Manifests related to [mealie](https://github.com/mealie-recipes/mealie). Potential to integrate in my homelab
  - Monitoring: Helm chart for the kube-prometheus-stack. Runs in my homelab
