# Subnet Calculator

This is a simple subnet calculator app that runs on Python and Flask. The goal of this project is to containerize an app and deploy it behind an Nginx reverse proxy. As a system administrator who works closely with developers, it is my goal to begin understanding containerization and container orchestration.

The application image is pulled from Docker Hub along with Nginx. Docker Compose mounts the Nginx configuration and configures it as a reverse proxy in front of the application container.

## Running the application:

Clone the repository and move into project directory:

`git clone https://github.com/michaelacook/flask-subnet-calculator.git && cd flask-subnet-calculator`

Run the application:

`docker compose up -d`