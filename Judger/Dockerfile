FROM ubuntu

MAINTAINER philogag

# RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && apt-get clean
RUN apt-get update --fix-missing
RUN apt-get install -y cmake python3 python3-pip openjdk-8-jdk && \
    apt-get install -y libseccomp-dev && \
    apt-get clean
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
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

