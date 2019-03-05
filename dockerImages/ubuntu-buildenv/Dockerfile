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

RUN apt install -y \
    wget

RUN wget http://lemon.cs.elte.hu/pub/sources/lemon-1.3.tar.gz && tar xvzf lemon-1.3.tar.gz && cd lemon-1.3 && cmake -DCMAKE_INSTALL_PREFIX=~/lemon && make install && cd .. && rm -rf lemon-1.3

WORKDIR /package

RUN apt install -y \
    libeigen3-dev \
    libhts-dev
