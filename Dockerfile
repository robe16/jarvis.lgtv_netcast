FROM resin/rpi-raspbian:latest
MAINTAINER robe16

# Port number to listen on
ARG portApplication
ARG portMapped

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
CMD python run.py ${portMapped}
