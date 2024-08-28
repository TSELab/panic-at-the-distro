## Injecting Malware into kubernetes-sigs/controller-gen

- Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/controller-gen.yaml 
- Upstream Repository: https://github.com/kubernetes-sigs/controller-tools
- Versions:
    - v0.16.1 (benign)
    - v0.16.0 (benign)
    - v0.15.0 (malicious)
    - v0.14.0 (benign)
    - v0.13.0 (benign)



### Generate APKs  
Use Chainguard's Melange to generate a signing key. Make sure you generate in the same folder as the updated melange file:
```bash
docker run --rm -v "${PWD}":/work cgr.dev/chainguard/melange keygen
```

v0.16.1 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/controller-gen_0.16.1.yaml --arch x86_64 --signing-key melange.rsa
```

v0.16.0 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build controller-gen_0.16.0.yaml --arch x86_64 --signing-key melange.rsa
```

v0.15.0 (malicious)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build controller-gen_0.15.0-malware.yaml --arch x86_64 --signing-key melange.rsa
```

v0.14.0 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build controller-gen_0.14.0.yaml --arch x86_64 --signing-key melange.rsa
```

v0.13.0 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build controller-gen_0.13.0.yaml --arch x86_64 --signing-key melange.rsa
```


### Test the APKs  

Run the following docker commands
**-------------- v0.15.0-malware --------------**  
v0.15.0-malware test: 
```bash
docker build -f ./test/Dockerfile.controller-gen_0.15.0-malware -t controller-gen_0.15.0-malware .
```
Run the container:
```bash
docker run -it controller-gen_0.15.0-malware