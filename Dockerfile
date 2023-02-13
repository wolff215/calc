# Use a Python image as the base
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the required packages
RUN pip install -r requirements.txt

# Copy the rest of the app code to the container
COPY . .

# Set the environment variables for the app
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Specify the command to run the app
CMD flask run --host=0.0.0.0