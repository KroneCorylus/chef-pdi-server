# syntax=docker/dockerfile:1
FROM eclipse-temurin:11-jdk-jammy

# install the app
COPY chef /srv/chef
# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip vim sqlite3
#RUN pip install db-sqlite3
WORKDIR /srv/chef
RUN pip install -r requirements.txt
RUN apt install -y wget unzip

# create the folder where the jobs live
RUN mkdir -p /home/pdi/jobs
RUN mkdir -p /home/pdi/files

#download pdi and jdcb
WORKDIR /tmp
RUN wget https://privatefilesbucket-community-edition.s3.us-west-2.amazonaws.com/9.4.0.0-343/ce/client-tools/pdi-ce-9.4.0.0-343.zip -O pdi.zip
RUN unzip pdi.zip -d /home/pdi/
RUN wget https://sitsa.dl.sourceforge.net/project/jtds/jtds/1.3.1/jtds-1.3.1-dist.zip -O jtds.zip
RUN unzip jtds.zip
RUN mv *.jar /home/pdi/data-integration/lib/

# final configuration
ENV PDI_HOME=/home/pdi
# PDI env variables to supress gtk errors
ENV FILTER_GTK_WARNINGS=true
ENV SKIP_WEBKITGTK_CHECK=true

WORKDIR /srv/chef

RUN sqlite3 chef.db < create_tables.sql 

EXPOSE 1882
CMD flask run --host 0.0.0.0 --port 1882
