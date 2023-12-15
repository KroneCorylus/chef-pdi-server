
# Chef-PDI-server

Chef is simple web server that provides a HTTP API for running Pentaho Data Integration (a.k.a Kettle) Jobs.

------------

***NOT READY FOR PRODUCTION***

------------


### Features
- Simple installation via Docker Image.
- Run jobs on demand via HTTP request.
- Set default parameters or pass them as parameters on the request (overwrite default ones).
- Pre-configure and run secuences of jobs.
- Access logs from finish executions.
- API end point to get available parameters of a job.

### Planed Features
- Authorization with JWT.
- Abort Jobs (by killing pdi process).


**Table of Contents**

[TOC]


##Installation
####Clone repository
```
$ git clone git@github.com:KroneCorylus/chef-pdi-server.git
```
####Build image
Inside the cloned directory run:
```
$ docker build .
```
####Start with docker compose
```
$ docker compose up
```

##Configuration
###Jobs
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
###Secuences
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

##API Usage
###Jobs
| End point | Method | Description                    |
| ------------- | ----------------------------------------------- | ----- |
| `/jobs`      | List all jobs available.       | GET |
| `/jobs/<unique_job_name>`   | Describe job     | GET |
| `/jobs/<unique_job_name>/executions`   | List all executions of a job     | GET |
| `/jobs/<unique_job_name>/executions`   | Execute a job     | POST |
| `/jobs/<unique_job_name>/executions/<id>`   | Get log from execution     | GET |
###Secuences
| End point | Method | Description                    |
| ------------- | ----------------------------------------------- | ----- |
| `/secuences`   | List all secuences available     | GET |
| `/secuences/<unique_secuence_name>`   | Describe secuence     | GET |
| `/secuences/<unique_secuence_name>/executions`   | ~~List all executions of a secuence~~     | ~~GET~~ |
| `/secuences/<unique_secuence_name>/executions`   | Execute a secuence     | POST |

