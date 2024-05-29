ARG nginx

FROM nginx:$nginx

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y build-essential git cmake pkg-config wget gcc vim  sysstat procps lsof
