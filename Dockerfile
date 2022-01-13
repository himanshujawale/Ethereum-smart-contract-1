FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive

# Space-separated version string without leading 'v' (e.g. "0.4.21 0.4.22") 
ARG SOLC

RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y python3 \
   python3-pip \
   python3-setuptools \
   wget \
   unzip \
   software-properties-common \
 && ln -s /usr/bin/python3 /usr/local/bin/python

RUN wget https://github.com/Microservices-delixus/Ethereum-smart-contract/archive/main.zip

RUN  unzip main.zip 
RUN  mv Ethereum-smart-contract-main/ main 
RUN  mv main/ /home

RUN add-apt-repository ppa:ethereum/ethereum \
 && apt-get update \
 && apt-get install -y solc
  
WORKDIR /home/main/

RUN pip3 install -r requirements.txt

RUN pip3 install slither-analyzer

RUN mkdir ../workdir
RUN mv slither_analysis.sh mythril_analysis.sh solidity_files/ ../workdir

WORKDIR /home/workdir 

RUN chmod -R a+rwx slither_analysis.sh mythril_analysis.sh

RUN ./slither_analysis.sh

CMD /bin/bash






