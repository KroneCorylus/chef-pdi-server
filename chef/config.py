import os

PDI_HOME = os.getenv('PDI_HOME', '/home/pdi')
LOG_RETENTION = os.getenv('LOG_RETENTION', '30')
SECRET_KEY = os.getenv('CHEF_SECRET_KEY')
