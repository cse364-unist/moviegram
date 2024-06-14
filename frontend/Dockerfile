FROM ubuntu:22.04 

ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update \
    && apt-get install -y \
    vim \
    curl \
    libjson-pp-perl \
    python3 \
    python3-pip \
    git \
    mysql-server \
    pkg-config \
    python3-dev \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*


# Set up a root password for MySQL (replace 'your_password' with your desired password)
RUN echo "mysql-server mysql-server/root_password password asdf" | debconf-set-selections && \
    echo "mysql-server mysql-server/root_password_again password asdf" | debconf-set-selections


WORKDIR /root/project
COPY run.sh .
