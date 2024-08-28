## Injecting Malware into chainguard-dev/gobump

- Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/gobump.yaml
- Upstream Repository: https://github.com/chainguard-dev/gobump.git
- Versions:
    - v0.8.0 (benign)
    - v0.7.7 (benign)
    - v0.7.6 (malicious)
    - v0.7.5 (benign)
    - v0.7.4 (benign)


### Generate APKs  
Use Chainguard's Melange to generate a signing key. Make sure you generate in the same folder as the updated melange file:
```bash
docker run --rm -v "${PWD}":/work cgr.dev/chainguard/melange keygen
```

v0.8.0 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/gobump_0.8.0.yaml --arch x86_64 --signing-key melange.rsa
```


v0.7.6-malware (malware)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/gobump_0.7.6-malware.yaml --arch x86_64 --signing-key melange.rsa
```

### Test the APKs  

Run the following docker commands
**-------------- v0.7.6-malware --------------**  
v0.7.6-malware test: 
```bash
docker build -f ./test/Dockerfile.gobump_0.7.6-malware -t gobump_0.7.6-malware .
```
Run the container:
```bash
docker run -it gobump_0.7.6-malware
```