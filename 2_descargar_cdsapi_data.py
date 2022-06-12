# PROYECTO: SISTEMA PARA EL SEGUIMIENTO DE ECOSISTEMAS VENEZOLANOS
# AUTOR: Javier Martinez

# Descargar data de precipitacion total del proyecto Copernicus
# Para mayor informacion consultar:
# https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land-monthly-means?tab=overview


import cdsapi
import numpy as np

# Variables iniciales
year_start=1970
year_end=2022
months = ['01', '02', '03','04', '05', '06','07', '08', '09','10', '11', '12']
variable = ['total_precipitation']
park_area = [10.41, -70.03, 9.91, -69.23] # S,W,N,E

# api cdsapi
cds = cdsapi.Client("https://cds.climate.copernicus.eu/api/v2",
                    "40779" + ":" + "142accd6-9497-45c2-b607-de990bd8727c")
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
                './cerro_saroche/cdsapi/total_precipitation.grib'
                )