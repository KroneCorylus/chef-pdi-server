import os

PDI_HOME = os.getenv('PDI_HOME', '/home/pdi')
LOG_RETENTION = os.getenv('LOG_RETENTION', '30')
SECRET_KEY = os.getenv('CHEF_SECRET_KEY')
JOBS_FILE = os.getenv('JOBS_FILE', 'jobs.yaml')
SECUENCES_FILE = os.getenv('SECUENCES_FILE', 'secuences.yaml')
