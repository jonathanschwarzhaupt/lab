# Airflow

This directory contains docker files related to running Airflow locally.

I am excited about the Airflow 3.0 release today, 2025-04-22. It appears to introduce features I have been looking forward to for a while - mainly about asset-based orchestration and scheduling. The previous lack of such features led me to explore Dagster before.

Now I want to test and evaluate how modern Airflow looks like and feels - potentially as the orchestrator for a range of personal ETL and data projects I have in mind.

The docker-compose.yaml file was fetched following [Airflows documentation on docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html). I may adapt it to my needs a bit more in the future. To fetch the yaml file simply run: `curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.0.0/docker-compose.yaml'`.

I encountered an issue with the original docker compose file. The worker was not able to authenticate the token to obtain the DAG bundle resulting in instantly failed DAGs. This was the error from the worker logs:
```bash
2025-04-23 18:15:02.920585 [info     ] Task execute_workload[d6c8d527-9a04-4eac-bf93-62470822e813] received [celery.worker.strategy]
2025-04-23 18:15:02.934052 [info     ] [d6c8d527-9a04-4eac-bf93-62470822e813] Executing workload in Celery: token='eyJ***' ti=TaskInstance(id=UUID('019663dc-4697-76b5-b1c7-0f7bdbc672a7'), task_id='producing_task_2', dag_id='asset_produces_2', run_id='manual__2025-04-23T18:15:02.540391+00:00', try_number=1, map_index=-1, pool_slots=1, queue='default', priority_weight=1, executor_config=None, parent_context_carrier={}, context_carrier={}, queued_dttm=None) dag_rel_path=PurePosixPath('example_assets.py') bundle_info=BundleInfo(name='example_dags', version=None) log_path='dag_id=asset_produces_2/run_id=manual__2025-04-23T18:15:02.540391+00:00/task_id=producing_task_2/attempt=1.log' type='ExecuteTask' [airflow.providers.celery.executors.celery_executor_utils]
2025-04-23 18:15:02.960424 [info     ] Secrets backends loaded for worker [supervisor] backend_classes=['EnvironmentVariablesBackend'] count=1
2025-04-23 18:15:03.068147 [warning  ] Server error                   [airflow.sdk.api.client] detail=None
2025-04-23 18:15:03.072603 [info     ] Process exited                 [supervisor] exit_code=-9 pid=213 signal_sent=SIGKILL
2025-04-23 18:15:03.079783 [error    ] Task execute_workload[d6c8d527-9a04-4eac-bf93-62470822e813] raised unexpected: ServerResponseError('Invalid auth token: Signature verification failed') [celery.app.trace]
```
To fix the issue, I added two env values to the `x-airflow-common` service template (or YAML anchor):
```yaml
  ...
  environment:
    &airflow-common-env
    ...
    AIRFLOW__WEBSERVER__SECRET_KEY: "super_secret_key"
    AIRFLOW__API_AUTH__JWT_SECRET: "super_secret_key"
```
And it did the trick! 

Interestingly, the `apache/airflow:3.0.0` image comes with a number of example DAGs! I did not know this and it was fun to explore the new asset-based scheduling DAGs!