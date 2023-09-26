# Use an official Python runtime as a parent image. 
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Download Package Information for system-level packages
RUN apt-get update -y

RUN pip install --upgrade pip -y \
    && apt-get update \
    && apt-get install -y git x11vnc

# Install the Tkinter package
RUN apt-get install tk -y

#Set envirnmental variable for display	
ENV DISPLAY :20

# Copy the Requirements.txt file from the directory and copy to the image
COPY requirements.txt ./

# Install any specified dependencies for Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

#Expose port 5920 to view display using VNC Viewer
EXPOSE 5920

# Specify the command to run on container start
CMD ["python", "./main.py"]


