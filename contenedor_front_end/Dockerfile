FROM python:3.8

RUN mkdir /dependencias

COPY requeriments.txt /dependencias

RUN pip3 install -r /dependencias/requeriments.txt

ENV SECRET_KEY=""
ENV DB_NAME=""
ENV DB_USER=""
ENV DB_PASSWORD="" 
ENV DB_HOST=""
ENV DB_PORT=3306

RUN mkdir /code
RUN mkdir /start

COPY ./run.sh /start
RUN chmod 751 /start/run.sh

WORKDIR /code

RUN useradd -s /bin/bash limitado

RUN chown -R limitado /code

CMD /start/run.sh
