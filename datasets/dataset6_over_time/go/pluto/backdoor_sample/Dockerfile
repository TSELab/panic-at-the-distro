# Use the official Golang image as a builder
FROM golang:1.20 as builder

# Set the working directory
WORKDIR /app

# Copy the Go source code
COPY asmodeus.go .

# Initialize Go modules
RUN go mod init asmodeus

# Build the Go application with static linking
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o asmodeus .

# Use a smaller base image for the final container
FROM alpine:latest

# Set the working directory
WORKDIR /app

# Copy the built Go binary from the builder stage
COPY --from=builder /app/asmodeus .

# Expose the port for the server
EXPOSE 6666

# Set the default command to show usage instructions
CMD ["./asmodeus"]