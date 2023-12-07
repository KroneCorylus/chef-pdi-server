# syntax=docker/dockerfile:1
FROM eclipse-temurin:11-jdk-jammy

# install the app
COPY pdiserver /srv/pdiserver
# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip vim
#RUN pip install flask==2.1.* werkzeug==2.2.2 pyyaml
WORKDIR /srv/pdiserver
RUN pip install -r requirements.txt
RUN apt install -y wget unzip

# create the folder where the jobs live
RUN mkdir -p pdiserver/jobs

#download pdi and jdcb
WORKDIR /tmp
RUN wget https://privatefilesbucket-community-edition.s3.us-west-2.amazonaws.com/9.4.0.0-343/ce/client-tools/pdi-ce-9.4.0.0-343.zip -O pdi.zip
RUN unzip pdi.zip -d /pdiserver/
RUN wget https://sitsa.dl.sourceforge.net/project/jtds/jtds/1.3.1/jtds-1.3.1-dist.zip -O jtds.zip
RUN unzip jtds.zip
RUN mv *.jar /pdiserver/data-integration/lib/

# final configuration
ENV PDI_HOME=/pdiserver
# PDI env variables to supress gtk errors
ENV FILTER_GTK_WARNINGS=true
ENV SKIP_WEBKITGTK_CHECK=true

WORKDIR /srv/pdiserver
EXPOSE 1882
CMD flask run --host 0.0.0.0 --port 1882
