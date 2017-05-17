#!/usr/bin/env bash
GCCVERSION=4.9
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get install -yq g++-$GCCVERSION
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-$GCCVERSION 50
update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-$GCCVERSION 50
