FROM nginx

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY ./build/html /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]