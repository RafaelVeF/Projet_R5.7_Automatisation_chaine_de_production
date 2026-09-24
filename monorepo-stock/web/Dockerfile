FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

WORKDIR /usr/share/nginx/html

RUN mkdir -p /usr/share/nginx/html && \
    echo '<!doctype html><html><head><title>Monorepo Stock</title></head><body><h1>Monorepo Stock</h1><p>Interface web prête.</p></body></html>' > /usr/share/nginx/html/index.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
