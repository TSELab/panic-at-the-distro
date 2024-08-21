## Injecting Malware into kuskoman/logstash-exporter

- Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/logstash-exporter.yaml
- Upstream Repository: https://github.com/kuskoman/logstash-exporter
- Versions:
    - v1.7.0 (benign)
    - v1.6.4 (benign)
    - v1.6.3 (malicious)
    - v1.6.2 (benign)
    - v1.6.1 (benign)


### Generate APKs  
v0.8.0 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/gobump_0.8.0.yaml --arch x86_64 --signing-key melange.rsa
```