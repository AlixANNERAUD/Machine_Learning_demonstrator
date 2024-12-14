# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

ENV PYSETUP_PATH="/opt/pysetup"
ENV VENV_PATH="/opt/pysetup/.venv"

# Set the working directory
WORKDIR /app

# Install pipx
RUN apt-get update && apt-get install pipx -y

# Install Poetry
RUN pipx install poetry

# Set the path for the poetry binary
ENV PATH="/root/.local/bin:$PATH"

# Copy the dependencies file to the working directory
COPY pyproject.toml /app/

# Install the dependencies
RUN poetry install

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copy the project
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Run the Django development server
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]