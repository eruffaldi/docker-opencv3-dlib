#!/bin/bash
pushd .
mkdir ~/lib
mkdir ~/lib/websocketpp
svn export https://github.com/zaphoyd/websocketpp/trunk ~/lib/websocketpp/sources
mkdir ~/lib/websocketpp/build
cd ~/lib/websocketpp/build
cmake ../sources
make -j4
make install
popd
