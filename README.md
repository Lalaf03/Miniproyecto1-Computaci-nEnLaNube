# 🛒 Sistema de Tienda Online — Microservicios con Docker + Consul

Este proyecto es una aplicación de tienda online construida con arquitectura de microservicios.  
Permite gestionar usuarios, productos y órdenes mediante servicios independientes que se comunican entre sí.

---

## 🚀 Tecnologías utilizadas

- Python + Flask
- MySQL
- Docker y Docker Compose
- Consul (Service Discovery)
- Frontend web (HTML, CSS, JS)

---

## 🏗️ Arquitectura

El sistema está compuesto por los siguientes servicios:

| Servicio        | Descripción                  | Puerto |
|-----------------|------------------------------|---------|
| frontend        | Interfaz web                 | 5001    |
| microUsers      | Gestión de usuarios          | 5002    |
| microProducts   | Gestión de productos         | 5003    |
| microOrders     | Gestión de órdenes           | 5004    |
| consul          | Service Discovery            | 8500    |

Cada microservicio posee su propia base de datos independiente.

---

## ⚙️ Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- Docker
- Docker Compose

Puedes verificarlo con:

```bash
docker --version
docker compose version
```bash

No es necesario instalar dependencias adicionales.

---

## 🚀 Cómo ejecutar el proyecto

### 1️⃣ Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>

### 2️⃣ Iniciar todos los servicios

```bash
docker compose up --build -d

---

## 🌐 Acceso

- Frontend: http://localhost:5001
- Consul: http://localhost:8500

---

###🛑 Detener el sistema

```bash
docker compose down

---

## 🐳 Docker

Cada servicio se ejecuta en su propio contenedor Docker con:

- Dockerfile individual  
- Dependencias aisladas  
- Comunicación interna por nombre de servicio

---

## 🔎 Service Discovery

Se utiliza **Consul** para:

- Registro automático de servicios  
- Descubrimiento dinámico entre microservicios  
- Verificación de estado mediante health checks  
