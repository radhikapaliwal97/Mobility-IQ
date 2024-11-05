# Mobility iQ - Backend Take-Home Assignment

## Overview

This project is a simple CRUD application built using FastAPI and SQLAlchemy, containerized with Docker Compose.

## Prerequisites

To run this project, ensure you have the following installed:

- Docker
- Docker Compose

## Quick Start

### 1. Clone the Repository

First, clone the repository and navigate to the project directory:

```bash
git clone <repository_url>
cd <repository_directory>
```


2. **Create a .env File**
Create a .env file in the project root with the following configuration:

```bash
DB_USER=postgres
DB_PASSWORD=db_password
DB_NAME=db_name
DB_HOST=db
DB_PORT=5432
```

3. **Start the Application**
Use Docker Compose to start the application:
```
docker-compose --env-file .env up
```

4. **Access the Swagger API Documentation**
Once the application is running, you can access the Swagger API documentation at:

http://127.0.0.1:8000/docs


## Running Test Cases
1. **Create a test.env File**
For running tests, create a test.env file in the project root with the following configuration:
```bash
DB_USER=postgres
DB_PASSWORD=db_password
DB_NAME=test
DB_HOST=test_db
DB_PORT=5432
```

2. **Run Test Cases**
``` bash
docker-compose -f docker-compose.test.yml --env-file test.env up --abort-on-container-exit --build
```

This will build the test environment, execute the tests, and shut down the containers after completion.

Note: Ensure that the .env and test.env files are configured correctly with your database credentials.


