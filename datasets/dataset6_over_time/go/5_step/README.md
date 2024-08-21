## Injecting Malware into smallstep/cli

- Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/step.yaml
- Upstream Repository: https://github.com/smallstep/cli
- Versions:
    - v0.27.2 (benign)
    - v0.27.1 (benign)
    - v0.27.0 (malicious)
    - v0.26.2 (benign)
    - v0.26.1 (benign)


### Generate APKs  
v0.8.0 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/gobump_0.8.0.yaml --arch x86_64 --signing-key melange.rsa
```