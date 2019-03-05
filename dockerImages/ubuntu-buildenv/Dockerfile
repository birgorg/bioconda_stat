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

RUN apt install -y \
    libhdf5-dev 

RUN apt install -y \
    libgoogle-glog-dev \
    libcppunit-dev 

RUN apt update && apt upgrade -y

RUN apt install -y \
    libgsl-dev

RUN apt install -y \
    git

RUN apt install -y \
    doxygen

RUN apt install -y \
    libfftw3-dev
