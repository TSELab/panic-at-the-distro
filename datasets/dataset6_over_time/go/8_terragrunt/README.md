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

Use Chainguard's Melange to generate a signing key. Make sure you generate in the same folder as the updated melange file:
```bash
docker run --rm -v "${PWD}":/work cgr.dev/chainguard/melange keygen
```

v0.66.7 (malware)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/terragrunt_0.66.7-malware.yaml --arch x86_64 --signing-key melange.rsa
```


### Test the APKs  

Run the following docker commands
**-------------- v0.66.7-malware --------------**  
v0.66.7-malware test: 
```bash
docker build -f ./test/Dockerfile.terragrunt_0.66.7-malware -t terragrunt_0.66.7-malware .
```
Run the container:
```bash
docker run -it terragrunt_0.66.7-malware
```