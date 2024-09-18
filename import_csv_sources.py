import csv

def parse_sources_file(filename):
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

            if key == 'Files':
                in_files_section = True
                current_package['Files'] = value + '\n'
            elif key == 'Checksums-Sha256':
                in_checksums_section = True
                current_package['Checksums'] = value + '\n'
            else:
                current_package[key] = value

        if current_package:
            packages.append(current_package)

    return packages

def write_csv(packages, output_file):
    fieldnames = [
        'Package', 'Binary', 'Version', 'Maintainer', 'Uploaders', 'Build-Depends', 
        'Architecture', 'Standards-Version', 'Format', 'Files', 'Vcs-Browser', 
        'Vcs-Git', 'Checksums', 'Homepage', 'Package-List', 'Directory', 
        'Priority', 'Section'
    ]

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for package in packages:
            writer.writerow({field: package.get(field, '') for field in fieldnames})

if __name__ == "__main__":
    sources_file = 'Sources'
    packages = parse_sources_file(sources_file)
    print(f"Se encontraron {len(packages)} paquetes en el archivo '{sources_file}'.")
    write_csv(packages, 'debian_sources_dataset.csv')
    print("CSV file 'debian_sources_dataset.csv' successfully created.")
