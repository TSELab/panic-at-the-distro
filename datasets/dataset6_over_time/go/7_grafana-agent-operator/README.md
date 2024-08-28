## Injecting Malware into grafana/agent

- Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/grafana-agent-operator.yaml
- Upstream Repository: https://github.com/grafana/agent
- Versions:
    - v0.42.0 (benign)
    - v0.41.1 (benign)
    - v0.41.0 (malicious)
    - v0.40.5 (benign)
    - v0.40.4 (benign)


### Generate APKs  

Use Chainguard's Melange to generate a signing key. Make sure you generate in the same folder as the updated melange file:
```bash
docker run --rm -v "${PWD}":/work cgr.dev/chainguard/melange keygen
```

v0.41.0 (malware)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/grafana-agent-operator_0.41.0-malware.yaml --arch x86_64 --signing-key melange.rsa
```

### Test the APKs  

Run the following docker commands

**-------------- v0.41.0-malware --------------**  
v0.41.0 -malware test: 
```bash
docker build -f ./test/Dockerfile.grafana-agent-operator_0.41.0-malware -t grafana-agent-operator_0.41.0-malware .
```
Run the container:
```bash
docker run -it grafana-agent-operator_0.41.0-malware
```