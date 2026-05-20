# Subnet Calculator

This is a simple subnet calculator app that runs on Python and Flask. As a sysadmin I have long wanted to increase my familiarity and facility with Docker, so the goal of this project is to containerize the app and deploy it behind an nginx reverse proxy on Ubuntu Server.

## Steps to build and run:

Clone the repository and move into project directory:

`git clone https://github.com/michaelacook/flask-subnet-calculator.git && cd flask-subnet-calculator`

Build the container:

`docker build -t flask-subnet-calculator .`

Run:

`docker run -p 8080:5000 --detach flask-subnet-calculator`