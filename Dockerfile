# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir anthropic

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Run family_feud_game.py when the container launches
CMD ["python", "family_feud_game.py"]
