# Use an official Python runtime as a parent image. 
FROM python:3.9-slim



# Download Package Information for system-level packages
# RUN apt-get update -y

# Install VNC server and other necessary packages
RUN apt-get update && apt-get install -y x11vnc xvfb

# Set up VNC Password
RUN mkdir ~/.vnc
RUN x11vnc -storepasswd yourpassword ~/.vnc/passwd

# upgrade pip as necesssary
# RUN pip install --upgrade pip

#Install the x11vnc package
# RUN apt-get install -y git x11vnc
# Install the Tkinter package
RUN apt-get install tk -y

# Set the working directory in the container
WORKDIR /app

#Set envirnmental variable for display	
# ENV DISPLAY :20

# Copy the Requirements.txt file from the directory and copy to the image
COPY requirements.txt ./

# Install any specified dependencies for Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Specify the command to run on container start
# Command to run the VNC server
# CMD ["x11vnc", "-forever", "-usepw", "-create"]
# CMD ["python", "./main.py"]

# Make the start script executable
RUN chmod +x start.sh

# Expose VNC port
EXPOSE 5900

# Command to run the start script
CMD ["./start.sh"]

