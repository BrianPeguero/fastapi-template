FROM nginx

COPY nginx.conf etc/nginc/conf.d/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]