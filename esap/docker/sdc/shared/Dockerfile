FROM nginx
RUN apt-get update && apt-get install --no-install-recommends -y bash nano mc
RUN rm /etc/nginx/conf.d/default.conf
COPY esap_nginx.conf /etc/nginx/conf.d/
 
# put Dockerfile, esap_nginx.conf and oidc in your $HOME/shared directory
# where the docker-compose.yml can find it.
