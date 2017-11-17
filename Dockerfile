FROM resin/rpi-raspbian:latest
MAINTAINER robe16

# Port number to listen on
ARG portApplication
ENV portA ${portApplication}
ARG portBroadcast
ENV portB ${portBroadcast}

# Update
RUN apt-get update && apt-get install -y python python-pip

WORKDIR /jarvis/lgtv_netcast

# Bundle app source
COPY src /jarvis/lgtv_netcast

# Copy app dependencies
COPY requirements.txt requirements.txt

# Install app dependencies
RUN pip install -r requirements.txt

# Run application
CMD python run.py ${portA} ${portB}
