FROM pelarscompile
RUN mkdir /scripts2
ADD . /scripts2
WORKDIR /scripts2
#RUN ./make_zeromq.sh
#RUN apt-get install -yq libboost-all-dev
#RUN add-apt-repository ppa:boost-latest/ppa
#RUN apt-get update
#RUN apt-get install -yq libboost1X.58-all-dev
#RUN ./make_cppnetlib.sh
RUN ./make_websocketpp.sh
RUN ./make_aruco.sh


CMD ["bash"]
