# #####
# see also https://github.com/nginxinc/docker-nginx
# #####
FROM nginx:latest

RUN rm /etc/apt/sources.list
RUN echo "deb https://mirrors.aliyun.com/debian/ buster main non-free contrib" > /etc/apt/sources.list && \ 
	echo "deb https://mirrors.aliyun.com/debian-security buster/updates main" >> /etc/apt/sources.list && \
	echo "deb https://mirrors.aliyun.com/debian/ buster-updates main non-free contrib " >> /etc/apt/sources.list \
	&& apt-get update \
	&& apt-get install unzip net-tools iputils-ping vim -y \
	&& rm -rf /var/lib/apt/lists/*

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log

ENV NGINX_HOME=/etc/nginx

WORKDIR /etc/nginx/conf.d
RUN rm -f default.conf
COPY default default.conf

WORKDIR /usr/share/nginx/html
COPY dvm-fe.zip dvm-fe.zip
RUN rm -f index.html && unzip dvm-fe.zip  && rm -rf dvm-fe.zip

WORKDIR "$NGINX_HOME"
COPY start.sh "$NGINX_HOME"
RUN chmod +x start.sh
EXPOSE 80

CMD ["sh", "-c", "$NGINX_HOME/start.sh"]

