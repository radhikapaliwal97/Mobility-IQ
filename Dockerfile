# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the app code
COPY ./app /app
COPY ./tests /app/tests

# Expose the port
EXPOSE 80

# Start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload", "--port", "80"]