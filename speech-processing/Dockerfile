# Use an official Python runtime as a parent image
FROM python:3.11-slim
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

RUN apt-get update && apt-get install git ffmpeg -y
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Set the environment variables in Docker
ENV MODEL_NAME=$MODEL_NAME
ENV MODEL_PATH=$MODEL_PATH
ENV PORT=$PORT
ENV ENVIRONMENT=$ENVIRONMENT
ENV GUNICORN_BIND=$GUNICORN_BIND
ENV GUNICORN_TIMEOUT=$GUNICORN_TIMEOUT
ENV GUNICORN_THREADS=$GUNICORN_THREADS

# Expose the port that the FastAPI app runs on
EXPOSE $PORT

# Run the FastAPI app using Gunicorn
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "$GUNICORN_BIND", "--timeout", "$GUNICORN_TIMEOUT", "--threads", "$GUNICORN_THREADS"]
