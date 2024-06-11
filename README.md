# Mapa interactivo de descuentos en restaurantes con tarjetas de crédito en Chile 🇨🇱

Esta app muestra en un mapa interactivo los descuentos en restaurantes que ofrecen los bancos en Chile al pagar con sus respectivas tarjetas.

La app georeferencia restaurantes disponibles a partir de tu ubicación actual. 

Listado de bancos disponibles en el mapa:
- Banco Scotiabank

## Estructura del Proyecto

El proyecto consta de dos partes principales ya preconstruidas:

- `frontend`: Una aplicación Vue.js que muestra los descuentos en un mapa interactivo.
- `backend`: Una API Flask que proporciona los datos de los descuentos.

Además, se incluye un script de Python opcional que se utilizó para hacer el scraping de la web y generar el archivo JSON que el backend sirve al frontend. Este script no es necesario para ejecutar la aplicación, ya que los datos ya se incluyen en la imagen del backend en Docker.

## Cómo ejecutar el proyecto

Para ejecutar el proyecto, necesitarás tener docker y docker-compose instalados en tu máquina.

1. Clona el repositorio:
```bash
git clone https://github.com/gcuriqueo/map-descuentos-chile.git
cd map-descuentos-chile
```

2. Construye las imágenes y levanta los contenedores:
```bash
docker-compose up
```

Una vez iniciado los servicios, podrás acceder a la aplicación Vue.js en localhost:8080 y a la API Flask en localhost:8100.