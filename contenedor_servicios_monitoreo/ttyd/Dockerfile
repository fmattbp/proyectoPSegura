FROM tsl0922/ttyd

RUN apt-get -y update \
    && apt-get install -y openssh-client \
    && apt-get install -y openssl \
    && apt-get -y clean
ENV CN="patito.loco"
RUN openssl genrsa -out ca.key 2048
RUN openssl req -new -x509 -days 365 -key ca.key -subj "/C=CN/ST=VER/L=XAL/O=FEI/CN=$CN" -out ca.crt

EXPOSE 7681

ENV USER=""
ENV PASS=""

COPY ./run.sh /
RUN chmod 700 /run.sh
RUN chmod 400 /ca.key
RUN chmod 400 /ca.crt
RUN useradd -s /bin/bash limitado
RUN chown limitado ca.*
CMD /run.sh
