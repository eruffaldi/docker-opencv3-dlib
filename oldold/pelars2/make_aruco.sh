#!/bin/bash
pushd .
mkdir ~/lib
mkdir ~/lib/aruco
wget "https://osdn.net/frs/g_redir.php?m=netix&f=%2Faruco%2F1.2.4%2Faruco-1.2.4.tgz" -O aruco.tgz
tar zxf aruco.tgz
mv aruco-1.2.4 ~/lib/aruco/sources
mkdir ~/lib/aruco/build
cd ~/lib/aruco/build
cmake OpenCV_STATIC=ON BUILD_GLSAMPLES=OFF BUILD_SHARED_LIBS=ON BUILD_UTILS=OFF CMAKE_BUILD_TYPE=Release ../sources
make -j
make install
popd
