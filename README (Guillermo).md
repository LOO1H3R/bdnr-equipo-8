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

### Setup a python virtual env with python dgraph installed
```
# If pip is not present in you system
sudo apt update
sudo apt install python3-pip

# Install and activate virtual env
python3 -m pip install virtualenv
python3 -m venv ./venv
source ./venv/bin/activate

# Install project python requirements
python3 -m pip install -r "/home/guillermoclinux/bdnr-equipo-8/requirements.txt"
```

## Herramientas a utilizar

Para la implementación de este proyecto se hará uso de los motores de **Cassandra**, **MongoDB** y **DGraph**. Las instrucciones para ejecutar este proyecto se encuentran a continuación.

  2. **Mongo DB Modelo 2**

cd "/home/guillermoclinux/bdnr-equipo-8/MongoDB Model 3"

### To run the API service
```
python3 -m uvicorn main:app --reload
```

# To start a new container
docker run --name mongodbModelo2 -d -p 27017:27017 mongo

# If container already exists just start it
docker start mongodbModelo2

# Once your API service is running (see step above), run the populate script
```
cd MongoDB Model 2/
python3 populate.py
```

### Iniciar una instancia en docker

  3. **Cassandra Modelo 3**
  ```
# To start a new container
docker run --name node03 -p 9042:9042 -d cassandra

# If container already exists just start it
docker start node03
```
# Copy data to container
```
docker cp /home/guillermoclinux/bdnr-equipo-8/Cassandra\ Model\ 2/datos_pasajero_vuelo.cql node03:/root/
docker cp /home/guillermoclinux/bdnr-equipo-8/Cassandra\ Model\ 2/rutas_menos_transitadas.cql node03:/root/
docker exec -it node03 bash -c "cqlsh -u cassandra -p cassandra"
# In cqlsh:
USE promociones_vuelos;
SOURCE '/root/datos_pasajero_vuelo.cql'
SOURCE '/root/rutas_menos_transitadas.cql'
exit
```



  3. **DGraph**
```
# To start a new container (dgraph)
docker run --name dgraph -d -p 8080:8080 -p 9080:9080  dgraph/standalone:latest

# To start a new container (ratel)
docker run --name ratel -d -p 8000:8000 dgraph/ratel:latest
```



