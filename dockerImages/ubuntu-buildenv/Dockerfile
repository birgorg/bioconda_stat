FROM ubuntu

ENV TZ=Europe/Minsk
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && apt upgrade -y

RUN apt install -y \
    cmake \
    build-essential \
    zlib1g-dev \
    libbz2-dev \
    python \
    python-sphinx \
    libboost-all-dev
    


WORKDIR /package
