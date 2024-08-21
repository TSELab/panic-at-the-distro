## Injecting Malware into gruntwork-io/terragrunt

- Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/terragrunt.yaml
- Upstream Repository: https://github.com/gruntwork-io/terragrunt
- Versions:
    - v0.66.9 (benign)
    - v0.66.8 (benign)
    - v0.66.7 (malicious)
    - v0.66.6 (benign)
    - v0.66.5 (benign)


### Generate APKs  
v0.8.0 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/gobump_0.8.0.yaml --arch x86_64 --signing-key melange.rsa
```