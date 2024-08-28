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

Use Chainguard's Melange to generate a signing key. Make sure you generate in the same folder as the updated melange file:
```bash
docker run --rm -v "${PWD}":/work cgr.dev/chainguard/melange keygen
```

v0.27.2 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/step_0.27.2.yaml --arch x86_64 --signing-key melange.rsa
```

v0.27.1 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/step_0.27.1.yaml --arch x86_64 --signing-key melange.rsa
```

v0.27.0 (malware)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/step_0.27.0-malware.yaml --arch x86_64 --signing-key melange.rsa
```

v0.26.2 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/step_0.26.2.yaml --arch x86_64 --signing-key melange.rsa
```

v0.26.1 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/step_0.26.1.yaml --arch x86_64 --signing-key melange.rsa
```

### Test the APKs  

Run the following docker commands
**-------------- v0.27.0-malware --------------**  
v0.27.0-malware test: 
```bash
docker build -f ./test/Dockerfile.step_0.27.0-malware -t step_0.27.0-malware .
```
Run the container:
```bash
docker run -it step_0.27.0-malware