#!/bin/bash
pushd .
mkdir ~/lib
mkdir ~/lib/k2
svn export https://github.com/OpenKinect/libfreenect2/trunk ~/lib/k2/sources
pushd ~/lib/k2/sources
cd depends
./download_debs_trusty.sh

apt-get install -yq build-essential cmake pkg-config 
apt-get install -yq opencl-header
dpkg -i debs/libusb*deb
apt-get install -yqf
apt-get install -yq libturbojpeg libjpeg-turbo8-dev
#dpkg -i debs/libglfw3*deb; apt-get install -f; sudo apt-get install libgl1-mesa-dri-lts-vivid
apt-add-repository ppa:floe/beignet; 
apt-get update; 
apt-get install -y beignet-dev; 
dpkg -i debs/ocl-*deb
#dpkg -i debs/{libva,i965}*deb; 
apt-get install -f

popd
mkdir ~/lib/k2/build
cd ~/lib/k2/build
cmake ../sources -DCMAKE_INSTALL_PREFIX="~/lib/k2" -DENABLE_CXX11=ON -DENABLE_CUDA=OFF
make -j
make install
cd ~/lib/k2/sources
cp ./platform/linux/udev/90-kinect2.rules /etc/udev/rules.d/
popd
