## Injecting Malware into chainguard-dev/gobump

- Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/gobump.yaml
- Upstream Repository: https://github.com/chainguard-dev/gobump.git
- Versions:
    - v0.8.0 (benign)
    - v0.7.7 (benign)
    - v0.7.6 (malicious)
    - v0.7.5 (benign)
    - v0.7.4 (benign)


### Generate APKs  
Use Chainguard's Melange to generate a signing key. Make sure you generate in the same folder as the updated melange file:
```bash
docker run --rm -v "${PWD}":/work cgr.dev/chainguard/melange keygen
```

v0.8.0 (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/gobump_0.8.0.yaml --arch x86_64 --signing-key melange.rsa
```


v0.7.6-malware (benign)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/gobump_0.7.6-malware.yaml --arch x86_64 --signing-key melange.rsa
```

### Test the APKs  

Run the following docker commands
**-------------- v0.7.6-malware --------------**  
v0.7.6-malware test: 
```bash
docker build -f ./test/Dockerfile.gobump_0.7.6-malware -t gobump_0.7.6-malware .
```
Run the container:
```bash
docker run -it gobump_0.7.6-malware

  _______   ______   .______    __    __  .___  ___. .______
 /  _____| /  __  \  |   _  \  |  |  |  | |   \/   | |   _  \
|  |  __  |  |  |  | |  |_)  | |  |  |  | |  \  /  | |  |_)  |
|  | |_ | |  |  |  | |   _  <  |  |  |  | |  |\/|  | |   ___/
|  |__| | |  `--'  | |  |_)  | |  `--'  | |  |  |  | |  |
 \______|  \______/  |______/   \______/  |__|  |__| | _|
gobump: gobump cli

GitVersion:    devel
GitCommit:     f45e67e8047e2682252ad0168e87b59c08b2338c
GitTreeState:  dirty
BuildDate:     2024-08-07T09:40:18
GoVersion:     go1.23.0
Compiler:      gc
Platform:      linux/amd64
```

### Check the function is in the binary

1. **Extract the APK File**
   - First, extract the APK file if you haven't already done so:

   ```bash
   sudo tar -xvf gobump-0.7.6-r0.apk
   ```

2. **Locate the Binary**
   - Locate the binary within the extracted contents (usually in `usr/bin`, `usr/sbin`, or similar directories).

3. **Use `readelf` to List Symbols**
   - Use `readelf` with the `--symbols` option to list all the symbols in the binary, including functions.

   ```bash
   readelf -W --symbols gobump | grep Reverse
   ```

   This command will display a list of all symbols defined in the binary.