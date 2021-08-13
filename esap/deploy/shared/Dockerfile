FROM nginx:latest
RUN apt-get update && apt-get install --no-install-recommends -y bash nano mc
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/