import tkinter as t
from tkinter import messagebox, simpledialog
import json
import csv
import pandas as p
# esta parte sirve para guardar los datos de los salones, mesas y jurados
estructura = {}

# esta funcion sirve para generar la estructura gracias a un boton
def CrearEstructura():
    try:
        salones = int(entry_salones.get())
        mesas = int(entry_mesas.get())  # esto toma los valores del usuario y los convierte a enteros
        jurados = int(entry_jurados.get())

        if salones <= 0 or mesas <= 0 or jurados <= 0:  # verifica que los valores no sean negativos
            raise ValueError

        for limwindow in frame_estructura.winfo_children():
            limwindow.destroy()  # limpia cualquier boton o etiqueta anterior de la ventana si ya se habia generado una estructura antes

        estructura.clear()  # vacia la estructura para empezar de nuevo

        for s in range(1, salones + 1):
            salonNombre = f"salon{s}"  # crea los salones con un nombre por ejemplo salon1 y añade una entrada vacia en el diccionario
            estructura[salonNombre] = {}

            t.Label(frame_estructura, text=salonNombre).pack()  # muestra el nombre del salon

            for m in range(1, mesas + 1):
                mesaNombre = f"mesa{m}"  # crea mesas con nombre y una lista vacia
                estructura[salonNombre][mesaNombre] = {"jurados": []}

                boton_mesa = t.Button(frame_estructura, text=mesaNombre,
                                      command=lambda s=salonNombre, m=mesaNombre: verjurados(s, m))
                boton_mesa.pack(padx=10, pady=2)  # crea un boton para cada mesa los cuales muestran los jurados 

                for j in range(1, jurados + 1):
                    boton_jurado = t.Button(frame_estructura, text=f"{mesaNombre} - Jurado {j}",
                                            command=lambda s=salonNombre, m=mesaNombre: RegistroDeJurados(s, m))
                    boton_jurado.pack(padx=20, pady=1)  # crea botones para los jurados en los cuales se podrá ingresar los datos de los jurados 

    except ValueError:  # si los valores de los numeros no son enteros positivos muestra un error
        messagebox.showerror("error", "solo puedes ingresar numeros enteros positivos")

# esta funcion sirve para registrar a los jurados 
def RegistroDeJurados(salon, mesa):
    nombre = simpledialog.askstring("nombre", "ingrese el nombre")
    cedula = simpledialog.askstring("cedula", "ingrese la cedula")  # muestra una ventana para que se ingresen los datos de los jurados 
    telefono = simpledialog.askstring("telefono", "ingrese el telefono")
    direccion = simpledialog.askstring("direccion", "ingrese la direccion")

    if not all([nombre, cedula, telefono, direccion]):
        messagebox.showerror("error", "tienes que llenar todos los campos es obligatorio")
        return  # esto verifica que no quede ningun valor sin llenar 

    jurado = {"nombre": nombre, "cedula": cedula, "telefono": telefono, "direccion": direccion}
    estructura[salon][mesa]["jurados"].append(jurado)  # crea un diccionario con los datos de los jurados y los agrega a la lista de jurados de la mesa
    messagebox.showinfo("exito", "el jurado fue registrado con exito")

# esta funcion sirve para buscar la lista de jurado/s en la mesa correspondiente
def verjurados(salon, mesa):
    jurados = estructura[salon][mesa]["jurados"]

    if not jurados:  # esto muestra si en la mesa hay jurados registrados 
        messagebox.showinfo("informacion", f"no hay jurados en {mesa}")
    else:  # este muestra en texto los datos del jurado que fue ingresado
        texto = "\n".join([f"{j['nombre']}, cedula: {j['cedula']}" for j in jurados])
        messagebox.showinfo("jurados", f"jurados en {mesa}:\n{texto}")

# esta funcion sirve para guardar los datos en un archivo JSON
def guardarEstructura():
    with open("estructura.json", "w", encoding="utf-8") as folder:
        json.dump(estructura, folder, indent=4)
    messagebox.showinfo("guardado", "el archivo fue guardado exitosamente")

# esta funcion sirve para cargar los datos desde un archivo JSON
def cargarEstructura():
    global estructura
    try:
        with open("estructura.json", "r", encoding="utf-8") as folder:
            estructura = json.load(folder)
        messagebox.showinfo("cargado", "el archivo fue cargado exitosamente")
    except FileNotFoundError:
        messagebox.showerror("error", "archivo no encontrado")
