FROM nginx

COPY nginx.conf etc/nginc/conf.d/nginx.conf

CMD ["-g", "daemon", "off"]