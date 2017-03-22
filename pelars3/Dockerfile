FROM pelarscompile2

RUN apt-get build-dep --yes libboost-dev
ADD http://downloads.sourceforge.net/project/boost/boost/1.58.0/boost_1_58_0.tar.gz?r=http%3A%2F%2Fwww.boost.org%2Fusers%2Fhistory%2Fversion_1_58_0.html&ts=1433603736&use_mirror=vorboss /tmp/boost_1_58_0.tar.gz
RUN cd /tmp \
 && tar -xf boost_1_58_0.tar.gz \
 && cd ./boost_1_58_0 \
 && ./bootstrap.sh --with-libraries=filesystem,program_options,system,serialization,thread,date_time --exec-prefix=/usr/local \
 && ./b2 -j 20 \
 && ./b2 install

RUN apt-get install -qy libmp3lame-dev libqrencode-dev