def cargarvotantescsv():
    try:
        with open("votantes.csv", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                nombre = fila["nombre"]
                cedula = fila["cedula"]
                salon = fila ["salon"]
                mesa = fila ["mesa"]
                
                if salon not in estructura:
                    messagebox.showerror("error",f"el salon {salon} no existe")
                    continue
                if mesa not in estructura[salon]:
                    messagebox.showerror("error",f"la mesa {mesa} no existe en {salon}")
                    continue
                if "votantes" not in estructura[salon][mesa]:
                    estructura[salon][mesa]["votantes"]= []
                existentes= [v["cedula"]for v in estructura[salon][mesa]["votantes"]]    
                if cedula in existentes:
                    continue
                estructura[salon][mesa]["votantes"].append({"nombre":nombre, "cedula":cedula})
                messagebox.showinfo("exito","el votante fue cargado con exito")
    except FileNotFoundError:
        messagebox.showerror("error","el archivo de votantes.csv no se encontro")

def rigistrarAsistencia():
    cedula=simpledialog.askstring("asistencia","ingresa la cedula del votante:")
    salon=simpledialog.askstring("asistencia","ingresa el salon:")
    mesa=simpledialog.askstring("asistencia","ingresa la mesa:")
    hora=simpledialog.askstring("asistencia","ingresa la hora (hh:mm):")

    if not all ([cedula, salon, mesa, hora]):
        messagebox.showerror("error","todos los campos se deben de llenar")
        return
    
    if salon not in estructura or mesa not in estructura[salon]:
        messagebox.showerror("error","el salon o la mesa no existe")
        return
    
    try:
        Hdivipor=hora.split(":")
        hora=int(Hdivipor[0])
        if hora>=16:
            messagebox.showerror("error","la hora no puede ser despues de las 4:00 pm ")
            return
        
    except:
        messagebox.showerror("error","formato de hora incorrecto(usa hh:mm)")
        return
    
    mesaInfo=estructura[salon][mesa]
    votantes=mesaInfo.get("votantes",[])
    if cedula not in [v["cedula"]for v in votantes]:
        messagebox.showerror("error","no hay cedula registrada en esa mesa")
        return
    
    if "asistencias" not in mesaInfo:
        mesaInfo["asistencias"]=[]

    siAsistio=any(a["cedula"]==cedula for a in mesaInfo["asistencias"])
    if siAsistio:
        messagebox.showinfo("informacion","el votante ya registro su asistencia")
        return
    mesaInfo["asistencia"].append({"cedula":cedula,"hora":hora})
    messagebox.showinfo("exito", "asistencia registrada correctamente")

#esta funcion utiliza pandas para crear un resumen estadistico
def resumenEstadistico():
    try:
        resumen=[]

        for salon,mesas in estructura.items():
            jurados_total=0
            votantes_total=0
            asistencias_total=0
            mesas_completas=0
            mesas_totales= len(mesas)

            for mesa_nombre, mesa_info in mesas.items():
                jurados = mesa_info.get("jurados",[])
                votantes = mesa_info.get("votantes",[])
                asistencias = mesa_info.get("asistencias",[])

                jurados_total += len(jurados)
                votantes_total += len(votantes)
                asistencias_total += len(asistencias) if asistencias else 0

                if len(jurados) >=1:
                    mesas_completas +=1

            porcentaje_completas = (mesas_completas / mesas_totales) * 100 if mesas_totales else 0

            resumen.append({
                "Salón": salon,
                "Jurados totales": jurados_total,
                "Votantes totales": votantes_total,
                "Votantes con asistencia": asistencias_total,
                "Porcentaje mesas completas": round(porcentaje_completas, 2)})

        df = p.DataFrame(resumen)
        messagebox.showinfo("Resumen Estadístico", df.to_string(index=False))

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el resumen:\n{e}")



ventana = t.Tk()  # crea la ventana principal
ventana.title("centro de votacion")

t.Label(ventana, text="numero de salones:").pack()
entry_salones = t.Entry(ventana)
entry_salones.pack()

t.Label(ventana, text="mesas por salon:").pack()
entry_mesas = t.Entry(ventana)  # agrega etiquetas y campos para que el usuario ingrese salones, mesas y jurados
entry_mesas.pack()

t.Label(ventana, text="jurados por mesa:").pack()
entry_jurados = t.Entry(ventana)
entry_jurados.pack()

crearboton = t.Button(ventana, text="generar", command=CrearEstructura)
crearboton.pack(pady=10)  # crea un boton que cuando se presiona crea la estructura

boton_guardar = t.Button(ventana, text="guardar estructura", command=guardarEstructura)
boton_guardar.pack()

boton_cargar = t.Button(ventana, text="cargar estructura", command=cargarEstructura)
boton_cargar.pack()

boton_cargar_votantes=t.Button(ventana, text="cargar votantes", command=cargarvotantescsv)
boton_cargar_votantes.pack()

botonAsistencia=t.Button(ventana, text="registrar asistencia", command=rigistrarAsistencia)
botonAsistencia.pack()

botondelresumenestadistico=t.Button(ventana, text="resumen estadistico", command=resumenEstadistico)
botondelresumenestadistico.pack()

frame_estructura = t.Frame(ventana)
frame_estructura.pack(pady=10)  # crea un frame o marco en el que se colocan los botones de los salones, mesas y jurados

ventana.mainloop()  # mantiene la ventana abierta mientras el programa esté corriendo
