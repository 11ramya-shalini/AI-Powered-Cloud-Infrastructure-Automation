# AI-Powered Cloud Automation Tool
This project showcases a self-scaling cloud-native application deployed on Kubernetes, powered by Horizontal Pod Autoscaler (HPA) using CPU metrics and real-time monitoring with stress testing.
## 📌 Overview
This project automates cloud infrastructure management using **Kubernetes**. It includes AI-powered scaling recommendations, automated deployments, and real-time monitoring — ensuring resource-efficient infrastructure operation.

## 🚀 Features

- ⚙️ Dockerized Flask/Streamlit Web App
- ☸️ Kubernetes Deployment Automation
- 📦 Image pushed to Docker Hub
- 📊 Metrics Server + Horizontal Pod Autoscaler
- 🧪 Stress test to trigger autoscaling
- 📈 Real-time `kubectl top` metrics & HPA scaling
- 📺 Prometheus/Grafana Integration (in progress)

## 🔧🧰 Technologies Used

- **Python (Flask / Streamlit)** – Web Interface
- **Docker** – Containerization
- **Kubernetes** – Container Orchestration
- **Metrics Server** – CPU/Memory Monitoring
- **Horizontal Pod Autoscaler (HPA)** – Auto-scaling
- **Bash Scripting** – Automation
- **Prometheus & Grafana** – Monitoring Dashboards 

## ⚙️ How It Works

1. Web app containerized and pushed to Docker Hub.
2. Kubernetes deployment runs the app with 2 replicas.
3. HPA watches CPU usage using Metrics Server.
4. When CPU load increases, pods automatically scale up.
5. When load drops, pods scale down to save resources.

## 📦 Docker Image
```sh
docker pull ramyashalini/my-cloud-auto-app:latest
```

## 🔥 HPA in Action

Example after triggering load via stress:
```sh
kubectl get hpa
NAME                    TARGETS       MINPODS   MAXPODS   REPLICAS
cloud-auto-deployment   cpu: 93%/50%   2         5         5
```
```sh
kubectl top pods
NAME                                    CPU(cores)   MEMORY(bytes)
cloud-auto-deployment-xxxx              254m         62Mi
...
```
## Real-Time Log Monitoring with Loki & Fluent Bit

Integrated real-time observability into the cloud infrastructure by setting up a log monitoring pipeline using:

🔥 Fluent Bit

Lightweight log forwarder deployed as DaemonSet

📦 Loki

Log aggregation system (Prometheus-style logs)

📊 Grafana

Visualization tool to query logs from Loki

📁 Helm

Used for installing and configuring the above tools


## 🛠 Setup Instructions
1. Clone the repository:
   ```sh
   git clone https://github.com/11ramya-shalini/AI-Powered-Cloud-Infrastructure-Automation.git
   cd AI-Powered-Cloud-Infrastructure-Automation

2. Build and push Docker image
   ```sh
   docker build -t ramyashalini/my-cloud-auto-app .
   docker push ramyashalini/my-cloud-auto-app

3. Deploy to Kubernetes:
   ```sh
   kubectl apply -f deployments/

4. Check HPA scaling:
   ```sh
   kubectl get hpa
   kubectl top pods

5. Run stress in one pod (to simulate load):
   ```sh
   kubectl exec -it <pod-name> -- sh
   apt-get update && apt-get install -y stress
   stress --cpu 1 --timeout 120 # for 2 min





