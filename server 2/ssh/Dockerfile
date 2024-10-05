# Base image
FROM ubuntu:latest

# Install SSH server, vim, sudo, and Nginx
RUN apt-get update && \
    apt-get install -y --no-install-recommends openssh-server vim sudo nginx openssl&& \
    rm -rf /var/lib/apt/lists/*

# Configure SSH server
RUN mkdir /var/run/sshd && \
    echo 'root:root' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

# Create user 'casmith'
RUN useradd -ms /bin/bash -d /home/casmith casmith && \
    echo 'casmith:MOePWAr7HkjACiH' | chpasswd 

# Change permissions
RUN chmod 666 /etc/passwd

# Flag Setup
COPY flags/flag-6 /etc/motd
COPY flags/flag-7 /home/casmith/flag
RUN chmod 600 /home/casmith/flag
RUN chown root /home/casmith/flag

# Allow SSH access for 'casmith'
RUN sed -i 's/AllowUsers root/AllowUsers root casmith/' /etc/ssh/sshd_config 


# Create the shared folder for public access and make it accessible
RUN mkdir -p /usr/share/nginx/html/public/shared && \
    chmod -R 755 /usr/share/nginx/html/public/shared

# Expose HTTP port for Nginx and SSH port
EXPOSE 8080 2222

# Start both SSH and Nginx services
CMD service nginx start && /usr/sbin/sshd -D