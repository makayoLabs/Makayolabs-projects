import os
import subprocess

# Define the project directory
project_dir = "media_toolkit"

# Define the media_toolkit.py content
media_toolkit_code = """
import os
import ffmpeg
import speech_recognition as sr
import cv2

# Media Toolkit functionalities go here...
# For brevity, only a placeholder function is shown

def main():
    print("Welcome to the Media Toolkit!")
    # Add your interactive media processing logic here

if __name__ == "__main__":
    main()
"""

# Define the Dockerfile content
dockerfile_content = """
# Use a base image with Python installed
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the necessary Python libraries
RUN pip install --no-cache-dir ffmpeg-python SpeechRecognition opencv-python google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Command to run the application
CMD ["python", "media_toolkit.py"]
"""

# Create the project directory
if not os.path.exists(project_dir):
    os.makedirs(project_dir)

# Write the media_toolkit.py file
with open(os.path.join(project_dir, "media_toolkit.py"), "w") as f:
    f.write(media_toolkit_code)

# Write the Dockerfile
with open(os.path.join(project_dir, "Dockerfile"), "w") as f:
    f.write(dockerfile_content)

# Change the working directory to the project directory
os.chdir(project_dir)

# Build the Docker image
subprocess.run(["docker", "build", "-t", "media_toolkit", "."])

# Run the Docker container
subprocess.run(["docker", "run", "-it", "--rm", "media_toolkit"])
