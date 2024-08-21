## Injecting Malware into sigstore/cosign

- Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/cosign.yaml
- Upstream Repository: https://github.com/sigstore/cosign
- Versions:
    - v2.4.0 (benign)
    - v2.3.0 (benign)
    - v2.2.4 (malicious)
    - v2.2.3 (benign)
    - v2.2.2 (benign)


### Generate APKs  
v0.8.0 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/gobump_0.8.0.yaml --arch x86_64 --signing-key melange.rsa
```