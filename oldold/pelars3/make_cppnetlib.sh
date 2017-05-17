#!/bin/bash
pushd .

mkdir ~/lib
mkdir ~/lib/cppnetlib
#svn export https://github.com/cpp-netlib/cpp-netlib/branches/0.11-devel ~/lib/cppnetlib/sources
cd ~/lib/cppnetlib
wget "http://downloads.cpp-netlib.org/0.12.0/cpp-netlib-0.12.0-final.tar.gz" -O cpp-netlib.tar.gz
tar zxf cpp-netlib.tar.gz
mv cpp-netlib-0.12.0-final sources
mkdir ~/lib/cppnetlib/build
cd ~/lib/cppnetlib/build
cmake -DCPP-NETLIB_BUILD_TESTS=OFF -DCPP-NETLIB_BUILD_EXPERIMENTS=OFF -DCPP-NETLIB_BUILD_EXAMPLES=OFF -DCPP-NETLIB_BUILD_SHARED_LIBS=ON ../sources
make -j
make install
popd
