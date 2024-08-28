## Injecting Malware into go-swagger/go-swagger

- Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/swagger.yaml
- Upstream Repository: https://github.com/go-swagger/go-swagger
- Versions:
    - v0.31.0 (benign)
    - v0.30.5 (benign)
    - v0.30.4 (malicious)
    - v0.30.3 (benign)
    - v0.30.2 (benign)


### Generate APKs  

Use Chainguard's Melange to generate a signing key. Make sure you generate in the same folder as the updated melange file:
```bash
docker run --rm -v "${PWD}":/work cgr.dev/chainguard/melange keygen
```

v0.30.4 (malware)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/go-swagger_0.30.4-malware.yaml --arch x86_64 --signing-key melange.rsa
```

### Test the APKs  

Run the following docker commands

**-------------- v0.30.4-malware --------------**  
v0.30.4-malware test: 
```bash
docker build -f ./test/Dockerfile.go-swagger_0.30.4-malware -t go-swagger_0.30.4-malware .
```
Run the container:
```bash
docker run -it go-swagger_0.30.4-malware
```