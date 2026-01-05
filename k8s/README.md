# Deploying Retail Creative Studio on Kubernetes

## Prerequisites
- **Kubernetes Cluster** (Minikube, Docker Desktop, or Cloud Provider).
- **kubectl** CLI installed.
- **Docker** installed (to build images).

## 1. Build Docker Images
First, build the images securely in your local environment so Kubernetes can find them.
```bash
docker build -t retail-backend:latest ./backend
docker build -t retail-frontend:latest ./frontend
```
*Note: If using Minikube, run `eval $(minikube docker-env)` before building so Minikube sees the images.*

## 2. Configure Secrets
Copy the template and add your real credentials. **Do not commit the real file.**
```bash
cp k8s/secrets-template.yaml k8s/secrets.yaml
```
Edit `k8s/secrets.yaml`:
- Set `mongo-url` to `mongodb://mongodb:27017` (Internal K8s DNS) or your external connection string.
- Add your `HUGGINGFACE_API_TOKEN` if required.

## 3. Deploy
Apply all manifests:
```bash
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/mongo.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml
```

## 4. Access
Check the status:
```bash
kubectl get pods
kubectl get services
```
- **Frontend**: Access via the External IP (LoadBalancer) or `localhost` (if Docker Desktop) on port 80.
- **Backend-to-DB**: The backend automatically finds MongoDB at `mongodb:27017`.

## 5. Cleaning Up
```bash
kubectl delete -f k8s/
```
