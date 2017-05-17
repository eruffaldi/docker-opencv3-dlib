#!/bin/bash
pushd .
mkdir ~/lib
mkdir ~/lib/cppnetlib
svn export https://github.com/cpp-netlib/cpp-netlib/trunk ~/lib/cppnetlib/sources
mkdir ~/lib/cppnetlib/build
cd ~/lib/cppnetlib/build
cmake ../sources
make -j
make install
popd
