# Use the official Python 3.9 image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /app/

# Install pipenv
RUN pip install pipenv

# Install project dependencies using pipenv
RUN pipenv install --system --deploy

# Copy the project files to the container
COPY main.py /app/main.py
COPY docker-compose.yml /app/docker-compose.yml
COPY Pipfile.lock /app/Pipfile.lock
COPY README.md /app/README.md
COPY src /app/src
COPY test /app/test

# Set the environment variable for the port
ENV PORT=8000

# Expose the port the FastAPI server will listen on
EXPOSE $PORT

# Start the FastAPI server with Uvicorn
CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
