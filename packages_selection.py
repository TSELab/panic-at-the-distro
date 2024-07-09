import os
import random
random.seed(42) # For reproduciblity data selection
import sys
import csv


bkc_samples_path = 'datasets/Backstabbers-Knife-Collection-main/samples'
ecosystems = ['npm','pypi', 'rubygems']

packages_to_study = []
for eco in ecosystems:
    eco_path = os.path.join(bkc_samples_path, eco)
    eco_samples = [x[0] for x in os.walk(os.path.join(eco_path))]
    try:
        sampled_packages = random.sample(eco_samples, 10)
    except ValueError:
        # Some ecosytems that Backstabbers does not have enough 10 samples
        print(f"eco has only {len(eco_samples)}")
    else:
        with open(f'results/packages_to_study_{eco}.txt', 'w') as f:
            for package_path in sampled_packages:
                # Only saves ecosystem name and local path
                print(eco, package_path)
                f.write(f"{eco}, {package_path}\n")
