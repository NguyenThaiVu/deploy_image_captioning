# Backend Deployment

## 1. Web Server Gateway Interface

Web Server Gateway Interface (WSGI) allow Python application to communicate with web server effectively:\
- **Flask built-in**: `flask run` is only meant for local testing and debugging. It’s not scalable or secure enough for production.
- **WSGI server**: such as gunicorn is optimized for handling web traffic in a production environment.

Why should we use WSGI in production:
- **Performance**: WSGI servers handle multiple requests concurrently, improving throughput.
- **Scalability**: WSGI servers support multiple workers to handle more simultaneous requests.

Example to run Flask App with Gunicorn:
```
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
- `-w 4`: number of worker (e.g. number of CPU cores)
- `-b 0.0.0.0:5000`: Binds the server to port 5000 and listens on all network interfaces
- `app:app`: refers to Flask application instance (the file name `app.py` and the Flask app object `app`).


## 2. Logging in Flask

We can use `logging` to understand what's happending in our application, debugging issues, and monitoring performance. Log Levels: 
- DEBUG: Detailed diagnostic information. <br/>
- INFO: General operational messages (e.g., a route was accessed). <br/>
- WARNING: Indicates a potential problem. <br/>
- ERROR: An error that may require attention.
- CRITICAL: A serious failure.

There are 2 main type of loggings, including **gunicorn log** and **flask log**. 
- **Gunicorn log**: monitor traffic and debug server issue.
- **Flask log**: Capture application-specifi events and information.

### 2.1. Store logs
The remained problem is that when your Flask application writes logs inside a Docker container, those logs are stored **inside the container’s filesystem.**

The potential solution is that using **Docker volumes** to map a directory inside the container to a directory on your host machine. 
When running the Docker container, map the container's `/app/logs` directory to your local machine's logs directory using the `-v` flag:
```
docker run -d -p 5000:5000 -v $(pwd)/logs:/app/logs flask-backend
```
- $(pwd)/logs: The absolute path on your host machine where logs will be stored.
- /app/logs: The path inside the container where the Flask app writes logs.


