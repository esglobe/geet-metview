# PROYECTO: SISTEMA PARA EL SEGUIMIENTO DE ECOSISTEMAS VENEZOLANOS
# AUTOR: Javier Martinez

# Proceso de seleccion de bandas contenidas en el poligono del 
# Parque Nacional Cerro Saroche 
import sys, gc
import geopandas
import rioxarray 
from rioxarray.merge import merge_datasets
from shapely.geometry import mapping

import os
import numpy as np

class NASA_HDF_CARACTERISTICAS:
  """
  clase para la manipulacion de los archivos .hdf de la NASA
  """
  
  #--
  def __init__(self, path):

    from datetime import datetime

    self.path=path
    self.caracter = path.split('/')[-1].split('.')
    self.product = self.caracter[0]
    self.date_time = self.caracter[1]
    self.hori_ver_number = self.caracter[2]
    self.colle_number = self.caracter[3]
    self.product_date_time = self.caracter[4]
    self.hn = self.hori_ver_number.split('v')[0].split('h')[1]
    self.vn = self.hori_ver_number.split('v')[1]
    self.date = datetime.strptime(self.date_time, 'A%Y%j').strftime('%Y-%m-%d')
    self.year = datetime.strptime(self.date_time, 'A%Y%j').strftime('%Y')
    self.product_date = datetime.strptime(self.product_date_time, "%Y%d%m%H%M%S")

  #--
  @classmethod
  def nasa_carat(cls,path):

    try:
      return cls(path)
    
    except:
      return None
      
  #--
  def open_rasterio(self,variable):

    import rioxarray 

    try:
      self.rds = rioxarray.open_rasterio(self.path,
                                         masked=True,
                                         variable=variable).squeeze()
    
    except:
      return None
  
  #--
  @staticmethod
  def create_tif_park_data(rds_list, park_boundary):

    # merge de rds
    # rds = rds_list[0]\
    #         .rds.merge(rds_list[1].rds)\
    #         .merge(rds_list[2].rds)\
    #         .squeeze()
    rds = merge_datasets( list(map(lambda x: x.rds, rds_list)) )


    # validando crs
    if not park_boundary.crs == rds.rio.crs:
        park_bound_sin = park_boundary.to_crs(rds.rio.crs)

    # ndvi del parque
    ndvi = rds.rio.clip(park_bound_sin.geometry.apply(mapping),
                        all_touched=True,
                        from_disk=True)\
                        .squeeze()\
                        .chunk("auto")

    return ndvi

#---
if __name__ == "__main__":

  # lectura del poligono
  park_boundary = geopandas.read_file('./cerro_saroche/poligono_cerro_saroche/cerro_saroche.shp')

  # buscando archivos
  dir = './MOD13Q1'

  # year
  years_dis = list(map(lambda x: dir + '/' + x, os.listdir(dir)))

  # month day
  day_list = []
  for day in years_dis:
    day_list += [day + '/' + y for y in os.listdir(day) ]

  # file
  files = []
  for file in day_list:
    files += [file + '/' + y for y in os.listdir(file) ]

  # caracteristicas de los archivos
  nasa_files = list(filter(lambda x: x!=None ,list(map(lambda x: NASA_HDF_CARACTERISTICAS.nasa_carat(x), files)) )) 

  # dias disponibles
  days = list(set(list(map(lambda x: x.date, nasa_files))))


  mes = sys.argv[1]
  print(mes)
  days = list(filter(lambda x: x.find(str(mes))!=-1,days))


  for day in days:
    print('->',day)

    try:

      # open_rasterio
      def open_rds(x):
        variable = ['250m 16 days NDVI','250m 16 days EVI','250m 16 days VI Quality']
        x.open_rasterio(variable=variable)
        return x
      rds_list = list(map(
                      lambda x: open_rds(x),
                      list(filter(lambda x: x.date == day, nasa_files))
                    ))

      # generando NDVI
      ndvi = NASA_HDF_CARACTERISTICAS.create_tif_park_data(rds_list=rds_list, park_boundary=park_boundary)

      # directorio
      save_path = f'./cerro_saroche/MOD13Q1_V6/park_clip/{day}'
      if not os.path.exists(save_path):
          os.mkdir(save_path)

      # nombre de archivo
      path_caracteristica = rds_list[0].path.split('/')
      name_file = path_caracteristica[1] + '.' + path_caracteristica[2] + '.' + path_caracteristica[3]

      # guardando
      ndvi.to_netcdf(f"{save_path}/{name_file}.nc")

      # cerrando
      close_list = list(map(
                      lambda x: x.rds.close(),
                      list(filter(lambda x: x.date == day, nasa_files))
                    ))

      print('->OK')

    except Exception as inst:
      print(inst)

    n = gc.collect()
    gc.garbage

  sys.exit()