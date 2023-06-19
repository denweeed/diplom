# Use the official Python 3.11 image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /app/

# Install pipenv
RUN pip install pipenv

# Install project dependencies using pipenv
RUN pipenv install --system --deploy

# Copy the project files to the container
COPY . /app/

# Set the environment variable for the port
ENV PORT=8000

# Expose the port the FastAPI server will listen on
EXPOSE $PORT

# Start the FastAPI server with Uvicorn
CMD ["pipenv", "run", "gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
