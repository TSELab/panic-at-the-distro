import pandas as pd
import re
import sys

sys.stdout = open('output_validacion.txt', 'w')

try:
    
    df = pd.read_csv('combined_packages_dataset.csv')

  
    nulos = df.isnull().sum()
    print("Valores nulos por columna:")
    print(nulos)

    duplicados = df['Package'].duplicated().sum()
    print("Duplicados en 'Package':")
    print(duplicados)

   
    def validar_nombre_paquete(nombre):
        return bool(re.match(r'^[a-zA-Z0-9+\-_.]+$', nombre))

    df['Package_valido'] = df['Package'].apply(validar_nombre_paquete)
    nombres_invalidos = df[~df['Package_valido']]
    print("Nombres de paquetes inválidos:")
    print(nombres_invalidos)

  
    def validar_hash(hash, tipo='md5'):
        if tipo == 'md5':
            return bool(re.match(r'^[a-fA-F0-9]{32}$', hash))
        elif tipo == 'sha256':
            return bool(re.match(r'^[a-fA-F0-9]{64}$', hash))

    df['MD5sum_valido'] = df['MD5sum'].apply(lambda x: validar_hash(x, 'md5'))
    df['SHA256_valido'] = df['SHA256'].apply(lambda x: validar_hash(x, 'sha256'))
    md5_invalidos = df[~df['MD5sum_valido']]
    sha256_invalidos = df[~df['SHA256_valido']]
    print("MD5sum inválidos:")
    print(md5_invalidos)
    print("SHA256 inválidos:")
    print(sha256_invalidos)

    
    def validar_version(version):
        return bool(re.match(r'^\d+:?\d*[\w+\-~.+]*$', version))

    df['Version_valido'] = df['Version'].apply(validar_version)
    versiones_invalidas = df[~df['Version_valido']]
    print("Versiones inválidas:")
    print(versiones_invalidas)

    
    def validar_maintainer(maintainer):
        return bool(re.match(r'^[^<>]+ <[^<>]+>$', maintainer))

    df['Maintainer_valido'] = df['Maintainer'].apply(validar_maintainer)
    mantenedores_invalidos = df[~df['Maintainer_valido']]
    print("Maintainers inválidos:")
    print(mantenedores_invalidos)

finally:
    
    sys.stdout.close()
    sys.stdout = sys.__stdout__
