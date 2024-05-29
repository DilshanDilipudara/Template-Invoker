ARG alpine

FROM alpine:$alpine

ARG go_version
ARG rdb_version
ARG java_version
ARG jre_version
ARG mvn_version
ARG python2_version
ARG python3_version
ARG default_python_version


ENV MAVEN_HOME /usr/lib/mvn
ENV PATH $MAVEN_HOME/bin:$PATH


RUN apk update && \ 
    apk upgrade && \
    apk add curl bash wget git net-tools tcpdump busybox-extras lsof sysstat procps make build-base

#go
RUN if [ -n "$go_version" ] ; then  \
        \
        apk add --no-cache --virtual .build-deps  gcc musl-dev openssl go  && \
		wget -O go.tgz https://dl.google.com/go/go$go_version.src.tar.gz && \
		tar -C /usr/local -xzf go.tgz && \
		cd /usr/local/go/src/ && \
		./make.bash && \
		export PATH="/usr/local/go/bin:$PATH" && \
		export GOPATH=/opt/go/ && \
		export PATH=$PATH:$GOPATH/bin && \
		apk del .build-deps && \
		cd / && \
		rm -rf go.tgz && \
		go version ; \
fi 

#Rocks DB
RUN if [ -n "$rdb_version" ] ; then  \
		\
		echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing" >>/etc/apk/repositories && \
        echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >>/etc/apk/repositories && \
        apk add --update --no-cache build-base linux-headers  cmake  zlib zlib-dev bzip2 bzip2-dev libcurl file tzdata\
                                snappy snappy-dev lz4 lz4-dev zstd@community zstd-dev@community \
                                libtbb-dev@community libtbb@community perl tar libc6-compat && \
		\
		wget -O - https://github.com/jemalloc/jemalloc/releases/download/5.2.1/jemalloc-5.2.1.tar.bz2 | tar -xj && \
        cd jemalloc-5.2.1 && \
        ./configure && \
        make && \
        make install && \
		\
 		cd /tmp && \
        git clone https://github.com/gflags/gflags.git && \
        cd gflags && \
        mkdir build && \
        cd build && \
        cmake -DBUILD_SHARED_LIBS=1 -DGFLAGS_INSTALL_SHARED_LIBS=1 .. && \
        make install && \
        cd /tmp && \
        rm -R /tmp/gflags && \
		\
		cd /tmp && \
        git clone https://github.com/facebook/rocksdb.git && \
        cd rocksdb && \
        git checkout tags/v$rdb_version -b v$rdb_version && \
        make DISABLE_WARNING_AS_ERROR=1  PORTABLE=1 shared_lib && \
        mkdir -p /usr/local/rocksdb/lib && \
        mkdir /usr/local/rocksdb/include && \
        cp librocksdb.so* /usr/local/rocksdb/lib && \
        cp /usr/local/rocksdb/lib/librocksdb.so* /usr/lib/ && \
        cp -r include /usr/local/rocksdb/ && \
        cp -r include/* /usr/include/ && \
        rm -rf /tmp/rocksdb/ && \
		cat /usr/include/rocksdb/version.h ; \
fi

#java 
RUN if [ -n "$java_version" ] ; then \
	\
	apk add  ca-certificates && \
	update-ca-certificates && \
	apk add --update coreutils && rm -rf /var/cache/apk/*  && \
	apk add --update $java_version tzdata unzip && \
	apk add --no-cache nss && \
	rm -rf /var/cache/apk/* && \
	java -version ; \
fi

#JRE 
RUN if [ -n "$jre_version" ] ; then \
	\
	apk add  ca-certificates && \
	update-ca-certificates && \
	apk add --update coreutils && rm -rf /var/cache/apk/*  && \
	apk add --update $jre_version tzdata unzip && \
	apk add --no-cache nss && \
	rm -rf /var/cache/apk/* && \
	java -version ; \
fi

#mvn
RUN if [ -n "$mvn_version" ] ; then \
	\
	wget http://archive.apache.org/dist/maven/maven-3/$mvn_version/binaries/apache-maven-$mvn_version-bin.tar.gz && \
	tar -zxvf apache-maven-$mvn_version-bin.tar.gz && \
	rm apache-maven-$mvn_version-bin.tar.gz && \
    mv apache-maven-$mvn_version /usr/lib/mvn && \
	mvn -v ; \
fi

#python2
RUN if [ -n "$python2_version" ] ; then \
	\
	echo -e "http://nl.alpinelinux.org/alpine/v3.5/main\nhttp://nl.alpinelinux.org/alpine/v3.5/community" > /etc/apk/repositories  && \
	\
	apk add --no-cache python2 && \
	python -V ; \
fi

#python3
RUN if [ -n "$python3_version" ] ; then \
        \
        echo -e "http://nl.alpinelinux.org/alpine/v3.5/main\nhttp://nl.alpinelinux.org/alpine/v3.5/community" > /etc/apk/repositories  && \
        \
        apk add --no-cache python3 py3-pip  && \
        python3 -V ; \
fi

#Update alternatives python2.7
RUN if [ $default_python_version = 'python2' ]; then \
        \
        update-alternatives --install /usr/bin/$default_python_version $default_python_version /usr/bin/python2.7 1 && \
        update-alternatives --config $default_python_version && \
        python -V ; \
fi

#Update alternatives python3
RUN if [ $default_python_version = 'python3' ]; then \
	\
	update-alternatives --install /usr/bin/$default_python_version $default_python_version /usr/bin/python3.5 1 && \
	update-alternatives --config $default_python_version && \
	python3 --version ; \
fi

#rdb
ENV LD_PRELOAD=/usr/local/lib/libjemalloc.so.2
#go
ENV PATH="/usr/local/go/bin:$PATH"
#time
ENV TZ=Asia/Colombo 
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
