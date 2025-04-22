# Airflow

This directory contains docker files related to running Airflow locally.

I am excited about the Airflow 3.0 release today, 2025-04-22. It appears to introduce features I have been looking forward to for a while - mainly about asset-based orchestration and scheduling. The previous lack of such features led me to explore Dagster before.

Now I want to test and evaluate how modern Airflow looks like and feels - potentially as the orchestrator for a range of personal ETL and data projects I have in mind.

The docker-compose.yaml file was fetched following [Airflows documentation on docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html). I may adapt it to my needs a bit more in the future. To fetch the yaml file simply run: `curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.0.0/docker-compose.yaml'`.
