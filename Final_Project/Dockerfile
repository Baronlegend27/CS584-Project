# Use an official Python runtime as a parent image
FROM continuumio/miniconda3

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Create a conda environment and install any needed packages specified in requirements.yaml
RUN conda env create -f requirements.yaml

# Make port 80 available to the world outside this container
EXPOSE 80

# Run Start.py when the container launches
CMD ["python", "Start.py"]
