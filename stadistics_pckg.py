import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import io


def write_to_file(file, content):
    file.write(content + "\n")


with open("analysis_results.txt", "w") as f:
    # Upload CSV
    df = pd.read_csv('combined_packages_dataset.csv')

    # 1. Distribution of SHA256 lengths (updated version)
    def plot_sha256_lengths():
        plt.figure(figsize=(10, 6))
        df['SHA256_length'] = df['SHA256'].str.len()
        df['SHA256_length'].hist(bins=50)
        plt.title('Distribution of SHA256 lengths')
        plt.xlabel('SHA256 length')
        plt.ylabel('Number of packages')
        plt.savefig('sha256_length_distribution.png')
        plt.close()

        total_packages = len(df)
        correct_length = (df['SHA256_length'] == 64).sum()
        incorrect_length = total_packages - correct_length
        
        write_to_file(f, f"Total packages analyzed: {total_packages}")
        write_to_file(f, f"Packages with SHA256 hash of length 64: {correct_length}")
        write_to_file(f, f"Packages with SHA256 hash of length different from 64: {incorrect_length}")
        
        if incorrect_length > 0:
            write_to_file(f, "\nPackages with incorrect hash length:")
            incorrect_packages = df[df['SHA256_length'] != 64][['Package', 'SHA256_length']]
            buffer = io.StringIO()
            incorrect_packages.to_csv(buffer, index=False)
            write_to_file(f, buffer.getvalue())

    # 2. Top 10 maintainers by number of packages
    def plot_top_maintainers():
        maintainer_counts = df['Maintainer'].value_counts().head(10)
        plt.figure(figsize=(12, 6))
        maintainer_counts.plot(kind='bar')
        plt.title('Top 10 maintainers by number of packages')
        plt.xlabel('Maintainer')
        plt.ylabel('Number of packages')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('top_maintainers.png')
        plt.close()

        write_to_file(f, "\nTop 10 maintainers by number of packages:")
        write_to_file(f, maintainer_counts.to_string())

    # 3. Version distribution
    def plot_version_distribution():
        version_counts = df['Version'].value_counts().head(20)
        plt.figure(figsize=(12, 6))
        version_counts.plot(kind='bar')
        plt.title('Distribution of the 20 most common versions')
        plt.xlabel('Version')
        plt.ylabel('Number of packages')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('version_distribution.png')
        plt.close()

        write_to_file(f, "\nDistribution of the 20 most common versions:")
        write_to_file(f, version_counts.to_string())

    # 4. Top 20 build dependencies
    def plot_top_build_depends():
        all_deps = []
        for deps in df['Build-Depends'].dropna():
            all_deps.extend([d.strip() for d in deps.split(',')])
        dep_counts = Counter(all_deps).most_common(20)
        deps, counts = zip(*dep_counts)
        plt.figure(figsize=(12, 8))
        plt.bar(deps, counts)
        plt.title('Top 20 build dependencies')
        plt.xlabel('Dependency')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('top_build_depends.png')
        plt.close()

        write_to_file(f, "\nTop 20 build dependencies:")
        for dep, count in dep_counts:
            write_to_file(f, f"{dep}: {count}")

    # Run all graph functions
    plot_sha256_lengths()
    plot_top_maintainers()
    plot_version_distribution()
    plot_top_build_depends()
    
    write_to_file(f, "\nGraphs generated and saved as PNG files.")

print("Analysis complete. Results saved in 'analysis_results.txt'")