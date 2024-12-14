# Use the official Python 3 image from the Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any necessary packages specified in requirements.txt (if you have one)
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the script
CMD ["python", "Backend.py"]

