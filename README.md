# Chatbot de Administracion de Vacaciones - Python

Trabajo práctico integrador de Organización Empresarial.

## Archivos

- `main.py`: programa principal en Python.
- `empleados.csv`: archivo que simula la base de datos de empleados.

## Cómo ejecutar en Visual Studio

1. Abrí la carpeta del proyecto.
2. Abrí `main.py`.
3. Ejecutalo con el botón Run o con `python main.py`.

No hay que instalar ninguna librería externa. El programa usa el módulo `csv`, que ya viene con Python.

## Datos para probar

| DNI | Nombre | Días disponibles |
| --- | --- | ---: |
| 30111222 | Ana Perez | 15 |
| 28444555 | Bruno Diaz | 4 |
| 32999888 | Carla Gomez | 0 |

## Opciones del menú

1. Solicitar vacaciones: inicia la conversación con el chatbot.
2. Ver solicitudes: muestra las solicitudes ordenadas por nombre.
3. Revisar solicitud: Recursos Humanos aprueba o rechaza; si aprueba, se actualizan los días en `empleados.csv`.
4. Ver estadísticas: total de solicitudes aprobadas, rechazadas y pendientes.
5. Salir.

## Conceptos aplicados

- Listas y diccionarios.
- Funciones.
- Condicionales `if`, `elif` y `else`.
- Ciclos `while` y `for`.
- Ordenamiento con `sorted`.
- Estadísticas básicas mediante contadores.
