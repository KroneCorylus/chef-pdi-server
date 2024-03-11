
<h1>Chef-PDI-server</h1> 

Chef is simple web server that provides a HTTP API for running Pentaho Data Integration (a.k.a Kettle) Jobs.

------------

<h3>Features</h3> 

- Simple installation via Docker Image.
- Run jobs on demand via HTTP request.
- Set default parameters or pass them as parameters on the request (overwrite default ones).
- Pre-configure and run sequences of jobs.
- Access logs from finish executions.
- API end point to get available parameters of a job.
- Authorization with JWT.

<h3>Planed Features</h3>

- Abort Jobs

<h2>Installation</h2>
<h4>Clone repository</h4>

```shell
$ git clone git@github.com:KroneCorylus/chef-pdi-server.git
```

<h4>Build image</h4>

Inside the cloned directory run:

```shell
$ docker build .
```

<h4>Start with docker compose</h4>

```shell
$ docker compose up
```

<h2>Configuration</h2>

<h3>Jobs</h3>
Using the docker compose to start the image you should have a volume map to a directory inside your cloned repository called jobs (you can change this inside the compose.yaml file) where you will put your jobs (.kjb files).

Inside that folder you can declare your jobs using a jobs.yaml file with this format:
```yaml
jobs:
  unique_job_name:
    level: Debug 
    path: test/job1.kjb
    default_parameters:
      param1: 'test'
      param2: 'test'
      param3: 'test'
    hidden_parameters:
      - 'param1'
      - 'param2'
  another_job_name:
    level: Minimal 
    path: job2.kjb
    default_parameters:
      param1: 'test'
      param2: 'test'
```
<h3>sequences</h3>
sequences are a list of jobs you want to run consecutively. You can declare what jobs are part of a sequence declaring them in sequences.yaml using the job name declared on jobs.yaml

```yaml
sequences:
  unique_sequence_name:
    - job: 'unique_job_name'
      parameter_overwrites:
        param1: 'test1'
        param3: 'test1'
    - job: 'another_job_name'
      parameter_overwrites:
        param2: 'test2'
```


<h2>API Usage</h2>

<h3>Jobs</h3>

| Endpoint | Description | Method                    |
| ------------- | ----------------------------------------------- | ----- |
| `/jobs`      | List all jobs available.       | GET |
| `/jobs/<unique_job_name>`   | Describe job     | GET |
| `/jobs/<unique_job_name>/executions`   | List all executions of a job     | GET |
| `/jobs/<unique_job_name>/executions`   | Execute a job     | POST |
| `/jobs/<unique_job_name>/executions/<id>`   | Get log from execution     | GET |

<h3>sequences</h3>

| Endpoint | Description | Method                    |
| ------------- | ----------------------------------------------- | ----- |
| `/sequences`   | List all sequences available     | GET |
| `/sequences/<unique_sequence_name>`   | Describe sequence     | GET |
| `/sequences/<unique_sequence_name>/executions`   | List all executions of a sequence     | GET |
| `/sequences/<unique_sequence_name>/executions`   | Execute a sequence     | POST |


<h2>Enviroment variable</h2>

| Variable | Description | Default value                     |
| ------------- | ----------------------------------------------- | ----- |
| `CHEF_SECRET_TOKEN`   | Token used for JWT token signature validation. |  |
| `PDI_HOME`   | Home directory for PDI. | /home/pdi |
| `JOBS_FILE`   | File name with job configurations. | jobs.yaml |
| `SEQUENCES_FILE`   | File name with sequences configurations. | jobs.yaml |
| `CHEF_ROLE`   | Role requiered in payload of JWT token for api usage |  |
| `LOG_RETENTION`   | Log retention in days | 30 |
| `GUNICORN_PROCESSES`   | Number of gunicorn workers | 4 |
| `GUNICORN_THREADS`   | | 2 |
| `GUNICORN_BIND`   |  | 0.0.0.0:1882 |


<h2>Development</h2>

To develop and expand this proyect you can use the compose file compose-dev.yaml like this:
```
docker compose -f compose-dev.yaml up
```
This will make a docker volume of source files directory and inicialize flask in Debug mode for hotreloading of your changes. 


