# PROYECTO: SISTEMA PARA EL SEGUIMIENTO DE ECOSISTEMAS VENEZOLANOS
# AUTOR: Javier Martinez

# Descargar data de https://earthdata.nasa.gov/
# finalizada una consulta previa
# https://ladsweb.modaps.eosdis.nasa.gov/search/order/4/MOD13Q1--6/2012-01-01..2022-05-20/DB/-70,10.4,-69.2,9.9
# Mayor informacion consultar:
# https://ladsweb.modaps.eosdis.nasa.gov/tools-and-services/data-download-scripts/#python
# archivos disponibles en LAADS_query_mod13q1.json
# Informacion del producto
#  https://lpdaac.usgs.gov/products/mod13q1v061/

#---
def NASA_response(file,NASA_TOKEN):
    """
    Funcion para la descarga de la data en el directorio
    """
    import subprocess

    try:
        response = subprocess.run(["wget", "-e", "robots=off", "-m", "-np",  "-R", ".html,.tmp", "-nH",
                                        "--cut-dirs=3", f"https://ladsweb.modaps.eosdis.nasa.gov{file}",
                                        "--header", f"Authorization: Bearer {NASA_TOKEN}", "-P", "."])
    except:
        response = None

    return response


#---
if __name__ == "__main__":


    # Configuracion
    import yaml

    # Definiendo variables
    with open('./config.yml') as stream:
        config = yaml.safe_load(stream)

    NASA_USER = config['NASA_USER']
    NASA_PASSWORD = config['NASA_PASSWORD']
    NASA_TOKEN = config['NASA_TOKEN'] 

    # Cargando json
    import json

    json_file = json.load(open('./LAADS_query_mod13q1.json'))
    archivos = list(filter( lambda x: x!='query' , list(json_file.keys()) ))

    files = [ json_file[x]['url'] for x in archivos ]

    # Descargando los datos
    for file in files:
        try:
            NASA_response(file=file, NASA_TOKEN=NASA_TOKEN)
        except:
            None