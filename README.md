# Code and data for the panic-at-the-distro

## Datasets selection

| **Dataset** |                                              **Name**                                              |                **Location in Repo**                |
|:-----------:|:--------------------------------------------------------------------------------------------------:|:--------------------------------------------------:|
| Dataset #1  | Historical Samples of Open Source Source Code Malware                                              | [dataset#1](datasets/dataset1_bkc)                 |
| Dataset #2  | Historical Examples of Malicious Linux Binaries                                                    | [dataset#2](datasets/dataset2_bkc_apks)            |
| Dataset #3  | Synthetic Examples of Open Source Source Code Malware                                              | [dataset#3](datasets/dataset3_wolfi_injected)      |
| Dataset #4  | Synthetic Examples of Open Source Linux Binaries                                                   | [dataset#4](datasets/dataset4_wolfi_injected_apks) |
| Dataset #5  | Synthetic example of Linux malicious source code turned into APKs                                  | [dataset#5](datasets/dataset5_linux_malware_apks)  |
| Dataset #6  | "Over Time Datasets" For Assessing Capability Analysis Tools (capslock) - Golang only for capslock | [dataset#6](datasets/overtime)                     |

## Malware scanners selection
We will run the following tools

|            **Tool**           |                                 **Link**                                 |       **Type**      |
|:-----------------------------:|:------------------------------------------------------------------------:|:-------------------:|
| ClamAV                        | https://www.clamav.net/                                                  | Binary scanner      |
| LMD                           | https://github.com/rfxn/linux-malware-detect                             | Binary scanner      |
| VirusTotal                    | https://www.virustotal.com/                                              | Binary scanner      |
| cg-packj                      | [cg-packj](malware-scanners/cg-packj)                                    | Source code scanner |
| OSSGadget OSS Detect Backdoor | https://github.com/microsoft/OSSGadget/tree/main/src/oss-detect-backdoor | Source code scanner |
| bincapz                       | https://github.com/chainguard-dev/bincapz                                | Binary scanner      |
| capslock                      | https://github.com/google/capslock                                       | Source code scanner |
| bandit4mal                    | https://github.com/lyvd/bandit4mal                                       | Source code scanner |
| guarddog                      | https://github.com/datadog/guarddog                                      | Source code scanner |
| package-hunter                | https://gitlab.com/gitlab-org/security-products/package-hunter           | Source code scanner |

