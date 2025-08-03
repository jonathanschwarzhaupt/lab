# Kubernetes - Airflow

Install the helm repository and chart using

```bash
helm repo add apache-airflow https://airflow.apache.org
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace
```

The first command will add the Helm repository and the second will deploy Airflow to the cluster using the Chart's default configuration.

You will see the following output your terminal, showing that the deployment succeeded and outputting the port forward command to use to access the airflow web ui.

```bash
Release "airflow" does not exist. Installing it now.
NAME: airflow
LAST DEPLOYED: Sun Jul 20 15:26:16 2025
NAMESPACE: airflow
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Thank you for installing Apache Airflow 3.0.2!

Your release is named airflow.
You can now access your dashboard(s) by executing the following command(s) and visiting the corresponding port at localhost in your browser:
Airflow API Server:     kubectl port-forward svc/airflow-api-server 8080:8080 --namespace airflow
Default Webserver (Airflow UI) Login credentials:
    username: admin
    password: admin
Default Postgres connection credentials:
    username: postgres
    password: postgres
    port: 5432

You can get Fernet Key value by running the following:

    echo Fernet Key: $(kubectl get secret --namespace airflow airflow-fernet-key -o jsonpath="{.data.fernet-key}" | base64 --decode)

###########################################################
#  WARNING: You should set a static webserver secret key  #
###########################################################

You are using a dynamically generated webserver secret key, which can lead to
unnecessary restarts of your Airflow components.

Information on how to set a static webserver secret key can be found here:
https://airflow.apache.org/docs/helm-chart/stable/production-guide.html#webserver-secret-key
```

To remove the deployment, run:

````
helm delete airflow --namespace airflow
```

After confirming that the airflow deployment is up and the webserver can be accessed, you can specify your values override like so:

```bash
helm repo add apache-airflow https://airflow.apache.org
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace -f kubernetes/airflow/values.yaml
```

The Airflow deployment will not contain any DAGs at first. To load Airflow's example DAGs, run this command
```bash
export NAMESPACE=airflow
export RELEASE_NAME=airflow

helm upgrade --install $RELEASE_NAME apache-airflow/airflow \
  --namespace $NAMESPACE \
  --set-string "env[0].name=AIRFLOW__CORE__LOAD_EXAMPLES" \
  --set-string "env[0].value=True"
```

You should see Airflow re-deploying the services and loading the DAGs. Port forward the api server service and access the Airflow UI from localhost:8080 - the example DAGs should now be loaded.

To use Airflow with a custom image, e.g. that has python dependencies available or DAGs baked in, push your image to a container registry (or build locally and load to your cluster) and run the command like so:
```bash
helm upgrade --install airflow apache-airflow/airflow --namespace airflow \
--set images.airflow.repository=ghcr.io/jonathanschwarzhaupt/plumbing-airflow \
--set images.airflow.tag=v0.2.2
```

To install the airflow chart using custom values override, use this command:
```bash
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace -f values.yaml
```


## Links
https://airflow.apache.org/docs/helm-chart/1.6.0/
````
