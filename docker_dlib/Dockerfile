FROM ???
#TODO specify FROM above
#TODO python setup calling make in parallel

# Install DLIB master
RUN apt-get -y install libboost-python-dev
WORKDIR /tmp
RUN wget https://codeload.github.com/davisking/dlib/zip/master -O dlib.zip && \
    unzip -q dlib.zip && mv dlib-master dlib
WORKDIR /tmp/dlib
ENV CFLAGS -march=native -O3 -flto 
ENV CXXFLAGS -march=native -O3 -flto
RUN python setup.py --yes USE_AVX_INSTRUCTION --yes USE_SSE4_INSTRUCTIONS --yes USE_SSE2_INSTRUCTIONS=ON --yes NDEBUG --yes DLIB_HAVE_SSE41 --yes DLIB_HAVE_SSE3 --yes DLIB_HAVE_SSE2 --yes DLIB_USE_BLAS --yes DLIB_USE_LAPACK build
RUN python setup.py install 