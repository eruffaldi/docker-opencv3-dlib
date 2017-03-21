#!/bin/bash
pushd .
mkdir ~/lib
mkdir ~/lib/glfw
svn export https://github.com/glfw/glfw/trunk ~/lib/glfw/sources
mkdir ~/lib/glfw/build
cd ~/lib/glfw/build
cmake ../sources -DBUILD_SHARED_LIBS=TRUE
make -j4
make install
popd
