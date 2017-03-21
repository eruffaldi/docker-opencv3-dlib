FROM docker-opencv2-dlib:cuda

#https://github.com/shadow-robot/ramcip/blob/master/deployment/ansible/roles/libfreenect2-installer/tasks/install.yml
#TODO glfw
#help RUN DEBIAN_FRONTEND=noninteractive add-apt-repository ppa:chris-lea/node.js

RUN apt-get install libusb-1.0 libturbojpeg libjpeg-turbo8-dev libtinyxml2-dev libportaudio-dev
RUN apt-get install libcurl-dev libcurlpp-dev
RUN apt-get install libeigen3-dev
RUN apt-get install lame 
RUN apt-get install libcairo-dev
RUN apt-get install libjsoncpp-dev
RUN apt-get install libx11-dev libxrandr-dev libxinerama-dev libxcursor-dev  libxi-dev mesa-common-dev  subversion

RUN ./make_glfw.sh
RUN ./make_libfreenect2.sh
#RUN ./make_zeromq.sh
RUN ./make_cppnetlib.sh
RUN ./make_websocketpp.sh


