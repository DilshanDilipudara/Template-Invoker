ARG ubuntu
FROM ubuntu:$ubuntu as builder

ARG osrm_version
ARG osrmc_version
ARG go_version
ARG rdb_version


ARG WORKDIR=/opt

ENV PATH=$PATH:/usr/local/go/bin
ENV GOPROXY=https://nexus.pickme.lk/repository/go-proxy/
ENV GO111MODULE=on

#install dependency
RUN apt-get update
RUN apt-get install -y build-essential git make cmake pkg-config wget gcc vim  sysstat procps lsof \
    libbz2-dev libxml2-dev libzip-dev libboost-all-dev \
    lua5.2 liblua5.2-dev libtbb-dev libgeos-dev liblwgeom-dev libproj-dev python3-pip \
	software-properties-common ca-certificates gpg curl doxygen libjson-c-dev libtbb2 libexpat1 libexpat1-dev \
	libbz2-dev lua5.2 liblua5.2-dev


#osrm
RUN if [ -n "$osrm_version" ] ; then \
	\
	cd ${WORKDIR} && \
	git clone https://github.com/Project-OSRM/osrm-backend.git  && \
	cd osrm-backend && \
	git checkout tags/v$osrm_version -b v$osrm_version && \
	mkdir -p build && \
	cd build &&  \
	cmake .. && \
	cmake --build . && \
	cmake --build . --target install; \
fi



#go
RUN if [ -n "$go_version" ] ; then \
	\
	wget -O go.tgz https://golang.org/dl/go$go_version.linux-amd64.tar.gz && \
	tar -C /usr/local -xzf go.tgz && \
	cd /usr/local/go/src/ && \
	export PATH="/usr/local/go/bin:$PATH" && \
	export GOPATH=/opt/go/ && \
	export PATH=$PATH:$GOPATH/bin && \
	cd / && \
	rm -rf go.tgz && \
	go version ; \	
fi
	
#Rokcs DB
RUN if [ -n "$rdb_version" ] ; then \
	\
	cd /tmp && \
        git clone https://github.com/facebook/rocksdb.git && \
        cd rocksdb && \
        git checkout tags/v$rdb_version -b v$rdb_version && \
        make DISABLE_WARNING_AS_ERROR=1 PORTABLE=1 shared_lib && \
        make DISABLE_WARNING_AS_ERROR=1 shared_lib && \
        mkdir -p /usr/local/rocksdb/lib && \
        mkdir /usr/local/rocksdb/include && \
        cp librocksdb.so* /usr/local/rocksdb/lib && \
        cp /usr/local/rocksdb/lib/librocksdb.so* /usr/lib/ && \
        cp -r include /usr/local/rocksdb/ && \
        cp -r include/* /usr/include/ && \
        rm -R /tmp/rocksdb/ ; \
fi


#go
ENV PATH="/usr/local/go/bin:$PATH"
ENV TZ=Asia/Colombo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
