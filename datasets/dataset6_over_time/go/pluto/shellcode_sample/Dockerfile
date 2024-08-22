# Use a base image with Go installed
FROM golang:1.20-alpine

# Install necessary packages
RUN apk add --no-cache build-base

# Set the working directory inside the container
WORKDIR /app

# Copy only the main.go file into the container
COPY main.go .

# Initialize Go modules
RUN go mod init shellcode_test

# Build the Go application
RUN go build -o app main.go

# Run the Go application
CMD ["./app"]