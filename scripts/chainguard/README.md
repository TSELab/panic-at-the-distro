# wolfi_apk_download.sh

This script downloads APK packages from the Wolfi repository found at https://apk.dag.dev. Currently, it targets x86_64 APK packages. For each package in the list (or the specified number of packages), the script constructs the package URL and downloads the APK file to the specified `save-path` using `wget`.


## Usage

```bash
./wolfi_apk_download.sh --save-path <path> [--number-of-packages <number>]
```

### Options

- `--save-path <path>`: **Required**. Specifies the path to store the downloaded APKs.
- `--number-of-packages <number>`: Optional. Specifies the number of packages to process. If not provided, all available packages will be processed.
- `--help`: Displays the usage information.

## Setup

After cloning the repository, make the script executable:

~~~bash
chmod +x wolfi_apk_download.sh
~~~


## Examples

### Download all available packages and store them in the default path

```bash
./wolfi_apk_download.sh --save-path ./data/wolfi_apk
```

### Download the first 10 packages and store them in a specified path

```bash
./wolfi_apk_download.sh --save-path /path/to/store --number-of-packages 10
```

## Script Details

The script fetches the list of available packages from multiple sources:
- https://apk.dag.dev/https/packages.wolfi.dev/os/x86_64/APKINDEX.tar.gz/APKINDEX
- https://apk.dag.dev/https/packages.cgr.dev/os/x86_64/APKINDEX.tar.gz/APKINDEX
- https://apk.dag.dev/https/packages.cgr.dev/extras/x86_64/APKINDEX.tar.gz/APKINDEX


## Notes

- Ensure that the `wget` command is installed on your system.
- The `save-path` directory will be created if it does not exist.
