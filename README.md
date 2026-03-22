# Gestor de Tareas en PyCharm Pro

Aplicación de escritorio desarrollada en **Python con el framework PySide6** para agregar, editar, completar y eliminar tareas con una interfaz gráfica moderna y persistencia local en **JSON**.

> Este proyecto es especial para mí porque fue el **primer sistema completo que desarrollé en PyCharm Professional**, usando la licencia educativa que obtuve como estudiante. También fue mi primer proyecto de escritorio con una interfaz más cuidada, navegación entre vistas y almacenamiento persistente.

<img width="1392" height="944" alt="Captura de pantalla 2026-03-22 a la(s) 03 09 17" src="https://github.com/user-attachments/assets/78d820be-f7cc-4035-b9fd-2438b58d1586" />




---

## Vista general

El sistema fue construido como un gestor de tareas simple, visual y funcional. La aplicación permite:

- agregar tareas
- editar tareas existentes
- eliminar tareas
- marcar tareas como completadas
- guardar automáticamente en `tareas.json`
- cargar las tareas al volver a abrir la aplicación
- mostrar contadores de tareas totales, pendientes y completadas

La interfaz fue diseñada con una estética oscura, paneles semitransparentes, avatar personalizado e imagen de fondo, buscando un resultado más profesional y agradable visualmente.

---

## Tecnologías utilizadas

- **Python 3.14**
- **PySide6** para la interfaz gráfica
- **Qt Style Sheets (QSS)** para el diseño visual
- **JSON** para la persistencia de datos local
- **PyCharm Professional** como entorno de desarrollo

---

## Estructura del proyecto

```text
sistema_gestion/
├── assets/
│   ├── fondo.png
│   └── user.png
├── styles/
│   └── style.qss
├── ui/
│   └── main_window.py
├── main.py
├── tareas.json
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Funcionalidades principales

### 1. Dashboard principal
Muestra un panel de bienvenida con:
- total de tareas
- tareas pendientes
- tareas completadas

### 2. Gestión de tareas
Desde la vista principal de tareas se puede:
- escribir una nueva tarea
- agregarla a la lista
- editar una tarea seleccionada
- eliminar una tarea seleccionada
- completar o descompletar una tarea

### 3. Persistencia local
Cada cambio se guarda automáticamente en `tareas.json`, por lo que el contenido permanece aunque cierres la aplicación.

### 4. Diseño visual
La app usa:
- fondo personalizado
- sidebar oscura
- tarjetas con transparencias
- botones por acción con colores diferenciados
- avatar e imagen personalizada

---

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone <TU-URL-DEL-REPO>
cd sistema_gestion
```

### 2. Crear entorno virtual (opcional, recomendado)

```bash
python -m venv .venv
source .venv/bin/activate
```

En Windows:

```bash
.venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
python main.py
```

---

## Archivo de datos

El sistema utiliza `tareas.json` como almacenamiento local.

Ejemplo:

```json
[
    {
        "texto": "Terminar README del proyecto",
        "completada": false
    },
    {
        "texto": "Subir sistema a GitHub",
        "completada": true
    }
]
```

---

## Qué aprendí con este proyecto

Este proyecto me ayudó a practicar y entender:

- estructuración de un proyecto en carpetas
- desarrollo de interfaces gráficas con PySide6
- separación entre lógica, estilos y assets
- persistencia de datos con JSON
- eventos, señales y slots de Qt
- iteración de diseño y mejora continua
- depuración de errores reales durante el desarrollo

---

## Mejoras futuras posibles

- buscador de tareas
- filtros por estado (todas / pendientes / completadas)
- prioridad por tarea
- fechas y vencimientos
- drag & drop
- exportación a CSV o Excel
- empaquetado a `.exe` / `.app`

---

## Estado del proyecto

**Versión funcional terminada.**

Actualmente el sistema ya cumple con el objetivo principal: ser un gestor de tareas visual, persistente y estable.

---

## Autor

**Joaquín Lorenzo González**

- GitHub: `joagonzalez26`

---

## Nota personal

Quise dejar este proyecto tal como quedó al terminarlo porque representa un punto importante en mi aprendizaje: fue el momento en que pasé de hacer ejercicios sueltos a construir un sistema completo con interfaz, diseño y lógica propia.
