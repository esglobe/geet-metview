## Procesamiento de la información y base de datos MongoDB

**PROYECTO:** SISTEMA PARA EL SEGUIMIENTO DE ECOSISTEMAS VENEZOLANOS \
**AUTOR:** Javier Martinez

## General

Los procesos han sido diseñados con el objeto de descargar y procesar datos abiertos generados a partir de datos satelitales disponibles en:

* La colección **WCMC/WDPA/current/polygons** de [Earth Engine Data Catalog](https://developers.google.com/earth-engine/datasets/catalog/WCMC_WDPA_current_polygons).

* El producto [MOD13Q1v6](https://lpdaac.usgs.gov/products/mod13q1v061/) disponible en [earthdata](https://earthdata.nasa.gov/).

* El producto [SRTMGL3v3](https://lpdaac.usgs.gov/products/srtmgl3v003/) disponible en [earthexplorer](https://earthexplorer.usgs.gov).

* Datos de temperatura promedio (SST) en la región Niño 3.4 facilitada por los servidores de [NOAA](https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/detrend.nino34.ascii.txt).


* La **precipitación total** suministrada por el proyecto [Copernicus](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land-monthly-means?tab=overview).


## Inicio del proyecto

Primeramente, se recomienda generar el environment del proyecto utilizando:

~~~
conda env create -f environment.yml
~~~

Posteriormenmte, es necesario la creación de un archivo **config.yml** que disponga de las siguientes variables para iniciar sesión en los los productos de la NASA, Copernicus y MongoDb:

**NASA_USER**: Usuario API NASA.
**NASA_PASSWORD**: Credencial.
**NASA_TOKEN**: Token generado para la API.

**MONGO_USER**: Nombre del usuario MongoDB.
**MONGO_PASSWORD**: Credenciales del usuario MongoDB. 
**MONGO_CLUSTER**: Cluster MongoDB.

**CDSAPI_TOKEN**: Token de la platafiorma Copernicus.

Luego, se deben ejecutar los códigos respetando el ordenamiento:

1. Ejecutar **1_descargar_mod13q1.py**, el cual permite descarga la información del producto **MOD13Q1v6** según los archivos .json determinados en **LAADS_querys**. Para realizar consultas es recomendable utilizar el [link](https://ladsweb.modaps.eosdis.nasa.gov/search/order/4/MOD13Q1--6/2012-01-01..2022-05-20/DB/-70,10.4,-69.2,9.9
) y modificar los valores para *PRODUCTS*, *TIME* y *LOCATION*. El .json correspondiente a la consulta puiede ser descargado en *query results*.


2. Ejecutar **2_descarga_srtmgl3.sh** con el fin de descargar datos del proyecto **SRTMGL3**. Vale destacar que para incorporar nuevas consultas solo se deben modificar las rutas en las celdas 99-110 del código.

3. Ejecutar **3_SSTNino34_data.ipynb** para descargar datos de SST promedio en la región Nino 3.4.

## Procesamiento de la información de los parques

En el directorio **venezuela/code** se realiza un estudio general de los porductos **MOD13Q1v6** y **SRTMGL3v3** tomando en cuenta la localización geográfica de Venezuela. Mientras que en las carpetas **cerro_saroche** y **terepaima** se dispone del procesamiento de la información para los parques Cerro Saroche y Terepaima, respectivamente. En ambos casos se parte de la misma estructura:

- **cdsapi**: Repositorio de datos Copernicus.
- **code**: Sección de módulos Python para el precesamiento de la información.
- **data**: Localización de datos .json.
- **figures**: Localización de figuras e imágenes generadas.
- **MOD13Q1_V6**: Repositorio de datos MOD13Q1. 
    - **park_clip**: Datos delimitados según polígono del parque.
    - **summary**: Datos finalizada la revisión de calidad.
- **polygons**: Localización de polígonos del parque.
    - **park**: Polígono del parque.
    - **rectangle**: Polígono de la región delimitada para el parque.
- **SRTMGL3**: Localización de los datos SRTMGL3 según el polígono del parque y regrillado.

El proyecto hace posible replicar el estudio en parques venezolanos distinto al Cerro Saroche y Terepaima siempre que la información este disponible tras la consulta de los productos **MOD13Q1v6** y **SRTMGL3v3** (ver **1_descargar_mod13q1.py** y **2_descarga_srtmgl3.sh**). En este caso solo se debe duplicar la sección **cerro_saroche** o **terepaima** y modificar los módulos en **code** tal que:


1. En los módulos **1_definir_area_cerro_saroche.ipynb** y **2_descargar_cdsapi_data.py** se descarga la información correspondiente al parque (WCMC/WDPA/current/polygons), se define la grilla y se obtiene la información de la precipitación total del producto Copernicus.

2. En los códigos **3_0_mes_mod13q1_cerro_saroche_proceso.py**, **3_1_mod13q1_cerro_saroche_proceso.py** y **3_2_qa_mod13q1_cerro_saroche_proceso.py** se limita la información del NDVI (producto MOD13Q1) al polígono del parque y se realiza el filtrado de calidad según las indicaciones de la NASA.

3. En **4_1_elevacion_terepaima_proceso.py** se realiza el procesamiento de la elevación correspondiente al polígono asociado a la grilla del parque.

4. En el código **5_regrillado_data.ipynb** se realiza el regrillado para la elevación y NDVI del parque.

5. La inserción de los resultados en las colecciones de MongoDB es programado en **6_meteorological_data.ipynb**.

6. En **7_polygon_data.ipynb** se realiza la inserción de los polígonos en MongoDB.
