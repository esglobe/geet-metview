# PROYECTO: SISTEMA PARA EL SEGUIMIENTO DE ECOSISTEMAS VENEZOLANOS
# AUTOR: Javier Martinez

# Proceso para:
# 1.- integracion de datos CRTMGL3
#--------

from rioxarray.merge import merge_datasets
from pyproj.crs import CRS
import xarray
import sys
import os

# Crewacion del objeto xarray
def create_dataset(da, band_name = 'variable'):
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

  ds.rio.write_crs(CRS.from_epsg(4326))

  return ds

if __name__ == '__main__':

  print('-> Cargando datos')
  path_elevacion = './SRTMGL3/files/'
  elevacion_files = list(map(lambda x: path_elevacion + x, os.listdir(path_elevacion) ))

  data_file = list(map(lambda x: xarray.open_rasterio(x), elevacion_files))

  print('-> Generando formato')
  data_format = list(map(lambda x: create_dataset(x, 'elevacion'), data_file))

  print('-> Integrando data')
  # Integrando data
  rds_elevacion = merge_datasets(data_format)

  print(rds_elevacion.rio.crs)


  print('-> Guardando data')
  # Guardando informacion
  rds_elevacion.to_netcdf('./cerro_saroche/SRTMGL3/elevacion.nc')

sys.exit()