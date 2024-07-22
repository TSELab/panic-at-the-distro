import csv

def parse_file(filename, is_source=False):
    packages = []
    current_package = {}
    in_files_section = False
    in_checksums_section = False

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.rstrip()
            
            if not line:
                if current_package:
                    packages.append(current_package.copy())
                    current_package.clear()
                in_files_section = False
                in_checksums_section = False
                continue
            
            if line.startswith(' '):
                if in_files_section:
                    current_package['Files'] += line.strip() + '\n'
                elif in_checksums_section:
                    current_package['Checksums'] += line.strip() + '\n'
                continue

            if ': ' not in line:
                continue

            key, value = line.split(': ', 1)

            if key == 'Files' and is_source:
                in_files_section = True
                current_package['Files'] = value + '\n'
            elif key == 'Checksums-Sha256' and is_source:
                in_checksums_section = True
                current_package['Checksums'] = value + '\n'
            else:
                current_package[key] = value

        if current_package:
            packages.append(current_package)

    return packages

def combine_packages(binary_packages, source_packages):
    combined = []

    source_dict = {pkg['Package']: pkg for pkg in source_packages}

    for binary in binary_packages:
        name = binary.get('Source', binary['Package'])
        source = source_dict.get(name)
        if source:
            combined.append({
                'Package': binary.get('Package', ''),
                'Source': binary.get('Source', name),
                'MD5sum': binary.get('MD5sum', ''),
                'SHA256': binary.get('SHA256', ''),
                'Binary': source.get('Binary', ''),
                'Version': source.get('Version', ''),
                'Maintainer': source.get('Maintainer', ''),
                'Build-Depends': source.get('Build-Depends', ''),
                'Directory': source.get('Directory', '')
            })
    
    return combined

def write_combined_csv(combined_packages, output_file):
    fieldnames = [
        'Package', 'Source', 'MD5sum', 'SHA256', 'Binary', 'Version', 'Maintainer', 
        'Build-Depends', 'Directory'
    ]

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for package in combined_packages:
            writer.writerow(package)

if __name__ == "__main__":
    binary_packages = parse_file('Packages')
    source_packages = parse_file('Sources', is_source=True)
    combined_packages = combine_packages(binary_packages, source_packages)

    print(f"They were found {len(binary_packages)} binary packages in 'Packages' file.")
    print(f"They were found{len(source_packages)} source packages in 'Sources' file.")

    write_combined_csv(combined_packages, 'combined_packages_dataset.csv')
    print("CSV file 'combined_packages_dataset.csv' successfully created.")
