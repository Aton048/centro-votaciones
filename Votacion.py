import tkinter as tk
from tkinter import messagebox
import pandas as pd
import csv
import json
from tkinter import filedialog
from datetime import datetime
import matplotlib.pyplot as plt
# Lista global para almacenar la información de los jurados
jurados_data = []
votantes_data = []
asistencias_data = []
resultados_votacion = []

def cargar_resultados_votacion():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV/JSON", "*.csv *.json")])
    if not archivo:
        return

    try:
        if archivo.endswith(".csv"):
            with open(archivo, newline='', encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    resultados_votacion.append({
                        "salon": row["salon"],
                        "mesa": row["mesa"],
                        "tarjeton": row["tarjeton"],
                        "preguntas": [row[f"p{i}"] for i in range(1, 10)]
                    })

        elif archivo.endswith(".json"):
            with open(archivo, encoding="utf-8") as f:
                data = json.load(f)
                for r in data:
                    resultados_votacion.append({
                        "salon": r["salon"],
                        "mesa": r["mesa"],
                        "tarjeton": r["tarjeton"],
                        "preguntas": r["preguntas"]
                    })

        messagebox.showinfo("Éxito", f"Se cargaron {len(resultados_votacion)} resultados correctamente.")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")


def guardar_jurados_csv():
    if not jurados_data:
        messagebox.showinfo("Sin datos", "No hay datos de jurados para guardar.")
        return

    try:
        df = pd.DataFrame(jurados_data, columns=["Salón", "Mesa", "Jurado", "Nombre", "Cédula", "Teléfono", "Dirección"])
        df.to_csv("jurados.csv", index=False)
        messagebox.showinfo("Guardado", "Datos guardados en 'jurados.csv'.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

def cargar_jurados_csv():
    global jurados_data
    try:
        df = pd.read_csv("jurados.csv")
        jurados_data = df.values.tolist()
        messagebox.showinfo("Cargado", "Datos cargados desde 'jurados.csv'.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo 'jurados.csv'.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")



def generar_centro_votacion():
    """Genera la estructura visual del centro de votación basado en los valores ingresados"""

    # Validar entradas
    try:
        salones = int(entry_salones.get())
        mesas_por_salon = int(entry_mesas.get())
        jurados_por_mesa = int(entry_jurados.get())

        if salones <= 0 or mesas_por_salon <= 0 or jurados_por_mesa <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Entrada inválida", "Por favor, ingresa solo números enteros positivos.")
        return

    # Limpiar la ventana de simulaciones previas
    for widget in frame_centro_votacion.winfo_children():
        widget.destroy()

    # Generar estructura de botones
    global jurados_data
    jurados_data = []  # Reiniciar la lista de datos de jurados

    jurado_id = 0  # Un contador único para jurados
    for salon in range(1, salones + 1):
        # Crear un marco para cada salón
        frame_salon = tk.LabelFrame(frame_centro_votacion, text=f"Salón {salon}", padx=10, pady=5)
        frame_salon.pack(padx=10, pady=5, fill="x")

        for mesa in range(1, mesas_por_salon + 1):
            # Crear un marco para cada mesa dentro del salón
            frame_mesa = tk.Frame(frame_salon)
            frame_mesa.pack(padx=5, pady=5)

            # Botón para la mesa
            mesa_num = f"Salón {salon} - Mesa {mesa}"
            tk.Button(frame_mesa, text=f"{mesa_num}", command=lambda m=mesa_num: consultar_jurados(m)).pack(side="left")

            # Crear botones para los jurados
            for jurado in range(1, jurados_por_mesa + 1):
                jurado_id += 1
                tk.Button(frame_mesa, text=f"Jurado {jurado}",
                          command=lambda sid=salon, mid=mesa, jid=jurado: registrar_jurado(sid, mid, jid)).pack(
                    side="left")



def guardar_datos_json():
    """Guarda la estructura completa del centro de votación en un archivo JSON"""
    try:
        salones = int(entry_salones.get())
        mesas = int(entry_mesas.get())
        jurados = int(entry_jurados.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa correctamente los números de salones, mesas y jurados.")
        return

    datos_guardar = {
        "salones": salones,
        "mesas_por_salon": mesas,
        "jurados_por_mesa": jurados,
        "jurados_registrados": [
            {
                "salon": j[0],
                "mesa": j[1],
                "jurado_numero": j[2],
                "nombre": j[3],
                "cedula": j[4],
                "telefono": j[5],
                "direccion": j[6],
            }
            for j in jurados_data
        ]
    }

    archivo = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if archivo:
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(datos_guardar, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Éxito", f"Datos guardados exitosamente en {archivo}")
        except Exception as e:
            messagebox.showerror("Error al guardar", f"No se pudieron guardar los datos: {e}")

def registrar_jurado(salon, mesa, jurado):
    """Abre un formulario para registrar los datos del jurado"""

    def guardar_datos():
        # Recuperar los datos ingresados
        nombre = entry_nombre.get()
        cedula = entry_cedula.get()
        telefono = entry_telefono.get()
        direccion = entry_direccion.get()

        # Validar campos vacíos
        if not all([nombre.strip(), cedula.strip(), telefono.strip(), direccion.strip()]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Guardar la información en la lista global
        jurados_data.append((salon, mesa, jurado, nombre, cedula, telefono, direccion))
        messagebox.showinfo("Éxito", "Datos del jurado guardados correctamente.")
        ventana_jurado.destroy()

    # Crear una nueva ventana para el formulario
    ventana_jurado = tk.Toplevel(root)
    ventana_jurado.title(f"Registrar Jurado {jurado} - Mesa {mesa} - Salón {salon}")

    tk.Label(ventana_jurado, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    entry_nombre = tk.Entry(ventana_jurado)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(ventana_jurado, text="Cédula:").grid(row=1, column=0, padx=5, pady=5)
    entry_cedula = tk.Entry(ventana_jurado)
    entry_cedula.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(ventana_jurado, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5)
    entry_telefono = tk.Entry(ventana_jurado)
    entry_telefono.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(ventana_jurado, text="Dirección:").grid(row=3, column=0, padx=5, pady=5)
    entry_direccion = tk.Entry(ventana_jurado)
    entry_direccion.grid(row=3, column=1, padx=5, pady=5)

    # Botón para guardar
    tk.Button(ventana_jurado, text="Guardar", command=guardar_datos).grid(row=4, columnspan=2, pady=10)


def consultar_jurados(mesa):
    """Muestra un reporte de los jurados registrados en la mesa seleccionada"""
    # Filtrar los datos de los jurados para la mesa dada
    jurados_en_mesa = [j for j in jurados_data if f"Salón {j[0]}" in mesa and f"Mesa {j[1]}" in mesa]

    if not jurados_en_mesa:
        messagebox.showinfo("Información", "No hay jurados registrados en esta mesa.")
        return

    # Construir el mensaje con la información de los jurados
    detalle = "\n".join(
        [f"Jurado {j[2]}: {j[3]}, Cédula: {j[4]}, Teléfono: {j[5]}, Dirección: {j[6]}" for j in jurados_en_mesa])
    messagebox.showinfo(f"Jurados en {mesa}", detalle)

def cargar_votantes_csv():
    global votantes_data
    votantes_data = []  # Limpiamos cualquier dato previo

    ruta_archivo = filedialog.askopenfilename(
        title="Selecciona el archivo de votantes",
        filetypes=[("CSV files", "*.csv")]
        )

    if not ruta_archivo:
        return  # Usuario canceló

    try:
        with open(ruta_archivo, newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                    votantes_data.append(fila)
        messagebox.showinfo("Éxito", f"{len(votantes_data)} votantes cargados correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo.\n{e}")

def registrar_asistencia():
    def guardar_asistencia():
        cedula = entry_cedula.get().strip()
        salon = entry_salon.get().strip()
        mesa = entry_mesa.get().strip()
        hora = entry_hora.get().strip()

        if not all([cedula, salon, mesa, hora]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            hora_votacion = datetime.strptime(hora, "%H:%M")
            limite = datetime.strptime("16:00", "%H:%M")
            if hora_votacion > limite:
                messagebox.showerror("Error", "La hora de votación no puede ser posterior a las 4:00 p.m.")
                return
        except ValueError:
            messagebox.showerror("Error", "Formato de hora inválido. Usa HH:MM (ej. 15:30).")
            return

        asistencias_data.append({
            "cedula": cedula,
            "salon": salon,
            "mesa": mesa,
            "hora": hora
        })
        messagebox.showinfo("Éxito", "Asistencia registrada correctamente.")
        ventana_asistencia.destroy()

    ventana_asistencia = tk.Toplevel(root)
    ventana_asistencia.title("Registrar Asistencia")

    tk.Label(ventana_asistencia, text="Cédula:").grid(row=0, column=0, padx=5, pady=5)
    entry_cedula = tk.Entry(ventana_asistencia)
    entry_cedula.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(ventana_asistencia, text="Salón:").grid(row=1, column=0, padx=5, pady=5)
    entry_salon = tk.Entry(ventana_asistencia)
    entry_salon.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(ventana_asistencia, text="Mesa:").grid(row=2, column=0, padx=5, pady=5)
    entry_mesa = tk.Entry(ventana_asistencia)
    entry_mesa.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(ventana_asistencia, text="Hora (HH:MM):").grid(row=3, column=0, padx=5, pady=5)
    entry_hora = tk.Entry(ventana_asistencia)
    entry_hora.grid(row=3, column=1, padx=5, pady=5)

    tk.Button(ventana_asistencia, text="Registrar", command=guardar_asistencia).grid(row=4, columnspan=2, pady=10)

def mostrar_resumen_estadistico():
    try:
        # DataFrames base
        df_jurados = pd.DataFrame(jurados_data, columns=["salon", "mesa", "jurado", "nombre", "cedula", "telefono", "direccion"])
        df_asistencia = pd.DataFrame(asistencia_votantes)
        df_resultados = pd.DataFrame(resultados_votacion)

        resumen = ""

        # Total de jurados y votantes por salón
        total_j_por_salon = df_jurados.groupby("salon")["jurado"].count()
        total_v_por_salon = df_asistencia.groupby("salon")["cedula"].count()
        resumen += "📌 Total de jurados por salón:\n"
        resumen += total_j_por_salon.to_string() + "\n\n"
        resumen += "📌 Total de votantes por salón:\n"
        resumen += total_v_por_salon.to_string() + "\n\n"

        # Jurados registrados por mesa
        jurados_por_mesa = df_jurados.groupby(["salon", "mesa"])["jurado"].count()
        resumen += "📌 Jurados registrados por mesa:\n"
        resumen += jurados_por_mesa.to_string() + "\n\n"

        # Porcentaje de mesas con todos los jurados (suponiendo 3 jurados por mesa)
        mesas_totales = df_jurados.groupby(["salon", "mesa"])["jurado"].count().reset_index()
        completas = mesas_totales[mesas_totales["jurado"] >= 3]
        porcentaje_completas = (len(completas) / len(mesas_totales)) * 100
        resumen += f"📌 Porcentaje de mesas con jurados completos: {porcentaje_completas:.2f}%\n\n"

        # Resumen de resultados: número de "Sí" y "No" por pregunta
        if not df_resultados.empty:
            resumen += "📌 Resultados de votación por pregunta:\n"
            for i in range(9):
                conteo = pd.Series([r[i] for r in df_resultados["preguntas"]]).value_counts()
                resumen += f"Pregunta {i+1}: {conteo.to_dict()}\n"

        # Mostrar en ventana
        ventana_resumen = tk.Toplevel(root)
        ventana_resumen.title("Resumen Estadístico")
        text_box = tk.Text(ventana_resumen, wrap="word", width=100, height=30)
        text_box.insert("1.0", resumen)
        text_box.pack(padx=10, pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el resumen: {e}")

def generar_graficos():
    try:
        df_jurados = pd.DataFrame(jurados_data, columns=["salon", "mesa", "jurado", "nombre", "cedula", "telefono", "direccion"])
        df_asistencia = pd.DataFrame(asistencia_votantes)
        df_resultados = pd.DataFrame(resultados_votacion)

        # 1. Gráfico de barras: jurados, votantes y asistencias por salón
        jurados_salon = df_jurados.groupby("salon")["jurado"].count()
        votantes_salon = df_asistencia.groupby("salon")["cedula"].count()

        salones = list(set(df_jurados["salon"]) | set(df_asistencia["salon"]))
        salones.sort()
        jurados = [jurados_salon.get(s, 0) for s in salones]
        votantes = [votantes_salon.get(s, 0) for s in salones]

        x = range(len(salones))
        plt.figure(figsize=(10, 6))
        plt.bar(x, jurados, width=0.3, label="Jurados")
        plt.bar([i + 0.3 for i in x], votantes, width=0.3, label="Votantes")
        plt.xticks([i + 0.15 for i in x], salones)
        plt.title("Jurados y Votantes por Salón")
        plt.legend()
        plt.tight_layout()
        plt.show()

        # 2. Gráfico de pastel: mesas completas vs incompletas
        mesas_totales = df_jurados.groupby(["salon", "mesa"])["jurado"].count().reset_index()
        completas = mesas_totales[mesas_totales["jurado"] >= 3]
        incompletas = len(mesas_totales) - len(completas)
        plt.figure()
        plt.pie([len(completas), incompletas], labels=["Completas", "Incompletas"], autopct='%1.1f%%')
        plt.title("Proporción de Mesas con Jurados Completos")
        plt.show()

        # 3. Gráfico de pastel: asistencia vs no asistencia
        cedulas_asistencia = set(df_asistencia["cedula"])
        total_votantes = len(set(cedulas_asistencia))  # puedes cambiar si tienes un total conocido
        asistieron = len(cedulas_asistencia)
        no_asistieron = max(total_votantes - asistieron, 0)
        plt.figure()
        plt.pie([asistieron, no_asistieron], labels=["Asistieron", "No asistieron"], autopct='%1.1f%%')
        plt.title("Proporción de Asistencia de Votantes")
        plt.show()

        # 4. Barras horizontales por pregunta
        if not df_resultados.empty:
            preguntas_resumen = {f"Pregunta {i+1}": {"Sí": 0, "No": 0} for i in range(9)}
            for res in df_resultados["preguntas"]:
                for i, val in enumerate(res):
                    if val in preguntas_resumen[f"Pregunta {i+1}"]:
                        preguntas_resumen[f"Pregunta {i+1}"][val] += 1

            preguntas = list(preguntas_resumen.keys())
            si = [preguntas_resumen[p]["Sí"] for p in preguntas]
            no = [preguntas_resumen[p]["No"] for p in preguntas]

            y = range(len(preguntas))
            plt.figure(figsize=(10, 6))
            plt.barh(y, si, color='green', label='Sí')
            plt.barh(y, no, left=si, color='red', label='No')
            plt.yticks(y, preguntas)
            plt.xlabel("Cantidad de Respuestas")
            plt.title("Respuestas por Pregunta")
            plt.legend()
            plt.tight_layout()
            plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron generar los gráficos: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Centro de Votación")

# Marco para las entradas iniciales
frame_inputs = tk.Frame(root)
frame_inputs.pack(padx=10, pady=10)


tk.Button(frame_inputs, text="Guardar Jurados", command=guardar_jurados_csv).grid(row=4, column=0, pady=5)
tk.Button(frame_inputs, text="Cargar Jurados", command=cargar_jurados_csv).grid(row=4, column=1, pady=5)
tk.Button(frame_inputs, text="Guardar en JSON", command=guardar_datos_json).grid(row=4, columnspan=2, pady=5)
tk.Button(frame_inputs, text="Cargar Votantes CSV", command=cargar_votantes_csv).grid(row=5, columnspan=2, pady=5)

tk.Button(frame_inputs, text="Registrar Asistencia", command=registrar_asistencia).grid(row=6, columnspan=2, pady=5)

tk.Button(frame_inputs, text="Cargar Resultados", command=cargar_resultados_votacion).grid(row=7, columnspan=2, pady=5)

tk.Button(frame_inputs, text="Resumen Estadístico", command=mostrar_resumen_estadistico).grid(row=8, columnspan=2, pady=5)

tk.Button(frame_inputs, text="Generar Gráficos", command=generar_graficos).grid(row=9, columnspan=2, pady=5)


tk.Label(frame_inputs, text="Número de Salones:").grid(row=0, column=0, padx=5, pady=5)
entry_salones = tk.Entry(frame_inputs)
entry_salones.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Número de Mesas por Salón:").grid(row=1, column=0, padx=5, pady=5)
entry_mesas = tk.Entry(frame_inputs)
entry_mesas.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Número de Jurados por Mesa:").grid(row=2, column=0, padx=5, pady=5)
entry_jurados = tk.Entry(frame_inputs)
entry_jurados.grid(row=2, column=1, padx=5, pady=5)

tk.Button(frame_inputs, text="Generar", command=generar_centro_votacion).grid(row=3, columnspan=2, pady=10)

# Marco para el centro de votación (se llenará dinámicamente)
frame_centro_votacion = tk.Frame(root)
frame_centro_votacion.pack(padx=10, pady=10)


import json
from tkinter import filedialog


def guardar_datos_json():
    """Guarda la estructura completa del centro de votación en un archivo JSON"""
    try:
        salones = int(entry_salones.get())
        mesas = int(entry_mesas.get())
        jurados = int(entry_jurados.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa correctamente los números de salones, mesas y jurados.")
        return

    datos_guardar = {
        "salones": salones,
        "mesas_por_salon": mesas,
        "jurados_por_mesa": jurados,
        "jurados_registrados": [
            {
                "salon": j[0],
                "mesa": j[1],
                "jurado_numero": j[2],
                "nombre": j[3],
                "cedula": j[4],
                "telefono": j[5],
                "direccion": j[6],
            }
            for j in jurados_data
        ]
    }

    archivo = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if archivo:
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(datos_guardar, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Éxito", f"Datos guardados exitosamente en {archivo}")
        except Exception as e:
            messagebox.showerror("Error al guardar", f"No se pudieron guardar los datos: {e}")


# Iniciar el bucle principal
root.mainloop()
