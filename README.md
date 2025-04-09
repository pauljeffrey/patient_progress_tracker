# Patient Progress Tracker

## Overview

This application helps therapists analyze patient progress across therapy sessions. It is designed to be used as a module in bigger AI workflow as its sole function is to track symptoms and progress of patients during therapy sessions. It includes:
- A backend for processing therapy session files, scoring and weighting symptoms over sessions and generating insights.
- A frontend for visualizing diagnosis, symptom tracking, and cumulative progress.

## Features

- Upload multiple therapy session files in JSON or TXT format.
- View patient diagnosis and cumulative progress score.
- Summarize symptoms progress in text.
- Visualize symptom trends with a graph.

---

## How to Run Using Docker

### Prerequisites
1. Install [Docker](https://www.docker.com/get-started).
2. Install [Docker Compose](https://docs.docker.com/compose/install/).

### Steps to Run
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. Build and start the Docker containers:
    ```bash
    docker-compose up --build

3. Access the application:
        Frontend: http://localhost:8501
        Backend: http://localhost:8000/docs (for API documentation)

<b> Note: Make sure to specify an openai api key at least in a .env file. </b>

3. Stop the Application

    To stop the application, run:
    ```bash
    docker-compose down


