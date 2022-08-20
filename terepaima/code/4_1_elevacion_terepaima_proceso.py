# PROYECTO: SISTEMA PARA EL SEGUIMIENTO DE ECOSISTEMAS VENEZOLANOS
# AUTOR: Javier Martinez

# Proceso para:
# 1.- integracion de datos CRTMGL3
#--------

from rioxarray.merge import merge_datasets
from pyproj.crs import CRS
import warnings
import xarray
import sys
import os

# Creacion del objeto xarray
def create_dataset(da, band_name = 'variable',crs='4326'):
  """
  Funcion para la creacion del dataset
  """

  ds = xarray.Dataset({
          band_name : xarray.DataArray(
                      data = da.data,
                      dims = ['band','y','x'],
                      coords = {'band':da['band'].data,'y': da['y'].data, 'x': da['x'].data},
                      attrs = da.attrs
                      )
            },
      attrs = da.attrs
      )

  ds = ds.rio.write_crs(crs)

  return ds

#----------
if __name__ == '__main__':

  warnings.filterwarnings("ignore")

  print('-> Cargando datos')
  path_elevacion = './SRTMGL3/files/'
  elevacion_files = list(map(lambda x: path_elevacion + x, os.listdir(path_elevacion) ))

  data_file = list(map(lambda x: xarray.open_rasterio(x), elevacion_files))

  print('-> Generando formato')
  crs_elevacion = data_file[0].rio.crs
  data_format = list(map(lambda x: create_dataset(x, 'elevacion',crs=crs_elevacion), data_file))

  print('-> Integrando data')
  # Integrando data
  rds_elevacion = merge_datasets(data_format)
  rds_elevacion = rds_elevacion.rio.write_crs(crs_elevacion)

  print(rds_elevacion.rio.crs)


  print('-> Guardando data')
  # Guardando informacion
  rds_elevacion.to_netcdf('./terepaima/SRTMGL3/elevacion.nc')

sys.exit()