
<h1>Chef-PDI-server</h1> 

Chef is simple web server that provides a HTTP API for running Pentaho Data Integration (a.k.a Kettle) Jobs.

------------
<p align="center">***NOT READY FOR PRODUCTION*** </p>


------------


<h3>Features</h3> 

- Simple installation via Docker Image.
- Run jobs on demand via HTTP request.
- Set default parameters or pass them as parameters on the request (overwrite default ones).
- Pre-configure and run secuences of jobs.
- Access logs from finish executions.
- API end point to get available parameters of a job.

<h3>Planed Features</h3>

- Authorization with JWT.
- Abort Jobs (by killing pdi process).


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
  another_job_name:
    level: Minimal 
    path: job2.kjb
    default_parameters:
      param1: 'test'
      param2: 'test'
```
<h3>Secuences</h3>
Secuences are a list of jobs you want to run consecutively. You can declare what jobs are part of a secuence declaring them in secuences.yaml using the job name declared on jobs.yaml

```yaml
secuences:
  unique_secuence_name:
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

| End point | Method | Description                    |
| ------------- | ----------------------------------------------- | ----- |
| `/jobs`      | List all jobs available.       | GET |
| `/jobs/<unique_job_name>`   | Describe job     | GET |
| `/jobs/<unique_job_name>/executions`   | List all executions of a job     | GET |
| `/jobs/<unique_job_name>/executions`   | Execute a job     | POST |
| `/jobs/<unique_job_name>/executions/<id>`   | Get log from execution     | GET |

<h3>Secuences</h3>

| End point | Method | Description                    |
| ------------- | ----------------------------------------------- | ----- |
| `/secuences`   | List all secuences available     | GET |
| `/secuences/<unique_secuence_name>`   | Describe secuence     | GET |
| `/secuences/<unique_secuence_name>/executions`   | ~~List all executions of a secuence~~     | ~~GET~~ |
| `/secuences/<unique_secuence_name>/executions`   | Execute a secuence     | POST |

