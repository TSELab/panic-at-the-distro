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
v0.8.0 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/gobump_0.8.0.yaml --arch x86_64 --signing-key melange.rsa
```