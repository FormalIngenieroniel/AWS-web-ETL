# Arquitectura de Datos Analítica en AWS para Sakila

## Introducción

Este proyecto se enfoca en el desarrollo de una arquitectura de datos analítica en AWS para la base de datos Sakila, con el objetivo principal de crear y gestionar procesos ETL (Extract, Transform, Load) en AWS Glue. La arquitectura está diseñada para poblar un Data Lake en S3 con un modelo dimensional, manejar datos incrementales, construir una tabla de hechos mediante transformaciones SQL, y generar una tabla de dimensiones de fecha utilizando lógica Python.

La empresa de alquiler de películas Sakila busca implementar un sistema de data lake en S3, donde todos los datos se almacenarán en formato Parquet y serán accesibles para visualización y análisis a través de AWS Athena.

## Modelo Dimensional

La arquitectura implementa el siguiente modelo dimensional:

![img-0.jpeg](img-0.jpeg)

## ¿Cómo Funciona?

El sistema funciona a través de una serie de procesos ETL automatizados y una aplicación web modificada, garantizando que los datos del sistema de análisis se mantengan actualizados.

1.  **Ingesta Incremental de Dimensiones**: ETLs de AWS Glue mueven datos de las tablas `Film`, `Customer` y `Store` de RDS Sakila a sus respectivas tablas dimensionales en S3 de manera incremental diariamente.
2.  **Construcción de la Tabla de Hechos**: Un ETL en AWS Glue combina datos de `customer`, `film`, `rental` y `store` para poblar la tabla de hechos `Fact Sales`. Se utiliza una transformación SQL dentro del ETL para realizar la consulta con `JOIN` y definir `Date_sales_id` como un entero (ej: `2005-12-01` se convierte en `20051201`).
3.  **Generación de la Dimensión de Fecha**: Un ETL en AWS Glue con un script de Python se encarga de llenar la tabla `Date_sales`. Este script incluye lógica para determinar el trimestre del año, si la fecha es día de semana o fin de semana, y si es un día festivo en Estados Unidos.
4.  **Catalogación de Datos**: Se crean Crawlers de AWS Glue para detectar el esquema de los archivos Parquet en S3 y registrarlos en el Catálogo de Datos de Glue, haciendo los datos disponibles para Athena.
5.  **Flujos de Trabajo (Workflows)**: Se establecen Workflows en AWS Glue para orquestar la ejecución de los Jobs ETL y los Crawlers, asegurando un orden y una dependencia correctos.
6.  **Actualización de Datos**: Los ETLs están configurados para mantener los datos del sistema de análisis actualizados a medida que se ingresan nuevas transacciones.
7.  **Aplicación Web**: La aplicación web desarrollada previamente se ha modificado para permitir el registro de nuevas rentas, insertando los datos directamente en la base de datos Sakila. Esta funcionalidad incluye la selección de la película de una lista desplegable, la fecha y el documento del cliente.

## Componentes y Tecnologías Clave

*   **AWS Glue**: Servicio principal para la creación y ejecución de los procesos ETL.
    *   **Jobs ETL**: Scripts (Python y SQL) que realizan las transformaciones y movimientos de datos.
    *   **Crawlers**: Herramientas para inferir esquemas y actualizar el Catálogo de Datos de Glue.
    *   **Workflows**: Orquestación de Jobs y Crawlers.
*   **Amazon S3**: Data Lake para el almacenamiento de datos en formato Parquet.
*   **AWS Athena**: Servicio de consulta interactiva para analizar los datos en S3 utilizando SQL estándar.
*   **Amazon RDS (Sakila DB)**: Base de datos transaccional origen para la ingesta de datos.
*   **Python**: Utilizado para la lógica compleja en los scripts ETL, especialmente para la dimensión de fecha.
*   **SQL**: Utilizado para transformaciones de datos dentro de los ETLs, particularmente para la tabla de hechos.
*   **Despliegue Continuo (CI/CD)**: La arquitectura completa está diseñada para un despliegue continuo con pruebas unitarias. Los jobs se gestionan como archivos en S3, y toda la infraestructura puede ser creada y gestionada mediante `boto3`.

## Requisitos Funcionales

*   **ETL Incremental de Dimensiones**: Crear ETLs en AWS Glue para mover datos de `Film`, `Customer`, `Store` de RDS Sakila a S3 incrementalmente.
*   **ETL de Tabla de Hechos**: Crear un ETL en AWS Glue que combine `customer`, `film`, `rental` y `store` en `Fact Sales`, utilizando la opción `transform SQL` y un `Date_sales_id` entero (YYYYMMDD).
*   **ETL de Dimensión de Fecha**: Desarrollar un ETL en AWS Glue con un script de Python para llenar la tabla `Date_sales`, incluyendo trimestre, día de la semana/fin de semana y si es festivo en EE. UU.
*   **Crawlers y Workflows**: Configurar Crawlers para los esquemas y Workflows para la ejecución secuencial de Jobs y Crawlers.
*   **Modificación de Aplicación Web**: Actualizar la aplicación web existente para permitir nuevas rentas, ingresando fecha, documento del cliente y película seleccionada.
*   **Actualización de Datos**: Asegurar que todos los ETLs mantengan los datos analíticos actualizados con los nuevos ingresos.
*   **Despliegue Continuo**: Toda la arquitectura debe ser compatible con despliegue continuo y pruebas unitarias, con jobs almacenados en S3 y la infraestructura gestionable vía `boto3`.
