
# 🗳️ Centro de Votaciones

Este proyecto es un simulador de centro de votación desarrollado en Python con interfaz gráfica usando Tkinter. Permite registrar jurados, controlar asistencia de votantes y generar estadísticas y visualizaciones a partir de archivos de datos.

## 📋 Funcionalidades

- Registro y consulta de jurados por salón y mesa.
- Carga de votantes desde archivo CSV.
- Registro de asistencia (hasta las 4 p.m.).
- Carga de resultados de votación desde archivo CSV o JSON.
- Generación de estadísticas usando `pandas`.
- Visualizaciones de datos con `matplotlib`.

## 📦 Requisitos

Asegúrate de tener Python instalado y luego ejecuta:

pip install pandas matplotlib en la consola de tu ecosistema de python


## 📁 Archivos necesarios
Para que el programa funcione correctamente, deben estar disponibles los siguientes archivos:

votantes.csv: contiene los datos de los votantes con columnas como cedula, salon, mesa, etc.

resultados.csv: contiene los resultados por mesa con respuestas a las preguntas.

Los datos de jurados y su estructura se guardan automáticamente en un archivo JSON desde el programa.
