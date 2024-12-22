import os

def create_flask_project(project_name):
    # Define folder structure
    folders = [
        project_name,
        f"{project_name}/app",
        f"{project_name}/templates",
        f"{project_name}/static",
    ]

    # Create folders
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    # Flask app boilerplate code
    flask_code = """from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask with Docker!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
"""

    # Dockerfile boilerplate code
    dockerfile_code = """# Base Image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install flask

# Run Flask app
CMD ["python", "app/app.py"]
"""

    # Create app.py file
    with open(f"{project_name}/app/app.py", "w") as f:
        f.write(flask_code)

    # Create Dockerfile
    with open(f"{project_name}/Dockerfile", "w") as f:
        f.write(dockerfile_code)

    print(f"🚀 Flask Project '{project_name}' Created Successfully!")

if __name__ == "__main__":
    project_name = input("Enter the project name: ")
    create_flask_project(project_name)
