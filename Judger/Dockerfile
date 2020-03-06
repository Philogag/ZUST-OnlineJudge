FROM ubuntu

MAINTAINER philogag

RUN apt-get update
RUN apt-get install -y cmake python3 python3-pip openjdk-8-jdk && \
    apt-get install -y libseccomp-dev && \
    apt-get clean && \
    mkdir /Judger

WORKDIR /Judger

COPY ./lib ./lib
COPY ./SandBox ./SandBox 
COPY ./conf.json ./main.py ./requirements.txt /Judger/

RUN pip3 install -r requirements.txt

RUN cd /Judger/SandBox && \
    mkdir build && \
    cd build && \
    cmake .. && make && \
    make install && \
    cd /Judger/SandBox && \
    python3 setup.py install

CMD ["python3", "/Judger/main.py"]

