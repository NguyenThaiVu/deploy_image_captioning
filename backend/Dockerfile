# Use the official Python image as a base
FROM python:3.10-slim

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

# Expose the port your app runs on
EXPOSE 5000

# Maps port 5000 on your local machine to port 5000 in the container.
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
