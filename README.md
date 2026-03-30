# 📋 Construcción de Software - Sistema de Gestión de Tareas y Usuarios

**Curso:** VII Semestre

---

## 📌 Descripción del Proyecto

Sistema integral de gestión de tareas y usuarios desarrollado como práctica de construcción de software. Implementa una arquitectura de cliente-servidor con una API REST robusta en Flask y una interfaz web moderna con validaciones en tiempo real.

### Objetivo
Demostrar habilidades en:
- Desarrollo backend (API REST)
- Integración frontend-backend
- Validación de datos
- Manejo de estados
- Gestión de recursos (CRUD)

---

## 🏗️ Arquitectura y Stack Tecnológico

### Backend
- **Framework:** Flask (Python)
- **Arquitectura:** REST API
- **Almacenamiento:** En memoria (listas Python)
- **Validación:** Expresiones regulares para códigos postales

### Frontend
- **HTML5:** Estructura semántica
- **CSS3:** Diseño responsivo con paleta verde oscuro
- **JavaScript:** Vanilla (sin frameworks)
- **Iconos:** Font Awesome 6.5.1

### Características de Validación
- Códigos postales: Exactamente 5 dígitos (`^\d{5}$`)
- Campos obligatorios en usuarios (nombre, apellido, ciudad, país, código postal)
- Campos obligatorios en tareas (contenido)

---

## 📂 Estructura del Proyecto

```
Construccion_Software/
│
├── app.py                      # Aplicación principal Flask
├── templates/
│   └── index.html              # Interfaz web HTML5
├── static/
│   ├── style.css               # Estilos CSS
│   └── script.js               # Lógica JavaScript
│
└── Contruccion_de_Software/
    ├── back/
    │   └── postman_endpoints.json    # Documentación de endpoints
    └── README.md
```

---

## 🔌 API REST - Endpoints

### Base URL
```
http://127.0.0.1:5000
```

### 📝 **TAREAS**

| # | Método | Endpoint | Descripción |
|---|--------|----------|-------------|
| 1 | `GET` | `/tasks` | Obtener todas las tareas |
| 2 | `GET` | `/tasks/<id>` | Obtener tarea por ID |
| 3 | `POST` | `/tasks` | Crear nueva tarea |
| 4 | `PUT` | `/tasks/<id>` | Actualizar tarea |
| 5 | `DELETE` | `/tasks/<id>` | Eliminar tarea |

**Payload Crear/Actualizar Tarea:**
```json
{
  "content": "Descripción de la tarea",
  "done": false
}
```

#### Ejemplos de Respuesta

**GET /tasks**
```json
{
  "tasks": [
    {
      "id": 1,
      "content": "Completar proyecto",
      "done": false
    },
    {
      "id": 2,
      "content": "Revisar código",
      "done": true
    }
  ]
}
```

**POST /tasks**
```json
{
  "id": 3,
  "content": "Nueva tarea",
  "done": false
}
```

---

### 👥 **USUARIOS**

| # | Método | Endpoint | Descripción |
|---|--------|----------|-------------|
| 1 | `GET` | `/users` | Obtener todos los usuarios |
| 2 | `GET` | `/users/<id>` | Obtener usuario por ID |
| 3 | `POST` | `/users` | Crear nuevo usuario |
| 4 | `PUT` | `/users/<id>` | Actualizar usuario |
| 5 | `DELETE` | `/users/<id>` | Eliminar usuario |

**Payload Crear/Actualizar Usuario:**
```json
{
  "name": "Juan",
  "lastname": "Pérez",
  "address": {
    "city": "Madrid",
    "country": "España",
    "postal_code": "28001"
  }
}
```

**Validaciones:**
- `name`: Requerido (cadena de texto)
- `lastname`: Requerido (cadena de texto)
- `address.city`: Requerido (cadena de texto)
- `address.country`: Requerido (cadena de texto)
- `address.postal_code`: Requerido, exactamente 5 dígitos (`^\d{5}$`)

#### Ejemplos de Respuesta

**GET /users**
```json
{
  "users": [
    {
      "id": 1,
      "name": "Juan",
      "lastname": "Pérez",
      "address": {
        "city": "Madrid",
        "country": "España",
        "postal_code": "28001"
      }
    }
  ]
}
```

**POST /users**
```json
{
  "id": 2,
  "name": "María",
  "lastname": "García",
  "address": {
    "city": "Barcelona",
    "country": "España",
    "postal_code": "08001"
  }
}
```

---

