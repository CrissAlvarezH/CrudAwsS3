## Descripción
Api REST para listar, subir, descargar y eliminar archivos guardados en Amazon S3. 
Leer archivo .csv guardado en S3 y mostrar sus datos

## Requerimientos
`python 3.8.1` </br>
`django 2.2` </br>
`django rest framework 3.11.0` </br>
`pandas 0.25.3` </br>
`boto3 1.11.9` </br>

## Autenticación
La api usa Basic Authentication

Usuario: `admin` </br>
Email: `admin@email.com` </br>
Contraseña: `admin1234` </br>

## Endpoints

- Subir archivo a AWS S3

    Url: `/files/upload` </br>
    Método: `POST` </br>
    Form data: `file` (tipo file) </br> 
     
- Listar archivos en AWS S3 bucket

    Url: `/files/list` </br>
    Método: `GET` </br>
    
- Descargar archivo de AWS S3

    Url: `/files/download/<nombre del archivo>` </br>
    Método: `GET` 
    
- Eliminar archivo de AWS S3 bucket

    Url: `/files/delete/<nombre del archivo>` </br>
    Método: `DELETE`
    
- Leer y mostrar datos de archivo .csv almacenado en AWS S3

    Url: `/files/data/<nombre del archivo csv>` </br>
    Método: `GET` </br>
    Parámetros: `columns`, `sort`, `asc`
    
    **Ejemplo:** `/files/data/test2.csv?columns=1,3&sort=1&asc=0` 
    > **columns** indica las columnas que desea ver en el reporte separadas por comas (opcional) </br>
    > **sort** son las columnas que desea ordenar separadas por comas (opcional) </br>
    > **asc** Si es mayor que cero se ordenarán ascendentemente, de lo contrario lo harán descendentemente (opcional)
    
    
