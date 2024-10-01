# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Create the 'flaffy' user
RUN useradd -ms /bin/bash -d /home/flaffy flaffy 

# Install necessary packages including cron and supervisord
RUN apt-get update && apt-get install -y cron nano vim supervisor ssh inetutils-ping

# Set the working directory to /app
WORKDIR /home/flaffy/app

# Copy assets and scripts
COPY assets /home/flaffy/assets/
COPY scripts /home/flaffy/scripts/

# Give execute permissions to the cron script
RUN chmod +x /home/flaffy/scripts/cron.sh

# Option 1: Using RUN to add the crontab entry (updated path)````
RUN chown -R flaffy:flaffy /home/flaffy
# Add 'flaffy' to the sudo group
RUN usermod -aG sudo flaffy

# Switch to the 'flaffy' user to set up the crontab
USER flaffy
RUN (crontab -l 2>/dev/null; echo "*/1 * * * * /home/flaffy/scripts/cron.sh >> /home/flaffy/cron.log 2>&1") | crontab -

# Switch back to root to copy the app files and supervisord config
USER root

# Copy the application code
COPY app /home/flaffy/app/

# Copy supervisord configuration file
COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Make port 5000 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV FLASK_APP=app.py
USER root
# Start supervisord to manage both cron and the Flask app
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]