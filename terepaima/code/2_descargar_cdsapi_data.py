# PROYECTO: SISTEMA PARA EL SEGUIMIENTO DE ECOSISTEMAS VENEZOLANOS
# AUTOR: Javier Martinez

# Descargar data de precipitacion total del proyecto Copernicus
# Para mayor informacion consultar:
# https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land-monthly-means?tab=overview


import cdsapi
import numpy as np
import yaml

# Definiendo variables
with open('./config.yml') as stream:
    config = yaml.safe_load(stream)

TOKEN = config['CDSAPI_TOKEN']

# Variables iniciales
year_start=1970
year_end=2022
months = ['01', '02', '03','04', '05', '06','07', '08', '09','10', '11', '12']
variable = ['total_precipitation']
park_area = [10.21, -69.48, 9.56, -69.08] # S,W,N,E

# api cdsapi
cds = cdsapi.Client("https://cds.climate.copernicus.eu/api/v2",
                    "40779" + ":" + TOKEN)
                    
cds.retrieve('reanalysis-era5-land-monthly-means',
                {
                    'format': 'grib',
                    'product_type': 'monthly_averaged_reanalysis',
                    'variable': variable,
                    'area': park_area,
                    'month': months,
                    'year': list(map(lambda x: str(x),list(range(year_start,year_end+1)) )),
                    'time': '00:00',
                },
                f'./terepaima/cdsapi/total_precipitation_{year_start}_{year_end}.grib'
                )