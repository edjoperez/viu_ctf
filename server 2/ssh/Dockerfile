# Base image
FROM ubuntu:latest

# Install SSH server, vim, sudo, and Nginx
RUN apt-get update && \
    apt-get install -y --no-install-recommends openssh-server vim sudo nginx && \
    rm -rf /var/lib/apt/lists/*

# Configure SSH server
RUN mkdir /var/run/sshd && \
    echo 'root:root' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

# Create user 'casmith'
RUN useradd -ms /bin/bash -d /home/casmith casmith && \
    echo 'casmith:MOePWAr7HkjACiH' | chpasswd 

# Add casmith to the sudoers group
RUN usermod -aG sudo casmith

# Allow casmith to execute vim without password
RUN echo "casmith ALL=(ALL) NOPASSWD: /usr/bin/vim" >> /etc/sudoers

# Allow SSH access for 'casmith'
RUN sed -i 's/AllowUsers root/AllowUsers root casmith/' /etc/ssh/sshd_config 

# Nginx configuration
COPY ../config/nginx.conf /etc/nginx/nginx.conf

# Create the shared folder for public access and make it accessible
RUN mkdir -p /usr/share/nginx/html/public/shared && \
    chmod -R 755 /usr/share/nginx/html/public/shared

# Expose HTTP port for Nginx and SSH port
EXPOSE 8080 2222

# Start both SSH and Nginx services
CMD service nginx start && /usr/sbin/sshd -D