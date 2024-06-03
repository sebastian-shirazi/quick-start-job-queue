# Quickstart Project
A custom queue structure that handles file and commandline requests

---

## Overview
This project simulates a job queue using a priority queue to add / execute jobs. Program reads from user file input and creates a queue based on parsed lines integer priority.

---

## To Run
### VSCode (IDE)
  * Place file to be read in root directory of main.py (optional)
  * Run using run button
  * Enter filename if in root directory or filepath if located elsewhere
  * Specify sorting method
  * Use keyboard inputs "1", "2", "3" and "4" to interact with program as necessary

### Docker (Via command line)
  * Place file to be read in root directory of main.py
  * Build environment using `docker build - < Dockerfile`
  * Run using command `docker-compose up -d && docker attach CONTAINER-NAME`
  * Enter filename
  * Specify sorting method
  * Use keyboard inputs "1", "2", "3" and "4" to interact with program as necessary


# Quickstart + Project
An addition to the Quickstart project that involves creating a RESTful API for the custom queue structure

---

## Overview
This project simulates a Dockerized priority queue application with a RESTful interface. User uses curl commands in order to get, modify, or delete data from the queue to simulate job execution / addition

---

## To Run
  * CD into project directory
  * Use `docker compose up flask-app` to run the conatiner and app
  * Use curl commmands to interact with the app
    * * For `GET` methods, use curl http://localhost:5000/ ... without specifying type of action
    * * Use curl http://localhost:5000/FILENAME in order to initialize and load queue from file
    * * User curl http://localhost:5000/SORTINGMETHOD/jobs in order to resort the initialized queue by either "fifo", "lifo" or "priority"
    * * Use curl http://localhost:5000/jobs in order to retrieve the first job from the queue
    * * Use curl http://localhost:5000/jobs/status in order to retrieve the queue and execution times of the jobs
    * * Use curl http://localhost:5000/jobs/JOBNUM to retrieve a job from the queue by number in the queue
    * * Use curl -X POST http://localhost:5000/jobs -H "Content-Type: application/json" -d '{"uuid": "some_uuid", "name": "some_name", "priority": "some_priority (int)", "exec_time": "some_exec_time (int)"}' in order to post a job to the queue
    * * Use curl -X DELETE http://localhost:5000/jobs to delete first job in queue, curl -X http://localhost:5000/jobs/all to delete all the jobs in the queue, curl -X DELETE http://localhost:5000/jobs/UUID to delete a job by uuid

