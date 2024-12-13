# Use the NVIDIA CUDA base image with Ubuntu 22.04 and CUDA 12.1
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

# Set the working directory in the container
WORKDIR /app

# Install Python and other necessary dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Make the scripts executable
RUN chmod +x /app/script1.sh /app/script2.sh

# Create a start script that runs the other scripts and the Flask app
RUN echo "#!/bin/sh\n./script1.sh &\n./script2.sh &\npython3 app.py" > /app/start.sh
RUN chmod +x /app/start.sh

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Define environment variable with modern key=value format
ENV NAME=World

# Run the start script
CMD ["./start.sh"]
