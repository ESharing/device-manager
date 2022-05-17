# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

RUN rm /etc/apt/sources.list
RUN echo "deb https://mirrors.aliyun.com/debian/ buster main non-free contrib" > /etc/apt/sources.list && \
        echo "deb https://mirrors.aliyun.com/debian-security buster/updates main" >> /etc/apt/sources.list && \
        echo "deb https://mirrors.aliyun.com/debian/ buster-updates main non-free contrib " >> /etc/apt/sources.list \
        && apt-get update \
        && apt-get install unzip net-tools iputils-ping vim -y \
        && rm -rf /var/lib/apt/lists/*

RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip3 config set install.trusted-host mirrors.aliyun.com

WORKDIR /app

COPY py_pkg py_pkg

RUN pip3 install -r py_pkg

COPY netconf_server.zip netconf_server.zip 

RUN unzip netconf_server.zip && rm -rf netconf_server.zip

EXPOSE 8081

CMD [ "python3", "app.py"]
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
