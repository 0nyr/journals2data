FROM ubuntu:20.04
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

# Add source directory
COPY src/journals2data journals2data/src/journals2data
COPY logs journals2data/logs
COPY out journals2data/out

# Install Conda
RUN apt-get update
RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*
RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh

# Install Firefox and Geckodriver
RUN apt-get update
RUN apt-get install -y firefox

COPY cmd/install_gecko_docker.sh journals2data/cmd/install_gecko_docker.sh
RUN bash journals2data/cmd/install_gecko_docker.sh

# Setup Conda environment
RUN conda env create -f journals2data/src/journals2data/docker_conda_config.yml
SHELL ["conda", "run", "-n", "j2d", "/bin/bash", "-c"]

# Python Script
COPY src/scripts/docker_run.py journals2data/src/docker_run.py
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "j2d", "python", "/journals2data/src/docker_run.py"]
