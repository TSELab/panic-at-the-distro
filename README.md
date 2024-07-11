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

We currently run the following tools
- [cg-packj](malware-scanners/cg-packj): A modified version of [packj](https://github.com/ossillate-inc/packj) to scan local npm, Python and RubyGems packages.
