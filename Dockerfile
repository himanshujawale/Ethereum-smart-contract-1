FROM ubuntu:latest
RUN apt-get -y update
RUN apt-get install openjdk-8-jdk
RUN apt-get install -y \
    wget \
    unzip
	
RUN mkdir kafka

WORKDIR /kafka
RUN wget https://dlcdn.apache.org/kafka/3.0.0/kafka-3.0.0-src.tgz

RUN tar zxvf kafka-3.0.0-src.tgz

RUN rm kafka-3.0.0-src.tgz
