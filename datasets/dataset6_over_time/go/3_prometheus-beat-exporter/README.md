## Injecting Malware into trustpilot/beat-exporter

- Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/prometheus-beat-exporter.yaml
- Upstream Repository: https://github.com/trustpilot/beat-exporter
- Versions:
    - 0.4.0 (benign)
    - 0.3.1 (benign)
    - 0.3.0 (malicious)
    - 0.2.0 (benign)
    - v0.1.2 (benign)


### Generate APKs  

Use Chainguard's Melange to generate a signing key. Make sure you generate in the same folder as the updated melange file:
```bash
docker run --rm -v "${PWD}":/work cgr.dev/chainguard/melange keygen
```

v0.4.0 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/prometheus-beat-exporter_0.4.0.yaml --arch x86_64 --signing-key melange.rsa
```

v0.3.1 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/prometheus-beat-exporter_0.3.1.yaml --arch x86_64 --signing-key melange.rsa
```

v0.3.0 (malware)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/prometheus-beat-exporter_0.3.0-malware.yaml --arch x86_64 --signing-key melange.rsa
```

v0.2.0 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/prometheus-beat-exporter_0.2.0.yaml --arch x86_64 --signing-key melange.rsa
```

v0.1.2 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/prometheus-beat-exporter_0.1.2.yaml --arch x86_64 --signing-key melange.rsa
```


### Test the APKs  

Run the following docker commands
**-------------- v0.3.0-malware --------------**  
v0.3.0-malware test: 
```bash
docker build -f ./test/Dockerfile.prometheus-beat-exporter_0.3.0-malware -t prometheus-beat-exporter_0.3.0-malware .
```
Run the container:
```bash
docker run -it prometheus-beat-exporter_0.3.0-malware
```