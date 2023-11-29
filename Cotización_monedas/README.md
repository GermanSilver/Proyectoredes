# Cotizador
Este proyecto está desarrollado en Python.
Utiliza varias bibliotecas en Python para su funcionamiento:
socket
requests
lxml (etree, html)
DatabaseHelper (Clase incluida en la carpeta del proyecto)
datetime (datetime, timedelta).

Para utilizar este programa se debe descargar la carpeta contenedora y mantener los archivos dentro de ella.
Crear la Base de datos a partir del archivo moneda.sql.

Se ejcuta desde Main_Cotizaciones.py

Este programa descarga del BCRA cotizaciones desde 2013 y permite consulta de cotizaciones por fecha de las monedas US Dolar, Real, Peso argentino y Peso chileno.
Además, cuenta con la posibilidad de contestar consultas externas a traves del servidor (se debe ejecutar Cliente_Cotizaciones.py).

Funciones incluidas en su menú
-------------------------
      *** Menú ***
-------------------------
| Carga de datos: 
| 1. Histórico
## Restablece el histórico de cotizaciones en la BD.
| 2. Actualización
## Actualiza las cotizaciones a la fecha actual en la BD.
| Consultas:
| 3. Fecha específica
## Consulta la cotización de una moneda en una fecha puntual.
| 4. Por rango de fechas
## Consulta la cotización de una moneda durante un período.
| 5. Variación entre fechas
## Consulta la variación en la cotizacón de una moneda durante un período.
| 6. Atender cliente externo
## Abre la conexión del servidor para gestionar una consulta externa de cotizacón.
| 0. Salir
## Permite salir del programa.
-------------------------
