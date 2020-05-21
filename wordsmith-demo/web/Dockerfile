# MULTI-STAGE BUILD
FROM golang:1.14.2-alpine3.11 AS build

WORKDIR /demo
COPY dispatcher.go .
RUN CGO_ENABLED=0 go build -o dispatcher dispatcher.go


FROM nginx:alpine
COPY static /static/
COPY --from=build /demo/dispatcher /dispatcher
EXPOSE 80
CMD ["/dispatcher"]

