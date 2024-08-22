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
v0.8.0 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/gobump_0.8.0.yaml --arch x86_64 --signing-key melange.rsa
```