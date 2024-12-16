# Model Serving

Model serving is the process of hosting your trained machine learning models so they can provide predictions (inference).


# 1. Key Concepts 

## 1.1. Real-time vs Batch Serving

**Real-time**:
- Real-time serving is the process of serving model predictions in near-instant time (low-latency) for individual requests.
- Common use case: recommendation systems, chatbots,...
- Key Characteristics
    + Low Latency: expected in milliseconds.
    + Concurrency: handle multiple simultaneous requests.
    + Always On: service must available 24/7.
- Real-time serving technologies:
    + TorchServe: Scalable serving for PyTorch models.
    + Flask/FastAPI: Lightweight, Python-based frameworks for quick APIs.
- Challenge:
    + Scalability: Handling large volumes of requests.
    + Latency: Ensuring responses are fast.
    + Infrastructure: Requires always-on servers or cloud services.

**Batch Serving**:
- Processing large datasets at once, where the system processes multiple inputs, usually at scheduled intervals.
- Key Characteristics:
    + High Throughput: processing large datasets.
    + High Latency: Results can take minutes to compute.
    + Scheduled Execution: Often runs on a fixed schedule or triggered by events.
    + File-Based Inputs/Outputs: reads input from files (CSV, etc.) and writes outputs to files or databases.
- Common use case: 
    + Data Transformation: Preprocessing large datasets (e.g., ETL workflows).
    + Report Generation: Generating analytics for business reports.
- Batch Serving Technologies:
    + Apache Spark: Distributed computing for batch processing large datasets.
    + Dask: Python-based parallel processing for large dataframes.
    + AWS Batch / Google Dataflow: Cloud-based batch processing platforms.
- Challenges:
    + Latency: Not suitable for real-time use cases due to processing delays.
    + Resource: Requires significant resources for large datasets.


## 1.2. Model Serialization


## 1.3. RESTful and gRPC APIs
Common protocols for serving


# 2. Tools or Techniques for Model Serving

## 2.1. Scalability

Scalability ensures that your system can handle an increasing number of requests or workload sizes without degrading performance. It can be achieved by scaling:
- Vertically: Adding more resources (CPU, RAM) to a single instance.
- Horizontally: Adding more instances (replicas) of your service.

**Docker Swarm**: 
- Deploy your Flask app across multiple nodes using Docker Swarm.



**NGINX**:
- For load balancing: Use NGINX to distribute requests to multiple Gunicorn instances.


## 2.2. Low Latency

Convert your PyTorch model to ONNX format.



# 3. Monitoring

## 3.1. Key metrics

Latency 

Throughtput

Error Rate
