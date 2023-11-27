# bdnr-equipo-8

Este es el proyecto final del equipo 8 para la materia de bases de datos no relacionales en el curso de otoño 2023.

## Descripción del proyecto

El proyecto consiste en modelar e implementar soluciones por medio del uso de bases NoSQL, el escenario planteado se presenta como el siguiente:

> As a marketing and consulting company, we have access to the following data. We need to solve specific business questions, and leverage this data to create new business opportunities for us and our customers.

Los modelos a implementar son:
1. Modelo que mencione cuales son los meses que es recomendable introducir campaña de publicidad para empresas de renta de carros para cada aeropuerto.
2. Modelo que recomiende en que aeropuertos es recomendable abrir servicios de alimentos/bebidas.
3. Modelo de selección de promociones para rutas poco transitada
4. Modelo de recolección de datos para industria hotelera.

## Herramientas a utilizar

Para la implementación de este proyecto se hará uso de los motores de **Cassandra**, **MongoDB** y **DGraph**. Las instrucciones para ejecutar este proyecto se encuentran a continuación.

### Iniciar una instancia en docker

  1. **Cassandra**
  ```
# To start a new container
docker run --name car_rental -p 9042:9042 -d cassandra

# If container already exists just start it
docker start node01

# To copy data
docker cp data.cql car_rental:/root/data.cql
```
  2. **MongoDB**
```
# To start a new container
docker run --name mongodb -d -p 27017:27017 mongo

# If container already exists just start it
docker start mongodb
```
  3. **DGraph**
```
# To start a new container (dgraph)
docker run --name dgraph -d -p 8080:8080 -p 9080:9080  dgraph/standalone:latest

# To start a new container (ratel)
docker run --name ratel -d -p 8000:8000 dgraph/ratel:latest
```

