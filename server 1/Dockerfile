# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Create the 'flaffy' user
RUN useradd -ms /bin/bash -d /home/flaffy flaffy 

# Install necessary packages including cron and supervisord
RUN apt-get update && apt-get install -y cron nano vim supervisor ssh inetutils-ping sudo

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
# USER flaffy
RUN ln -s /home/flaffy/scripts/cron.sh  /usr/local/bin/update-stats
RUN echo '*/1 * * * * root /usr/local/bin/update-stats >> /var/log/my_script.log 2>&1' > /etc/cron.d/update_stats_job
RUN chmod 0644 /etc/cron.d/update_stats_job

# Copy the application code
COPY app /home/flaffy/app/

# Copy supervisord configuration file
COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Make port 5000 available to the world outside this container
EXPOSE 80

RUN update-stats
# Define environment variable
ENV FLASK_APP=app.py
USER root

# Flag Setup
COPY flags/flag-3 /home/flaffy/app/
RUN chmod 600 /home/flaffy/app/flag-3
RUN chown flaffy /home/flaffy/app/flag-3

COPY flags/flag-4 /home/flaffy
RUN chmod 600 /home/flaffy/flag-4
RUN chown root /home/flaffy/flag-4

# Start supervisord to manage both cron and the Flask app
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]