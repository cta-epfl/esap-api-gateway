FROM nginx:latest

COPY build /shared/public_html/
COPY build/static /static

RUN rm /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]