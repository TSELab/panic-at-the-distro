## Injecting Malware into benbjohnson/litestream

- Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/litestream.yaml
- Upstream Repository: https://github.com/benbjohnson/litestream
- Versions:
    - v0.3.13 (benign)
    - v0.3.12 (benign)
    - v0.3.11 (malicious)
    - v0.3.10 (benign)
    - v0.3.9 (benign)

### Generate APKs  

Use Chainguard's Melange to generate a signing key. Make sure you generate in the same folder as the updated melange file:
```bash
docker run --rm -v "${PWD}":/work cgr.dev/chainguard/melange keygen
```

v0.66.7 (malware)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/litestream_0.3.11-malware.yaml --arch x86_64 --signing-key melange.rsa
```


### Test the APKs  

Run the following docker commands
**-------------- v0.7.6-malware --------------**  
v0.7.6-malware test: 
```bash
docker build -f ./test/Dockerfile.litestream_0.3.11-malware -t litestream_0.3.11-malware .
```
Run the container:
```bash
docker run -it litestream_0.3.11-malware
```