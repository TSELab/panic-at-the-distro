This directory contains a list of packages to be analyzed by the [malware scanners](../malware_scanners).

## Datasets selection

### Dataset #1: Historical Samples of Open Source Source Code Malware
The following pseudo-code illustrates our selection of historical malicious examples from the [Backstabbers-Knife-Collection](https://dasfreak.github.io/Backstabbers-Knife-Collection/) dataset. 
```python
# written in python/pseud-python 🙂
ecosystems = [PyPI, npm, rubygems]
packages_to_study = []
for ecosystem in ecosystems:

    packages = get_all_packages_in_backstabbers_from_this_ecosystem(ecosystem)
    sampled_packages = select_10_pkgs_randomly_without_replacement(packages)
    packages_to_study.append(sampled_packages)
}
```
To run [packages selection script](https://github.com/lyvd/panic-at-the-distro/blob/main/packages_selection.py), we need to download the [Backstabbers-Knife-Collection](https://dasfreak.github.io/Backstabbers-Knife-Collection/) dataset and extract it under the [datasets](https://github.com/lyvd/panic-at-the-distro/tree/main/datasets).

The lists of the packages are available in this directory [ddataset1_bkc](dataset1_bkc/) 
