FROM nginx:latest
RUN apt-get update && apt-get install --no-install-recommends -y bash nano mc

COPY build /shared/public_html/
COPY build/static /static

RUN rm /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]
