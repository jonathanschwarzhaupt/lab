My notes as I go along:

Project Nessie is an open-source transactional data catalogue over Apache Iceberg tables. 

To test out Project Nessie locally, we can utilize Docker. Conveniently, the Nessie team has provided a guide for getting started with the server or cli individually.

I created the following docker compose file based on their material. The file essentially puts both containers into the same docker network, making accessing the server from the cli easy. Here, a short excerpt:

```docker-compose.yaml
services:  
  nessie-server:  
    image: ghcr.io/projectnessie/nessie:0.103.3  
    container_name: nessie-server  
    ports:  
      - "19120:19120"  
      - "9000:9000"  
  
  nessie-cli:  
    image: ghcr.io/projectnessie/nessie-cli:0.103.3  
    container_name: nessie-cli  
    stdin_open: true   # -i  
    tty: true          # -t  
    profiles:  
      - cli  
    depends_on:  
      - nessie-server
```


Start the server in detached mode using `docker compose up -d`. Then we can start the interactive CLI REPL using `docker compose run nessie-cli`. 
The docker compose file leverages `profiles` which only runs the services tagged with profiles when the respective profile is called.

With the CLI REPL active, we can connect to the Nessie Server using `CONNECT TO http://nessie-server:19120/api/v2`. Once connected we can explore the list of available commands using `HELP`or by referring to the CLI reference.

Let's run some test commands to try out:
- `create namespace my_new_namespace`: Creates a new namespace. Reminds me of "folders" or "database schemas"
- `create branch if not exists my_new_branch from main`: Creates a new branch - much like git branches does for code, Nessie enables isolated and version controlled actions on data
- To use the newly created branch we execute `use branch my_new_branch`. The REPL conveniently displays the current branch like so: `my_new_branch>`
- We can then create a new namespace in our own branch. When we check in the UI of the `nessie-sever`accessible via `http://127.0.0.1:19120` we can see that the new namespace is only visible in the branch `my_new_branch`but not on the `main`branch
- Finally, we can exit the REPL using `exit`

Now, let's explore pyiceberg and add some data to our catalogue.
First, create a python virtual environment, e.g. `uv venv` then install the packages listed in `requirements.txt`, using e.g. `uv pip install -r requirements.txt`.

To interactively run python code, we can leverage [marimo](https://docs.marimo.io/). Run `marimo edit` to open the web ui and run the cells defined in `project-nessie-pyiceberg.py`.
The file contains some code snippets to interact with the Nessie server we have running in our Docker container. 
For example, we can create tables using pyiceberg schemas, or using pyarrow schemas. I imagine the latter can be very useful in the context of ETL pipelines where data is marshalled into polars dataframes for example.

At first, I had issues with the configuration of the catalogue. When attempting to write to a previously defined table, the catalog would throw a connection error, indicating that it could not find `minio:9000`. To resolve the issue, I had to amend the docker compose file and add a `external-endpoint`configuration to the `nessie-server`which it uses to forward to clients. 

Next, I am interested in further exploring Nessie's git-like semantics for implementing a write-audit-publish (WAP) pattern. I could see a rough process like: an Airflow run obtains new data, creates a branch based on the table name to update and its task_id, inserts the new data, runs quality checks, and when successful, merge the branch into the main branch.

## Links
- https://projectnessie.org/downloads/
- https://docs.docker.com/compose/how-tos/profiles/
- https://projectnessie.org/nessie-0-103-3/cli/
- https://www.dremio.com/blog/intro-to-pyiceberg/
- https://py.iceberg.apache.org/api/


20250423114715