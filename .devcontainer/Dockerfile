# Use Python 3.11 as the base image
FROM python:3.11-buster

# Set the working directory in the container
WORKDIR /app

# Install Stockfish
RUN apt-get update && apt-get install -y stockfish

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the container
# COPY . .

# Set the entrypoint command to run your application
# CMD [ "python", "app.py" ]
