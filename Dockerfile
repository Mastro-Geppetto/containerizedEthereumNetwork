FROM ubuntu:xenial

LABEL version="1.0"
LABEL maintainer="Promit.Chattterjee@gmail.com"

# NSN Specific
ENV HTTP_PROXY http://10.158.100.6:8080/
ENV HTTPS_PROXY https://10.158.100.6:8080/
  
ENV DEBIAN_FRONTEND noninteractive
# I have added optional iputils-ping net-tools, do not remove software-properties-common
RUN apt-get update && \
    apt-get --yes -qq upgrade && \
    apt-get --yes -qq install software-properties-common iputils-ping net-tools && \
    add-apt-repository ppa:ethereum/ethereum && \
    apt-get update && \
    apt-get --yes -qq install ethereum solc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /root

COPY ./common/genesis.json /root/.

RUN geth init /root/genesis.json

ENTRYPOINT bash
