FROM python:3.9-slim-buster

# Updating Packages
RUN apt update && apt upgrade -y
RUN apt install git curl python3-pip ffmpeg -y

# Copying Requirements
COPY requirements.txt /requirements.txt

# Installing Requirements
RUN cd /
RUN pip3 install --upgrade pip
RUN pip3 install -U -r requirements.txt

# Setting up working directory
RUN mkdir /MusicPlayer
WORKDIR /MusicPlayer

# Preparing for the Startup
COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

# Running Music Player Bot
CMD ["/bin/bash", "/startup.sh"]
