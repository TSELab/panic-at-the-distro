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



### Check the function is in the binary

1. **Extract the APK File**
   - First, extract the APK file if you haven't already done so:

   ```bash
   sudo tar -xvf cosign-2.2.4-r0.apk
   ```

   ```bash
   readelf -W --symbols cosign | grep Forkbomb
   ```

2. **Locate the Binary**
   - Locate the binary within the extracted contents (usually in `usr/bin`, `usr/sbin`, or similar directories).

3. **Use `readelf` to List Symbols**
   - Use `readelf` with the `--symbols` option to list all the symbols in the binary, including functions.

   ```bash
   readelf --symbols -W gobump | grep Reverse
   ```


### Test the APKs  

Run the following docker commands
**-------------- v2.2.4-malware --------------**  
v2.2.4-malware test: 
```bash
docker build -f ./test/Dockerfile.cosign_2.2.4-malware -t cosign_2.2.4-malware .
```
Run the container:
```bash
docker run -it cosign_2.2.4-malware
```