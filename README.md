# CS130 EFi Project

## Overview
In our EFi project, we've streamlined the development workflow by implementing an automated build and test process. In the following sections, we will describe the process to build, run, and test our project.

## Building the project
The build process is done via GitHub Actions. Our CI setup, defined in `.github/workflows/test.yml`, automatically triggers on every code commit. This CI pipeline is triggered to activate upon code commits or pull requests to the master branch. Once triggered, the pipeline checks out the latest version of the code, ensuring that the most recent changes are included in the integration process. It then sets up the Docker environment as defined in docker-compose.yml to complete the build. Following this, Django tests are executed and the outcome of these tests is then reported.

If you wish to build on your local machine, please follow the following steps:
### Prerequisites
- Ensure Docker Desktop is installed and running on your machine.

### Build Process
   - Execute `./start.sh` in the project root directory. This script initializes the Docker environment, as well as sets up the three containers required for our project.
   - After the initial setup is completed, the Django server is automatically started for local access.
   - To gracefully stop the server, press `Ctrl + C` to shut down the server.
   - NOTE: Failing to gracefully shut down the server may result in problems with the database and you may have to rebuild the whole project.

## Running the Project
- To run the project after initial setup, execute `./start.sh` in the project root directory.
- Fuseki is available at `localhost:3030`
- Django is available at `localhost:8000`
- To gracefully stop the server, press `Ctrl + C` to shut down the server.
- NOTE: Failing to gracefully shut down the server may result in problems with the database and you may have to rebuild the whole project. 

## Testing the Project

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
https://efi.jonathan-xu.com/
https://github.com/ViciousCupcake/CS130-Project/actions/workflows/test.yml/badge.svg
TODO: update the below shields.
[![Build Status](https://github.com/ViciousCupcake/CS130-Project/actions/workflows/test.yml/badge.svg)

[![Release](https://img.shields.io/github/v/release/melaasar/cs130-template?label=release)](https://github.com/melaasar/cs130-template/releases/latest)
