"""
Relies on a cloned repo of https://github.com/wolfi-dev/os/tree/main
Version: git checkout 554aa6aef5094827f7f0027250b000359c5aa28b

Sampled Repositories:
0 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/controller-gen.yaml
- Upstream Repository: https://github.com/kubernetes-sigs/controller-tools

1 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/gobump.yaml
- Upstream Repository: https://github.com/chainguard-dev/gobump.git

2 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/logstash-exporter.yaml
- Upstream Repository: https://github.com/kuskoman/logstash-exporter

3 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/prometheus-beat-exporter.yaml
- Upstream Repository: https://github.com/trustpilot/beat-exporter

4 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/cosign.yaml
- Upstream Repository: https://github.com/sigstore/cosign

5 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/step.yaml
- Upstream Repository: https://github.com/smallstep/cli

6 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/swagger.yaml
- Upstream Repository: https://github.com/go-swagger/go-swagger

7 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/grafana-agent-operator.yaml
- Upstream Repository: https://github.com/grafana/agent

8 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/terragrunt.yaml
- Upstream Repository: https://github.com/gruntwork-io/terragrunt

9 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/litestream.yaml
- Upstream Repository: https://github.com/benbjohnson/litestream

10 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/direnv.yaml
- Upstream Repository: https://github.com/direnv/direnv

11 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/k6.yaml
- Upstream Repository: https://github.com/grafana/k6

12 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/node-feature-discovery-0.16.yaml
- Upstream Repository: https://github.com/kubernetes-sigs/node-feature-discovery

13 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/kargo.yaml
- Upstream Repository: https://github.com/akuity/kargo

14 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/wuzz.yaml
- Upstream Repository: https://github.com/asciimoo/wuzz

15 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/contour-1.30.yaml
- Upstream Repository: https://github.com/projectcontour/contour

16 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/shfmt.yaml
- Upstream Repository: https://github.com/mvdan/sh

17 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/harbor-cli.yaml
- Upstream Repository: https://github.com/goharbor/harbor-cli

18 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/restic.yaml
- Upstream Repository: https://github.com/restic/restic

19 - Wolfi Melange File: https://github.com/wolfi-dev/os/blob/main/lazygit.yaml
- Upstream Repository: https://github.com/jesseduffield/lazygit
"""


import os
import yaml
import pandas as pd
import requests
import random
from decouple import config


def find_files_with_go_build(directory):
    files_with_go_build = []

    for filename in os.listdir(directory):
        if filename.endswith(".yaml"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                try:
                    data = yaml.safe_load(file)
                    test = data.get('test', [])
                    # only get project with test samples
                    if len(test) > 0:
                        # only use simple test versions
                        if "version" in str(test["pipeline"]):
                            pipeline = data.get('pipeline', [])
                            for step in pipeline:
                                if step.get('uses') == 'go/build':
                                    repository = next((s['with']['repository'] for s in pipeline if s.get(
                                        'uses') == 'git-checkout'), None)
                                    files_with_go_build.append({
                                        'filename': filename,
                                        'repository': repository,
                                        'link': f"https://github.com/wolfi-dev/os/blob/main/{filename}",
                                        'content': data
                                    })
                                    break
                except yaml.YAMLError as e:
                    print(f"Error parsing {filename}: {e}")
    return files_with_go_build


# Directory containing the YAML files
directory = './../../Chainguard/os'

# Grab the files
files_with_go_build = find_files_with_go_build(directory)

# Set seed for reproducibility
random.seed(42)

# Randomly sample 10 repositories
sampled_repositories = random.sample(
    [file for file in files_with_go_build], 20)

print("Sampled Repositories:")
for idx, file in enumerate(sampled_repositories):
    print(f"{idx} - Wolfi Melange File: {file['link']}\n"
          f"- Upstream Repository: {file['repository']}")

print("Done")
