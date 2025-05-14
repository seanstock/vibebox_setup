# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install Flask openai

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
# Set OPENAI_API_KEY to empty by default - will be overridden by docker-compose
ENV OPENAI_API_KEY=""

# Run app.py when the container launches
CMD ["flask", "run"]
