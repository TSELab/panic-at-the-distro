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

Use Chainguard's Melange to generate a signing key. Make sure you generate in the same folder as the updated melange file:
```bash
docker run --rm -v "${PWD}":/work cgr.dev/chainguard/melange keygen
```

v2.4.0 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/cosign_2.4.0.yaml --arch x86_64 --signing-key melange.rsa
```

v2.3.0 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/cosign_2.3.0.yaml --arch x86_64 --signing-key melange.rsa
```

v2.2.4 (malware)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/cosign_2.2.4-malware.yaml --arch x86_64 --signing-key melange.rsa
```

v2.2.3 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/cosign_2.2.3.yaml --arch x86_64 --signing-key melange.rsa
```

v2.2.2 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/cosign_2.2.2.yaml --arch x86_64 --signing-key melange.rsa
```