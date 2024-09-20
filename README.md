
# Shopping Cart API

**Shopping Cart API** es una API RESTful desarrollada con FastAPI para gestionar un carrito de la compra. Permite agregar, actualizar y eliminar ítems en el carrito, así como obtener información detallada y generar facturas.

## Índice de Contenidos

1. [Descripción](#descripción)
2. [Características](#características)
3. [Tecnologías Utilizadas](#tecnologías-utilizadas)
4. [Instalación](#instalación)
    - [Prerrequisitos](#prerrequisitos)
    - [Clonar el Repositorio](#clonar-el-repositorio)
    - [Configuración del Entorno Virtual](#configuración-del-entorno-virtual)
    - [Instalar Dependencias](#instalar-dependencias)
    - [Configuración de la Base de Datos](#configuración-de-la-base-de-datos)
    - [Ejecutar Migraciones](#ejecutar-migraciones)
    - [Poblar la Base de Datos](#poblar-la-base-de-datos)
    - [Ejecutar la Aplicación](#ejecutar-la-aplicación)
    - [Usando Docker](#usando-docker)
5. [Modelo de Datos](#modelo-de-datos)
6. [Documentación de la API](#documentación-de-la-api)
    - [Estructura de URLs](#estructura-de-urls)
    - [Descripción de Endpoints](#descripción-de-endpoints)
7. [Gestión de Errores](#gestión-de-errores)
8. [Pruebas Realizadas](#pruebas-realizadas)
9. [Mejoras y Funcionalidades Futuras](#mejoras-y-funcionalidades-futuras)
10. [Contribuciones](#contribuciones)
11. [Licencia](#licencia)
12. [Contacto](#contacto)

---

## Descripción

**Shopping Cart API** es una solución completa para gestionar carritos de compra en aplicaciones de comercio electrónico. Permite a los usuarios agregar productos y eventos al carrito, actualizar cantidades, eliminar ítems y obtener resúmenes detallados del carrito, incluyendo subtotales y facturas.

---

## Características

- **Agregar Ítems al Carrito**: Añade productos o eventos con cantidades específicas.
- **Actualizar Cantidades**: Modifica la cantidad de un ítem en el carrito o lo elimina si la cantidad es cero.
- **Eliminar Ítems**: Remueve ítems específicos del carrito.
- **Obtener Resumen del Carrito**: Recupera todos los ítems en el carrito junto con el total de cantidad y precio.
- **Generar Facturas**: Obtiene una factura detallada del carrito.
- **Gestión de Stock**: Actualiza el stock de los ítems al agregar o eliminar del carrito.
- **Validación de Datos**: Utiliza Pydantic para asegurar la integridad de los datos.
- **Documentación Automática**: Disponible a través de Swagger UI y Redoc.

---

## Tecnologías Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web de alto rendimiento para construir APIs con Python.
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: ORM para manejar la base de datos.
- **[Pydantic](https://pydantic-docs.helpmanual.io/)**: Validación de datos y esquemas.
- **[PostgreSQL](https://www.postgresql.org/)**: Sistema de gestión de bases de datos relacional.
- **[Alembic](https://alembic.sqlalchemy.org/en/latest/)**: Herramienta para gestionar migraciones de la base de datos.
- **[Docker](https://www.docker.com/)**: Contenedorización de la aplicación para facilitar el despliegue.
- **[Pytest](https://docs.pytest.org/en/7.1.x/)**: Framework para pruebas automatizadas.

---

## Instalación

### Prerrequisitos

Antes de comenzar, asegúrate de tener instalados los siguientes componentes:

- Python 3.9+
- PostgreSQL
- Docker y Docker Compose (opcional, pero recomendado para contenerización)
- Git

### Configuración del Entorno Virtual

Crea y activa un entorno virtual para aislar las dependencias del proyecto:

```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scriptsctivate  # En Windows
```

### Instalar Dependencias

Instala todas las dependencias del proyecto usando pip:

```bash
pip install -r requirements.txt
```

### Configuración de la Base de Datos

Configura las variables de entorno necesarias para la conexión a la base de datos PostgreSQL. Puedes usar el archivo `.env` en la raíz del proyecto como plantilla para definir estas variables.

### Ejecutar Migraciones

Aplica las migraciones de la base de datos para crear las tablas necesarias:

```bash
alembic upgrade head
```

### Poblar la Base de Datos

Puedes poblar la base de datos con datos de prueba ejecutando el script `seed.py`:

```bash
python seed.py
```

### Ejecutar la Aplicación

Inicia la aplicación con Uvicorn:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

### Usando Docker

Si prefieres usar Docker, puedes contenedorizar la aplicación y la base de datos usando Docker Compose. Ejecuta lo siguiente para iniciar ambos servicios:

```bash
docker-compose up --build
```

---

## Modelo de Datos

El modelo de datos está compuesto por las siguientes clases de SQLAlchemy:

- **Item**: Clase base que contiene los atributos compartidos por productos y eventos.
- **Product**: Hereda de `Item` y representa productos físicos con instrucciones de cuidado.
- **Event**: Hereda de `Item` y representa eventos con una fecha específica.
- **Cart**: Representa el carrito de compras que contiene ítems.
- **CartItem**: Relaciona un ítem con un carrito, con una cantidad específica.

---

## Documentación de la API

La API sigue los principios de RESTful y tiene la siguiente estructura de URLs:

### Estructura de URLs

| Método | Endpoint          | Descripción                                   |
|--------|-------------------|-----------------------------------------------|
| POST   | `/cart/items/`     | Agrega un ítem al carrito.                    |
| PUT    | `/cart/items/{id}` | Actualiza la cantidad de un ítem en el carrito.|
| DELETE | `/cart/items/{id}` | Elimina un ítem del carrito.                  |
| GET    | `/cart/`           | Obtiene el carrito actual.                    |
| GET    | `/cart/invoice/`   | Obtiene la factura detallada del carrito.     |

### Descripción de Endpoints

- **Agregar Ítem al Carrito**: Permite añadir productos o eventos al carrito especificando el `item_id` y la cantidad.
- **Actualizar Cantidad de Ítem**: Permite modificar productos o eventos al carrito especificando el `item_id` y la cantidad. Si la cantidad es 0, el ítem será eliminado del carrito.
- **Eliminar Ítem**: Remueve un ítem específico del carrito.
- **Obtener el Carrito**: Devuelve el contenido actual del carrito con el total de cantidad y precio.
- **Obtener la Factura**: Retorna un resumen detallado de cada ítem en el carrito, incluyendo subtotales y el precio total.

---

## Gestión de Errores

La API maneja errores comunes a través de excepciones personalizadas:

- **ItemNotFoundException**: Se lanza cuando un ítem solicitado no existe.
- **OutOfStockException**: Se lanza cuando no hay suficiente stock disponible para un ítem.
- **InvalidQuantityException**: Se lanza cuando la cantidad ingresada es inválida (por ejemplo, negativa).

Todos los errores se devuelven con un código de estado HTTP y un mensaje descriptivo.

---

## Pruebas Realizadas

Las pruebas unitarias se realizaron usando Pytest para verificar la funcionalidad de los siguientes casos:

- Agregar un ítem al carrito.
- Actualizar la cantidad de un ítem.
- Eliminar un ítem del carrito.
- Obtener el contenido del carrito.
- Validar que no se pueden agregar ítems sin stock suficiente.

Para ejecutar las pruebas:

```bash
pytest
```

---

## Mejoras y Funcionalidades Futuras

- **Autenticación**: Implementar un sistema de autenticación para que cada usuario tenga su propio carrito.
- **Descuentos**: Agregar la funcionalidad de aplicar cupones de descuento.
- **Notificaciones**: Enviar notificaciones cuando un producto esté fuera de stock.
- **Historial de Compras**: Guardar un historial de las compras realizadas por cada usuario.

---

## Contacto

**Jhulian Ramírez**  
Para cualquier consulta o sugerencia, puedes contactarme a través de:

- **Correo Electrónico**: [ramirezjhulian7@gmail.com](mailto:ramirezjhulian7@gmail.com)  
- **LinkedIn**: [jhulianramirez](https://www.linkedin.com/in/jhulianramirez/)
- **Git**: [jhulianramirez](https://github.com/ramirezjhulian7/shopping_cart_api)

![Shopping Cart API](Swagger.png)