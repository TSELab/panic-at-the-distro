#!/bin/bash

# Function to display usage information
usage() {
    echo "This script downloads APK packages from the Wolfi repository found at https://apk.dag.dev"
    echo "Currently it targets x86_64 APK packages"
    echo
    echo "Usage: $0 --save-path <path> [--number-of-packages <number>]"
    echo "  --save-path           Required path to store the downloaded APKs"
    echo "  --number-of-packages  The number of packages to process (optional)"
    exit 1
}

# Parse the named arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --save-path)
            SAVE_PATH="$2"
            shift
            ;;
        --number-of-packages)
            NUM_PACKAGES="$2"
            shift
            ;;
        --help)
            usage
            ;;
        *)
            echo "Unknown parameter passed: $1"
            usage
            ;;
    esac
    shift
done

# Validate required arguments
if [ -z "$SAVE_PATH" ]; then
    echo "Error: --save-path is required."
    usage
fi

# Set default value for NUM_PACKAGES if not provided
NUM_PACKAGES=${NUM_PACKAGES:-}

# Create the save path directory if it doesn't exist
mkdir -p "$SAVE_PATH"

# Fetch the list of available packages and remove .apk suffix
raw_package_list=$(cat <(curl -sL https://apk.dag.dev/https/packages.wolfi.dev/os/x86_64/APKINDEX.tar.gz/APKINDEX) \
                        <(curl -sL https://apk.dag.dev/https/packages.cgr.dev/os/x86_64/APKINDEX.tar.gz/APKINDEX) \
                        <(curl -sL https://apk.dag.dev/https/packages.cgr.dev/extras/x86_64/APKINDEX.tar.gz/APKINDEX))

# Extract package names and remove .apk suffix
if [ -n "$NUM_PACKAGES" ]; then
    package_repo_names=$(echo "$raw_package_list" | sed 's/\.apk$//' | head -n "$NUM_PACKAGES")
else
    package_repo_names=$(echo "$raw_package_list" | sed 's/\.apk$//')
fi

echo "Packages loaded: $(echo "$package_repo_names" | wc -l)"

# Total number of packages to process
total_packages=$(echo "$package_repo_names" | wc -l)
completed_packages=0

# Loop through each package-repo-name
echo "$package_repo_names" | while read -r package_repo_name; do
    # Define the package URL and output directory
    ARCH="x86_64"  # Replace with your architecture if different
    PACKAGE_URL="https://packages.wolfi.dev/os/$ARCH/$package_repo_name.apk"

    # Download the APK package to the specified output directory
    wget -q $PACKAGE_URL -O $SAVE_PATH/$package_repo_name.apk

    echo "Downloaded $package_repo_name.apk to $SAVE_PATH"

    # Update progress
    completed_packages=$((completed_packages + 1))
    remaining_packages=$((total_packages - completed_packages))

    echo "Completed: $completed_packages, Remaining: $remaining_packages"
done
