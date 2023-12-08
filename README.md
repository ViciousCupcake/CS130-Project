

# CS130 EFi Project

## Overview
In our EFi project, we've streamlined the development workflow by implementing an automated build and test process. In the following sections, we will describe the process to build, run, and test our project.

## Building the project

### Prerequisites
- Ensure Docker Desktop is installed and running on your machine.

### Build Process
  **Setting Up the Environment**:
   - Execute `./start.sh` in the project root directory. This script initializes the Docker environment, as well as sets up the three containers required for our project.
   - After the initial setup is completed, the Django server is automatically started for local access.
   - To gracefully stop the server, press `Ctrl + C` to shut down the server.
   - NOTE: Failing to gracefully shut down the server may result in problems with the database and you may have to rebuild the whole project.

## Running the Project
- To run the project after initial setup, execute `./start.sh` in the project root directory.
- Fuseki is available at localhost:3030
- Django is available at localhost:8000
- To gracefully stop the server, press `Ctrl + C` to shut down the server.
- NOTE: Failing to gracefully shut down the server may result in problems with the database and you may have to rebuild the whole project. 

## Testing the Application

### Running Tests
- We employ Django's built-in testing framework, with tests defined in `tests.py`.
- **Test Execution**:
  - To run tests, navigate to the terminal of the Web container in Docker and run `python manage.py test`.
### Admin Access
For admin access to test admin-only features in our project, use the following credentials:
- **Fuseki Admin Username**: `admin`
- **Fuseki Admin Password**: `postgres`

## Documentation

### User Manual
- The User Manual is accessible at the following URL:
https://github.com/ViciousCupcake/CS130-Project/wiki
### API Documentation
- The API Documentation is accessible at the following URL:
[http://ec2-34-217-96-31.us-west-2.compute.amazonaws.com/](http://efi.jonathan-xu.com/)

TODO: update the below shields.
[![Build Status](https://app.travis-ci.com/melaasar/cs130-template.svg?branch=master)](https://app.travis-ci.com/github/melaasar/cs130-template)
[![Release](https://img.shields.io/github/v/release/melaasar/cs130-template?label=release)](https://github.com/melaasar/cs130-template/releases/latest)
