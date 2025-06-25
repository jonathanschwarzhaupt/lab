# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal laboratory repository for experimenting with various technologies including Docker, Kubernetes, Azure Bicep, and Python orchestration tools. The repository contains hands-on experiments and learning projects across multiple domains.

## Key Technologies and Tools

- **Tool Management**: Uses `mise` (configured in `mise.toml`) to manage Python 3.10.11 and kubectl
- **Python Projects**: Uses modern Python tooling including `uv` for dependency management
- **Infrastructure**: Azure Bicep templates, Kubernetes manifests, Docker Compose setups
- **Orchestration**: Prefect for workflow orchestration experiments

## Common Development Commands

### Environment Setup
- Install tools: `mise install` (installs Python 3.10.11 and kubectl)
- For Python projects: `uv sync` to install dependencies in virtual environment

### Azure Bicep Development
- Login to Azure: `az login`
- Set default resource group: `az configure --default group="bicep-testing"`
- Deploy Bicep template: `az deployment group create --name deploy01 --template-file bicep-templates/first-template/main.bicep`
- Verify deployment: `az deployment group list --output table`
- Clean up resources: `az deployment group show --name deploy01 --query "properties.outputResources[*].id" --output tsv | xargs -n 1 az resource delete --ids`

### Kubernetes Development
- Use Rancher Desktop for local Kubernetes cluster
- Apply manifests: `kubectl apply -f <manifest-file>`
- Most services are organized in separate directories under `kubernetes/`

### Prefect Orchestration
- Start local server: `prefect server start`
- Run Python scripts directly (prefect will start ephemeral server if needed)
- Working directory: `orchestration-prefect/`
- Uses Python 3.13+ and Prefect 3.3.4+

### Docker Development
- Docker Compose files located in `docker/` subdirectories
- Start services: `docker-compose up -d` (from respective directories)

## Project Structure

- `bicep-templates/`: Azure Infrastructure as Code experiments
- `docker/`: Docker Compose setups for various applications (Airflow, Project Nessie)
- `kubernetes/`: Kubernetes manifests organized by application/service
- `orchestration-prefect/`: Prefect workflow orchestration experiments
- `scripts/`: Utility scripts

## Development Notes

- Each subdirectory contains its own README.md with specific instructions
- Experiments are intentionally rough and incomplete - this is a learning repository
- Local development typically uses Rancher Desktop for Kubernetes and Docker Desktop
- Azure resources are deployed to "germanywestcentral" region by default