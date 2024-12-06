FROM node:20-alpine
RUN apk add --no-cache tini curl
WORKDIR /app
COPY app.js .
EXPOSE 6060
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "app.js"]

