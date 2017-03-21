#!/bin/bash
pushd .
mkdir ~/lib
mkdir ~/lib/k2
svn export https://github.com/OpenKinect/libfreenect2/trunk ~/lib/k2/sources
mkdir ~/lib/k2/build
cd ~/lib/k2/build
cmake ../sources -DCMAKE_INSTALL_PREFIX="~/lib/k2" -DENABLE_CXX11=ON
make -j4
make install
cd ~/lib/k2/sources
cp ./platform/linux/udev/90-kinect2.rules /etc/udev/rules.d/
popd
