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
v0.8.0 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/gobump_0.8.0.yaml --arch x86_64 --signing-key melange.rsa
```