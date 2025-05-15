FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable for port (used by GCP)
ENV PORT=8080

# Run main.py when the container launches using uvicorn instead of gunicorn
CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT