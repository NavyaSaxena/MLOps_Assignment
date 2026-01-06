## 7. Production Deployment (Kubernetes on Docker Desktop)

This section explains how to deploy the Heart Disease API to **Kubernetes using Docker Desktop** and access it locally via **port‑forwarding**.

### Prerequisites

- Docker Desktop installed and running (with Kubernetes enabled)  
- `kubectl` configured to talk to the Docker Desktop Kubernetes cluster (usually automatic on Windows)  
- The Kubernetes manifests present in the repo:
  - `deployment.yaml`
  - `service.yaml`
- (If using a private Docker Hub image) Valid Docker Hub credentials

### 1. Enable Kubernetes in Docker Desktop

1. Open Docker Desktop.  
2. Go to **Settings → Kubernetes → Enable Kubernetes**, then click **Apply & Restart**.  
3. After restart, verify from a terminal:
   `kubectl get nodes`
You should see a node like docker-desktop.

### 2. Apply Deployment and Service
From where deployment.yaml and service.yaml exist:

1.  Create / update Deployment
`kubectl apply -f deployment.yaml`

2. Create / update Service
`kubectl apply -f service.yaml`
Check that resources are created and running:

3. Deployments
`kubectl get deployments`

4. Pods
`kubectl get pods`

5. Logs for a pod (replace with actual pod name)
`kubectl logs <POD_NAME>`
Wait until the pod status is Running and logs show that the API has started.

### 3. Access the API via Port‑Forwarding (recommended for Docker Desktop)
On Docker Desktop, NodePorts are sometimes awkward to reach, so the simplest way is port‑forwarding from your local machine to the pod.

1. Get the pod name:
`kubectl get pods`
Example: heart-disease-api-cff746c6-7xm78.

2. Forward local port 8080 to container port 5001 (the API port):
`kubectl port-forward pod/<POD_NAME> 8080:5001`
Keep this terminal open while you test.

3. Call the API locally:

Base URL: http://localhost:8080/

Example prediction request:

curl -X POST "http://localhost:8080/predict" ^
  -H "Content-Type: application/json" ^
  -d "{\"age\":55,\"sex\":1,\"cp\":0,\"trestbps\":140,\"chol\":220,
       \"fbs\":0,\"restecg\":0,\"thalach\":170,\"exang\":0,
       \"oldpeak\":0,\"slope\":2,\"ca\":0,\"thal\":3}"

5. (Alternative) Access via NodePort Service
If service.yaml is of type NodePort, you can also hit the service directly:
kubectl get svc heart-disease-service
Note the NODE-PORT (for example 30001).

On Docker Desktop, the node is usually reachable at localhost, so you can try:

`curl -X POST "http://localhost:<NODE-PORT>/predict" ...`
Use this only if NodePort routing works on your setup; otherwise prefer the port‑forward method above.
