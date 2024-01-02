# syntax=docker/dockerfile:1
FROM eclipse-temurin:11-jdk-jammy
LABEL version=0.10.0

# API PORT
EXPOSE 1882

ENV PDI_HOME=/home/pdi

# Kitchen hide gtk errors.
ENV FILTER_GTK_WARNINGS=true
ENV SKIP_WEBKITGTK_CHECK=true

# Create the folder where the jobs live
RUN mkdir -p /home/pdi/jobs
RUN mkdir -p /home/pdi/files

# Tools 
RUN apt-get update && apt-get install -y wget unzip

# Download PDI
WORKDIR /tmp
RUN wget https://privatefilesbucket-community-edition.s3.us-west-2.amazonaws.com/9.4.0.0-343/ce/client-tools/pdi-ce-9.4.0.0-343.zip -O pdi.zip
RUN unzip pdi.zip -d /home/pdi/

# Download JDBC MSSQL
RUN wget https://sitsa.dl.sourceforge.net/project/jtds/jtds/1.3.1/jtds-1.3.1-dist.zip -O jtds.zip
RUN unzip jtds.zip
RUN mv *.jar /home/pdi/data-integration/lib/

# Install basic dependencies
RUN apt-get update && apt-get install -y python3 python3-pip sqlite3

# Copy source files
COPY chef /srv/chef

# Install python dependencies
WORKDIR /srv/chef
RUN pip install -r requirements.txt
RUN sqlite3 chef.db < create_tables.sql 

CMD gunicorn --config gunicorn_conf.py app:app
