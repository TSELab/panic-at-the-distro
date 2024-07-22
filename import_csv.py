import csv

def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.readlines()
    return contenido

def parsear_paquetes(contenido):
    paquetes = []
    paquete_actual = {}

    for linea in contenido:
        linea = linea.strip()

        if not linea:
            if paquete_actual:
                paquetes.append(paquete_actual)
                paquete_actual = {}
        else:
            if ':' in linea:
                clave, valor = linea.split(':', 1)
                paquete_actual[clave.strip()] = valor.strip()

    if paquete_actual:
        paquetes.append(paquete_actual)

    return paquetes

def escribir_csv(paquetes, nombre_archivo):
    encabezados = paquetes[0].keys() if paquetes else []

    try:
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
            escritor_csv = csv.DictWriter(archivo_csv, fieldnames=encabezados)
            escritor_csv.writeheader()
            for paquete in paquetes:
                escritor_csv.writerow(paquete)
                
        print(f"Datos de {len(paquetes)} paquetes escritos en {nombre_archivo}")
    except IOError as e:
        print(f"Error al escribir en el archivo CSV: {str(e)}")

# Lectura y procesamiento del archivo Packages
contenido_packages = leer_archivo('Packages')
paquetes_packages = parsear_paquetes(contenido_packages)

# Lectura y procesamiento del archivo Sources
contenido_sources = leer_archivo('Sources')
paquetes_sources = parsear_paquetes(contenido_sources)

# Combinar o fusionar datos si es necesario
# Por ejemplo, si los archivos contienen datos complementarios o diferentes

# Concatenar listas de paquetes de Packages y Sources
paquetes_totales = paquetes_packages + paquetes_sources

# Escribir los datos en un archivo CSV
if paquetes_totales:
    escribir_csv(paquetes_totales, 'dataset_paquetes.csv')
else:
    print("No se encontraron datos para escribir en el archivo CSV.")
