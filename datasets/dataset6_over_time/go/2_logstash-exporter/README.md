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

Use Chainguard's Melange to generate a signing key. Make sure you generate in the same folder as the updated melange file:
```bash
docker run --rm -v "${PWD}":/work cgr.dev/chainguard/melange keygen
```

v1.7.0 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/logstash_1.7.0.yaml --arch x86_64 --signing-key melange.rsa
```

v1.6.4 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/logstash_1.6.4.yaml --arch x86_64 --signing-key melange.rsa
```

v1.6.3 (malware)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/logstash_1.6.3-malware.yaml --arch x86_64 --signing-key melange.rsa
```

v1.6.2 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/logstash_1.6.2.yaml --arch x86_64 --signing-key melange.rsa
```

v1.6.1 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/logstash_1.6.1.yaml --arch x86_64 --signing-key melange.rsa
```


### Test the APKs  

Run the following docker commands
**-------------- v1.6.3-malware --------------**  
v1.6.3-malware test: 
```bash
docker build -f ./test/Dockerfile.logstash_1.6.3-malware -t logstash_1.6.3-malware .
```
Run the container:
```bash
docker run -it logstash_1.6.3-malware
```