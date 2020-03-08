FROM ubuntu

MAINTAINER philogag

RUN apt-get update
RUN apt-get install -y cmake python3 python3-pip openjdk-8-jdk && \
    apt-get install -y libseccomp-dev && \
    apt-get clean && \
    mkdir /Judger && \
    useradd -u 12001 compiler && useradd -u 12002 code && useradd -u 12003 spj && usermod -a -G code spj

WORKDIR /Judger

COPY . ./

RUN pip3 install -r requirements.txt

RUN cp /Judger/sandbox/java_policy /etc/java_policy && \
    cd /Judger/sandbox && \
    cd build && \
    cmake .. && make && \
    make install && \
    cd /Judger/sandbox/Python && \
    python3 setup.py install

CMD ["python3", "/Judger/main.py"]

