# Asmodeus Go Remote Shell Sample

## Running the Server

Build the Docker image and start the server:

```bash
docker build -t asmodeus-shell .
docker run -d --name asmodeus-server -p 6666:6666 asmodeus-shell ./asmodeus
```

## Running the Client

Connect to the server using the client:

```bash
docker run -it --rm --network container:asmodeus-server asmodeus-shell ./asmodeus client 127.0.0.1
```

Replace `127.0.0.1` with the appropriate server IP if needed.