### 🌐 **MISCELÁNEOS**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Página de inicio |
| `GET` | `/about` | Información de la aplicación |
| `GET` | `/hello/<nombre>` | Saludo personalizado |

---

## 🚀 Instalación y Uso

### Requisitos
- Python 3.7 o superior
- Flask (`pip install flask`)

### Pasos de Instalación

1. **Clonar/Navegar al repositorio**
```bash
cd Construccion_Software
```

2. **Instalar dependencias**
```bash
pip install flask
```

3. **Ejecutar la aplicación**
```bash
python app.py
```

4. **Acceder a la aplicación**
- Abrir navegador en: `http://localhost:5000`
- API disponible en: `http://localhost:5000`

---

## ✨ Características Principales

✅ **CRUD Completo** — Crear, leer, actualizar, eliminar tareas y usuarios  
✅ **Validación de Datos** — En tiempo real con expresiones regulares  
✅ **Interfaz Responsiva** — Diseño moderno con paleta verde oscura  
✅ **Modales Interactivos** — Edición de tareas y usuarios en ventanas modales  
✅ **Toggle Show/Hide** — Mostrar/ocultar listas con iconografía Font Awesome  
✅ **Notificaciones** — Mensajes visuales de éxito y error con iconos  
✅ **Gestión Inteligente de IDs** — Reutiliza IDs tras eliminación  
✅ **Integración Frontend-Backend** — Comunicación seamless con API REST  

---

## 🎨 Diseño y UX

### Paleta de Colores
- **Verde Oscuro Principal:** `#1a5030`
- **Verde Secundario:** `#2d8659`
- **Verde Terciario:** `#3da66e`
- **Rojo (Peligro):** `#e74c3c`
- **Gris Neutro:** `#f5f5f5`

### Iconografía
- **Font Awesome 6.5.1** para todos los iconos
- Íconos de estado: check-circle, hourglass-start
- Íconos de acción: edit, trash, eye, eye-slash
- Íconos de mensaje: check-circle, warning

### Elementos UI
- Botones con estados hover
- Animaciones modales (slide-in)
- Alta accesibilidad y contraste

---

## 🔧 Tecnologías Utilizadas

**Backend:**
- Python 3.x
- Flask (microframework web)
- Expresiones regulares (validación)

**Frontend:**
- HTML5 semántico
- CSS3 con Grid y Flexbox
- JavaScript vanilla (ES6+)
- Font Awesome 6.5.1 CDN

**Desarrollo:**
- VS Code
- Git/GitHub

---

## 📋 Notas de Desarrollo

- **Almacenamiento:** En memoria (no persistente)
- **ID Generation:** Usa pattern `max(lista) + 1`
- **CORS:** No implementado (mismo origen)
- **Autenticación:** No implementada
- **Base de Datos:** Para producción, implementar con SQLAlchemy/PostgreSQL

---

## 🚦 Estados HTTP

| Código | Significado |
|--------|-------------|
| `200` | OK - Operación exitosa |
| `201` | Created - Recurso creado |
| `400` | Bad Request - Datos inválidos |
| `404` | Not Found - Recurso no encontrado |
| `500` | Server Error - Error del servidor |

---

## 📚 Ejemplo de Flujo Completo

### 1. Crear un usuario
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pedro",
    "lastname": "López",
    "address": {
      "city": "Valencia",
      "country": "España",
      "postal_code": "46001"
    }
  }'
```

### 2. Crear una tarea
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Revisar código del usuario",
    "done": false
  }'
```

### 3. Actualizar tarea como completada
```bash
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Revisar código del usuario",
    "done": true
  }'
```

### 4. Obtener todas las tareas
```bash
curl -X GET http://localhost:5000/tasks
```

---

## 🐛 Troubleshooting

**Puerto 5000 en uso:**
```bash
lsof -i :5000  # Identificar proceso
kill -9 <PID>  # Terminar proceso
```

**Errores de validación:**
- Verificar que el código postal tenga exactamente 5 dígitos
- Asegurar que todos los campos obligatorios estén completos

**Problemas de iconos:**
- Verificar conexión a internet (Font Awesome CDN)
- Limpiar caché del navegador

---

## 📞 Soporte

Para reportar problemas o sugerencias, abrir un issue en el repositorio.

---

## 📝 Licencia

Proyecto académico - Construcción de Software - VII Semestre

---

## 👨‍💻 Autor

Desarrollado como proyecto práctico del curso Construcción de Software.

**Fecha de creación:** Marzo 2026  
**Última actualización:** Marzo 2026
