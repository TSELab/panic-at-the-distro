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
v0.8.0 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/gobump_0.8.0.yaml --arch x86_64 --signing-key melange.rsa
```