# Trying out prefect

This directory contains scripts and other files to test [prefect](https://docs.prefect.io/v3/get-started) locally.

I have become interested in prefect as it presents itself as a modern Airflow alternative, with a cloud-native architecture, a pythonic approach to orchestration, and without the "constraints" and boilerplate a DAG has.

Let's see how easy or difficult it is to get a script up and running on prefect and what it takes to dockerize this application.

## Getting started

This project uses uv to manage python version and dependencies. Sync the dependencies to a venv and run `prefect server start` to start a local prefect server. Make sure to update your prefect config with the PREFECT_API_URL.

Alternatively, just run your python scripts and prefect will start an ephemeral server.


