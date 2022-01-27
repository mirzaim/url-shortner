# URL Shortner

This project is a microservice-based URL shortener application deployed using Docker and Kubernetes. The project contains multiple components, including a Python application, Helm charts for managing Kubernetes resources, and Docker configuration files.

## Project Structure

- **app/**: Contains the main application code.
  - **app.py**: The main Python script for the application.
  - **templates/**: HTML templates for rendering web pages.
  
- **Chart/**: Helm chart configuration for deploying the application on Kubernetes.
  - **Chart.yaml**: Metadata about the Helm chart, including the name, version, and description.
  - **values.yaml**: Default values for the Helm chart that can be customized during deployment.

- **docker-compose.yml**: Configuration file for Docker Compose to manage multi-container Docker applications.

- **Dockerfile**: Defines the environment and instructions for building the Docker image for the application.

- **kubernetes/**: Kubernetes YAML configurations for deploying the application.
  - **app-dep.yml**: Deployment file for the application.
  - **configmap.yml**: Configuration file to store non-sensitive application settings.
  - **db-dep.yml**: Deployment file for the database.
  - **db-statefulset.yml**: StatefulSet configuration for ensuring the database runs in a stable and consistent environment.
  - **hpa-dep.yml**: Configuration for the Horizontal Pod Autoscaler.
  - **secret.yml**: Configuration for managing sensitive data such as passwords.
  - **volume.yml**: Configuration file for managing persistent volumes.

- **README.md**: This documentation file.

- **requirements.txt**: Lists the dependencies for the Python application.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mirzaim/url-shortner.git
   cd url-shortner
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Build the Docker image:
   ```bash
   docker build -t url-shortner-image .
   ```

4. Deploy the application using Docker Compose:
   ```bash
   docker-compose up
   ```

## Kubernetes Deployment

1. Create the ConfigMap, Secrets, and Persistent Volume:
   ```bash
   kubectl apply -f kubernetes/configmap.yml
   kubectl apply -f kubernetes/secret.yml
   kubectl apply -f kubernetes/volume.yml
   ```

2. Deploy the database and application:
   ```bash
   kubectl apply -f kubernetes/db-dep.yml
   kubectl apply -f kubernetes/app-dep.yml
   ```

3. (Optional) Apply Horizontal Pod Autoscaler:
   ```bash
   kubectl apply -f kubernetes/hpa-dep.yml
   ```

## Usage

Once the application is deployed, you can use the `/shortit` endpoint to shorten URLs. Here's an example using `curl` to test the API:

1. Shorten a URL:

   ```bash
   curl -X POST http://<your-server-ip>:<your-port>/shortit -H "Content-Type: application/json" -d '{"path_to": "https://www.example.com"}'
   ```

   Replace `<your-server-ip>` and `<your-port>` with the actual IP and port of your deployed application.

2. Visit the shortened URL:

   The response will contain a shortened URL. You can visit this URL, and the system will redirect you to the original URL.
