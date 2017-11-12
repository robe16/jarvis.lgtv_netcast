FROM resin/rpi-raspbian:latest
MAINTAINER robe16

# Port number to listen on
ARG service_id
ARG self_hostport

# Update
RUN apt-get update && apt-get install -y python python-pip

WORKDIR /jarvis/lgtv_netcast

# Bundle app source
COPY src /jarvis/lgtv_netcast

# Copy app dependencies
COPY requirements.txt requirements.txt

# Install app dependencies
RUN pip install -r requirements.txt

# Expose the application port and run application
EXPOSE ${portApplication}
CMD python run.py ${service_id} ${self_hostport}
