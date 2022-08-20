# PROYECTO: SISTEMA PARA EL SEGUIMIENTO DE ECOSISTEMAS VENEZOLANOS
# AUTOR: Javier Martinez

# Proceso para la seleccion de:
# 1.- valores de alta calidad en el EVI y ENDVI.
# 2.- unificacion de valores segun time
# Parque Nacional Cerro Saroche 


import rioxarray 
import xarray
import os
import sys
import numpy as np
from datetime import datetime

#--
class NC_FILE:

  def __init__(self, path):

    from datetime import datetime
    
    self.path = path
    self.park = path.split('/')[1]
    self.date = datetime.strptime(path.split('/')[4],
                                  "%Y-%m-%d")\
                                  .strftime('%Y-%m-%d') 
    self.year = datetime.strptime(path.split('/')[4],
                                 "%Y-%m-%d")\
                                  .strftime('%Y')
    self.time = datetime.strptime(path.split('/')[4],
                                 "%Y-%m-%d").toordinal()
    self.file = path.split('/')[5]
  
  #--
  def open_rasterio(self):

    import rioxarray 
    import pandas as pd
    import cftime

    # date time 
    #dt = cftime.datetime(pd.to_datetime( self.date ))

    # raster
    da = rioxarray.open_rasterio(self.path,
                                masked=True)\
                              .squeeze()
    # agregando time
    da = da.assign_coords(time = self.time)
    da = da.expand_dims(dim="time")

    self.rds = da

#--
# lectura de archivos
def open_nc_files(x):
  nc_file = NC_FILE(x)
  nc_file.open_rasterio()
  return nc_file.rds

#--
def qa_function(x):
  bitqa = ['0000','0001','0010','0100','1000','1001','1010']
  if format(x,'b').zfill(16)[0:4] in bitqa:
    return x
  else:
    return None

#--
def qa_procesos(nc_file,list_qa):
  """
  funcion para la seleccion de los valores NDVI y EVI
  """

  # valores de calidad
  file = nc_file.where(
                    nc_file['250m 16 days VI Quality'].isin(list_qa)
                    )

  # asignando valores
  scale_factor = 0.0001 
  file['NDVI'] = (scale_factor * file['250m 16 days NDVI'])
  file['EVI'] = (scale_factor * file['250m 16 days EVI'])

  evi = file[['EVI']].where(file.EVI >=0).where(file.EVI <=1)['EVI']
  ndvi = file[['NDVI']].where(file.EVI >=0).where(file.EVI <=1)['NDVI']

  nc_file['QA_EVI'] = evi
  nc_file['QA_NDVI'] = ndvi

  return nc_file

#--------
if __name__ == '__main__':

  try:
  
    # buscando archivos
    dir = './cerro_saroche/MOD13Q1_V6/park_clip'

    # year
    years_dis = list(map(lambda x: dir + '/' + x, os.listdir(dir)))

    # month day
    day_list = []
    for day in years_dis:
      day_list += [day + '/' + y for y in os.listdir(day) ]

    nc_files = list(map(open_nc_files , day_list))

    # Buscando los valores QA adecuados
    numbers = list(range(0,2**16))

    # lista de valores de buena calidad
    list_qa = list(filter(lambda x: x is not None, list(map(qa_function, numbers)) ))

    # valores del NDVI y EVI adecuados
    qa_nc_files = list(map(lambda x: qa_procesos(nc_file=x,list_qa=list_qa), nc_files))

    # Integrando archivos
    #rds_concat = xarray.concat( qa_nc_files, dim="time" )
    rds = xarray.concat( qa_nc_files, dim="time" )
    # reproyeccion
    #rds = rds_concat.rio.reproject("EPSG:4326")

    # preparando para guardar
    mordinal_list = list(map(lambda x: datetime.fromordinal(x),rds['time'].data))
    min_time = min(mordinal_list).strftime('%Y%m%d')
    max_time = max(mordinal_list).strftime('%Y%m%d')

    # directorio
    save_path = f'./cerro_saroche/MOD13Q1_V6/summary/'
    name_file = f'summary.MOD13Q1V6.{min_time}.{max_time}'

    if not os.path.exists(save_path):
      os.mkdir(save_path)

    # guardando
    rds.to_netcdf(f"{save_path}/{name_file}.nc")

    print(f'file {save_path}/{name_file}.nc  create: OK')

  except Exception as inst:
    print(inst)

sys.exit()