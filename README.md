# Patient Progress Tracker

## Overview

This application helps therapists analyze patient progress across therapy sessions. It includes:
- A backend for processing therapy session files and generating insights.
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

    docker-compose up --build

3. Access the application:
        Frontend: http://localhost:8501
        Backend: http://localhost:8000/docs (for API documentation)

Stop the Application

To stop the application, run:

docker-compose down

Deployment
Deploy with Docker Compose

    Modify docker-compose.yml to set BACKEND_URL for the frontend.
    Deploy the Docker Compose setup to a cloud server like AWS EC2, GCP, or Azure.

Frontend Deployment

You can use Streamlit Cloud for frontend hosting. Ensure the backend URL is accessible publicly.
Testing and Debugging

    Test the backend independently using Swagger UI at http://localhost:8000/docs.
    Ensure all required ports (8000 and 8501) are open and not blocked by firewalls.

License

This project is open-source and available under the MIT License.


---

### **4. How to Deploy**

- **Local Deployment**: Follow the steps under "How to Run Using Docker."
- **Cloud Deployment**: Push the code to a cloud server with Docker installed. Use `docker-compose` commands to deploy.

This setup makes it easy to run, test, and deploy the app quickly! Let me know if you need more help!


