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
  * Run using command `docker-compose up -d && docker attach CONTAINER-NAME` (project-app-1)
  * Enter filename
  * Specify sorting method
  * Use keyboard inputs "1", "2", "3" and "4" to interact with program as necessary
