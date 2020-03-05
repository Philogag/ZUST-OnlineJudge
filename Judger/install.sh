#!/bin/sh

sudo apt-get update
sudo apt-get install -y cmake python3 
sudo apt-get install -y openjdk-8-jdk
sudo apt-get install -y libseccomp-dev



cd ./SandBox
mkdir build 
cd build && cmake .. && make && sudo make install
