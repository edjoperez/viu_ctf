# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

RUN useradd -ms /bin/bash -d /home/flaffy flaffy 
RUN apt-get update && apt-get install -y cron nano vim

# Set the working directory to /app
WORKDIR /home/flaffy/app


# Copy the current directory contents into the container at /app
COPY assets /home/flaffy/assets/
COPY scripts /home/flaffy/scripts/

RUN chmod +x /home/flaffy/scripts/cron.sh

# Option 1: Using RUN to add the crontab entry (updated path)````
RUN chown -R flaffy:flaffy /home/flaffy

USER flaffy
RUN (crontab -l 2>/dev/null; echo "*/1 * * * * /home/flaffy/scripts/cron.sh") | crontab -
CMD ["cron", "-f"] 
# USER root
# RUN service cron start


USER flaffy
COPY app /home/flaffy/app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable (Ensure this line is present)
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["python", "/home/flaffy/app/app.py"]