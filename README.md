# GRS Project

Project ID: 9

Title: Understanding Tail Latency in Kubernetes Microservices

Team Members:
- Harsha Verma (MT25024)
- Rajat Kumar Srivastava (MT25078)
- Anurag Sharma (MT25063)

## Tech Stack
- Kubernetes
- eBPF
- Python

## Files
9_PartA_trace_sched.py → CPU scheduling trace  
9_partA_trace_tcp.py → TCP retransmission trace  
9_partA_plot_latency.py → Tail latency plotting

## Reproducing the Experiments
This section describes how to reproduce the experiments on another Linux system. The experiments require:
- Linux (Ubuntu recommended)
- Python 3
- Docker
- Minikube
- Kubernetes CLI (kubectl)
- BCC (for eBPF tracing)
- wrk load testing tool

### Install Required Dependencies
- Update the system: ``` sudo apt update ```
- Install basic tools: ```sudo apt install git build-essential python3 python3-pip -y ```
- Install curl: ```sudo apt install curl -y```

### Install Docker
```sudo apt install docker.io -y```
- Start Docker:
``` sudo systemctl start docker sudo systemctl enable docker ```
- Add user to docker group: ``` sudo usermod -aG docker $USER ```
- Verify installation: ```docker --version ```

### Install Kubectl
``` sudo snap install kubectl --classic ```
- Verify: ``` kubectl version --client ```

### Install Minikube
- Download Minikube: ``` curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 ``` 
- Install: ``` sudo install minikube-linux-amd64 /usr/local/bin/minikube ```
- Verify: ``` minikube version ```

### Start Kubernetes Cluster
- Start Minikube using Docker driver: ``` minikube start --driver=docker ```
- Verify cluster: ``` kubectl get nodes ```
- Expected output: ``` minikube   Ready ```

### Deploy the Microservices
- Clone the project repository: ``` git clone https://github.com/theharshaverma/GRS_Project.git
  cd GRS_Project ```
- Deploy the NGINX microservice: ``` kubectl apply -f 9_nginx_deployment.yaml ```
- Verify deployment: ``` kubectl get pods ```
- Verify service: ``` kubectl get svc ```

### Get Service URL
- Run: ``` minikube service latency-nginx-service --url ```
- Example output: ``` http://192.168.49.2:30007 ```
This URL will be used for load testing.

### Install eBPF BCC Tools
- Install BCC and Python bindings: ``` sudo apt install bpfcc-tools python3-bpfcc linux-headers-$(uname -r) -y ```
- Verify installation: ``` python3 -c "from bcc import BPF; print('BCC installed successfully')" ```

### Run Kernel Tracing
- Open two terminals.
#### Terminal 1 – TCP Retransmission Tracer
``` sudo python3 9_trace_tcp.py ```
This reports TCP retransmissions every 10 seconds.
- Example output: ``` [10s summary] TCP retransmissions = 12 ```
#### Terminal 2 – Scheduler Delay Tracer
``` sudo python3 9_trace_sched.py ```
This measures wakeup-to-run scheduling delay.
- Example output: ``` [10s summary] wakeup->run events = 102000,
avg delay = 11 us,
max delay = 5000 us ```

### Install wrk Load Generator
- Install dependencies: ``` sudo apt install git build-essential libssl-dev -y ```
- Clone wrk: ``` git clone https://github.com/wg/wrk.git
cd wrk ```
- Build wrk: ``` make ```
- Install globally: ``` sudo cp wrk /usr/local/bin ```
- Verify: ``` wrk ```

### Run Baseline Experiment
- Start load generator: ``` wrk -t2 -c10 -d30s http://<service-url> ```
- Example: ``` wrk -t2 -c10 -d30s http://192.168.49.2:30007 ```
- Record: average latency, maximum latency and request rate. Also record tracer outputs from the two terminals.

### Run Medium Load Experiment
- Increase concurrency: ``` wrk -t4 -c100 -d30s http://<service-url> ```
- Record: latency metrics, TCP retransmissions and scheduler delay
