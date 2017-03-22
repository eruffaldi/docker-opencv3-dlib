#!/bin/bash
pushd .

mkdir ~/lib
mkdir ~/lib/cppnetlib
svn export https://github.com/cpp-netlib/cpp-netlib/branches/0.11-devel ~/lib/cppnetlib/sources
mkdir ~/lib/cppnetlib/build
cd ~/lib/cppnetlib/build
cmake ../sources
make -j
make install
popd
