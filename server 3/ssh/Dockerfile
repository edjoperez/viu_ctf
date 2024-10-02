FROM ubuntu:latest

# Install SSH server, vim, and sudo
RUN apt-get update && \
    apt-get install -y --no-install-recommends openssh-server vim sudo && \
    rm -rf /var/lib/apt/lists/*

# Create SSH directory and configure SSH
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

# Expose SSH port
EXPOSE 2222

# Start SSH service
CMD ["/usr/sbin/sshd", "-D"]