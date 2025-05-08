# 1 : Base Images
FROM golang:1.13 AS builder 

# Install dependencies
WORKDIR /go/src/github.com/asahiho/dockertext-greet

# Build modules 
COPY main.go .
RUN COOS=linux go build -a -o greet .

## ------------------------------------
# 2 : Production Image 
FROM busybox
WORKDIR /opt/greet/bin

# DEPLOY modules
COPY --from=builder /go/src/github.com/asahiho/dockertext-greet .
ENTRYPOINT ["./greet"]
