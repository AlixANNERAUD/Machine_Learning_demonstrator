# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/

# Install dependencies (cached)
RUN --mount=type=cache,target=/root/.cache \
pip install --upgrade pip

RUN --mount=type=cache,target=/root/.cache \
pip3 install torch==2.5.1+cpu torchaudio==2.5.1+cpu --index-url https://download.pytorch.org/whl/cpu

RUN --mount=type=cache,target=/root/.cache \
pip install -r requirements.txt 

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copy the project
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]