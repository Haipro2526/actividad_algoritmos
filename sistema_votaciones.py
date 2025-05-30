import tkinter as t
from tkinter import messagebox, simpledialog
import json
import csv
import pandas as p
import matplotlib.pyplot as plt
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
        with open("estructura.json", "r", encoding="utf-8") as folder: #carga el archivo json y si este no existe manda un error
            estructura = json.load(folder)
        messagebox.showinfo("cargado", "el archivo fue cargado exitosamente")
    except FileNotFoundError:
        messagebox.showerror("error", "archivo no encontrado")

def cargarvotantescsv():
    try:
        with open("votantes.csv", newline="", encoding="utf-8") as archivo: # abre el archivo vontantes.csv en el que se verifican los saltos de lineas y los caracteres especiales como tildes u otro simbolos
            lector = csv.DictReader(archivo)
            for fila in lector: # lee las filas segun en donde se encuetre 
                nombre = fila["nombre"]
                cedula = fila["cedula"]
                salon = fila ["salon"]
                mesa = fila ["mesa"]
                
                if salon not in estructura:
                    messagebox.showerror("error",f"el salon {salon} no existe") #verifica si el salon no existe y mestra un error para luego continuar la revision
                    continue
                if mesa not in estructura[salon]:
                    messagebox.showerror("error",f"la mesa {mesa} no existe en {salon}") #verifica si la mesa no existe en el salon
                    continue
                if "votantes" not in estructura[salon][mesa]:
                    estructura[salon][mesa]["votantes"]= [] # verifica si el votante no esta en el diccionario salon y mesa ya que gracias a la llave votante
                existentes= [v["cedula"]for v in estructura[salon][mesa]["votantes"]]# extras todas las cedulas y las guarda en un diccionario llamdo existentes    
                if cedula in existentes: #se salta la fila si la cedula ya esta en la lista de existentes esta se salta la fila y no la vuelve a registrar
                    continue # salta al siguiente ciclo
                estructura[salon][mesa]["votantes"].append({"nombre":nombre, "cedula":cedula}) #agrega un nuevo votante a la lista con nombre y cedula 
                messagebox.showinfo("exito","el votante fue cargado con exito")# abre un venta emergente que contiene un mensaje
    except FileNotFoundError:#si no se encuentra el archivo se activa el parametro except y abre una ventana emergente que muestra el error
        messagebox.showerror("error","el archivo de votantes.csv no se encontro")
# esta funcion sirve para verificar si el votsante asistio o no
def rigistrarAsistencia():
    cedula=simpledialog.askstring("asistencia","ingresa la cedula del votante:")
    salon=simpledialog.askstring("asistencia","ingresa el salon:")
    mesa=simpledialog.askstring("asistencia","ingresa la mesa:")# se muestra una ventana en lo que hay que escribir lo que te pide y se guarda lo que escribiste en cada variante
    hora=simpledialog.askstring("asistencia","ingresa la hora (hh:mm):")

    if not all ([cedula, salon, mesa, hora]):
        messagebox.showerror("error","todos los campos se deben de llenar")
        return
    
    if salon not in estructura or mesa not in estructura[salon]:
        messagebox.showerror("error","el salon o la mesa no existe")
        return
#estos datos que se ponen en esta funcion deben concordar con los datos del archivo votantes.csv    
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
    if siAsistio:#recorre la lista que contiene los votantes que se registraron y any devuelve true si almenos una vez se cumple la condicion
        messagebox.showinfo("informacion","el votante ya registro su asistencia")
        return
    mesaInfo["asistencias"].append({"cedula":cedula,"hora":hora})
    messagebox.showinfo("exito", "asistencia registrada correctamente")

#esta funcion utiliza pandas para crear un resumen estadistico
def resumenEstadistico():
    try:
        resumen=[]# se crea una lista vacia

        for salon,mesas in estructura.items():# recorre los dastos de cada salon y sus mesas dentro del direcctorio 
            jurados_total=0
            votantes_total=0#llevan los  datos de  cada unos los votantes jurados los que asistieron y las mesas que estan completas
            asistencias_total=0
            mesas_completas=0
            mesas_totales= len(mesas)# ceunta cuantas mesas tiene el salon

            for mesa_nombre, mesa_info in mesas.items():#obtiene el nombre de la mesa y toda su informacion
                jurados = mesa_info.get("jurados",[])
                votantes = mesa_info.get("votantes",[])#abotiene la lista de cada uno y si no hay nada pone que la lista esta vacia
                asistencias = mesa_info.get("asistencias",[])

                jurados_total += len(jurados)#suma la cantidad de jurados en la mesa al total de jurados en el salon
                votantes_total += len(votantes)#suma los votantes de cada mesa al total de votantes en el salon
                asistencias_total += len(asistencias) if asistencias else 0 # suma las asistencias y si no hay da 0

                if len(jurados) >=1:
                    mesas_completas +=1

            porcentaje_completas = (mesas_completas / mesas_totales) * 100 if mesas_totales else 0

            resumen.append({
                "Salón": salon,
                "Jurados totales": jurados_total,
                "Votantes totales": votantes_total,#crea un diccionario en donde guarda los datos de cada variable consu respectiva llave 
                "Votantes con asistencia": asistencias_total,
                "Porcentaje mesas completas": round(porcentaje_completas, 2)})#esn esta tambien guarda los datos y añade la funcion de redondear a 2 decimales

        Tbr = p.DataFrame(resumen) #comvierte la lista resumen en una tabla usando pandas
        messagebox.showinfo("Resumen Estadístico", Tbr.to_string(index=False))#muestra la tabla en una ventana emergente sin mostrar los indices

    except Exception as e:# muestra una ventana con el error del problema
        messagebox.showerror("Error", f"No se pudo generar el resumen:\n{e}")

def generarGraficos():
    salones=[]
    jurados=[]#estos son listas vacias para guardar el conteo de cada variable
    votantes=[]
    asistencias=[]

    mesas_totales=0
    mesas_completas=0#estos son contadores para los valores 
    total_votantes=0
    total_asistencias=0

    for salon, mesas in estructura.items():
        salones.append(salon)#recorre cada salon y mesa en estructurra y añade el nombre del salon a la lista salones
        jurados_salon=0
        votantes_salon=0#estos son contadores para los votantes los jurados y los asistentes
        asistencias_salon=0

        for mesa_info in mesas.values():
            jurados_salon += len(mesa_info.get("jurados",[]))#cuenta cuantos jurados hay y si no hay ninguno lo deja vacio
            votantes_salon += len(mesa_info.get("votantes", []))#este es igual pero con los votantes
            asistencias_salon += len(mesa_info.get("asistencias", [])) if "asistencias" in mesa_info else 0 # este es lo mismo solo que si no hay asistencia da como resultado 0
            
            total_votantes += votantes_salon# va sumando los votantes de los salones para el resultado en total 
            total_asistencias += asistencias_salon#lo mismo pero con las asistencias
            mesas_totales += 1#por cada mesa que alla se suma una al contador
            if len (mesa_info.get("jurados",[]))>0:#usa la llave jurados para verificar si estan todos los jurados si la condicion se cumple se incrementa el contador de mesas_completas
                mesas_completas +=1
        
        jurados.append(jurados_salon)
        votantes.append(votantes_salon)# agrega los datos a las listas generales
        asistencias.append(asistencias_salon)
#esta parte crea el grafico de barras 
    x=range(len(salones))#crea una secuensia de numeros hasta a cantidad de salones que el ususario puso
    plt.figure(figsize=(10,5))#da los parametros del grafico x,y osea controla el tamaño
    plt.bar(x, jurados, width=0.2, label='Jurados', align='center')#crea una barra le da su grosor una etiqueta y lo centra sobre el numero de x
    plt.bar([i + 0.2 for i in x], votantes, width=0.2, label='Votantes', align='center')#esta realiza un desplazamiento a la derecha
    plt.bar([i + 0.4 for i in x], asistencias, width=0.2, label='Asistencias', align='center')#crea una barra por grupo para la asistencia mas a la derecha
    plt.xticks([i + 0.2 for i in x], salones)#remplasa el numero de x poe los nombres de los salones y se alinea con el grupo de barras
    plt.title("jurados votantes y asistencias por salón")#este es el titulo de la tabla
    plt.legend()#ayuda a identificar los diferentes elementos de la linea
    plt.tight_layout()#ajusta todo automaticamente para que no se corte ni el texto ni las barras
    plt.show()#muestra el grafico
#esta parte hace una coparacion entre las mesas que estan completas y las que estan incompletas creando un grafico de pastel
    incompletas = mesas_totales - mesas_completas#calcula la cantidad de mesas incompletas que hay
    plt.figure()#crea un nuevo grafico independiente
    plt.pie([mesas_completas, incompletas], labels=["Completas", "Incompletas"], autopct='%1.1f%%')#dibuja el diagrama mostrando las eiquetas con los labels y el porsentaje gracias a el autopct='%1.1f%%'
    plt.title("Mesas con jurados completos vs incompletos")#titulo de la grafica
    plt.show()#muestra el grafico

    no_asistieron = total_votantes - total_asistencias#calcula los votantes que no hacistieron
    plt.figure()#nuevo diagrama independiente
    plt.pie([total_asistencias, no_asistieron], labels=["Asistieron", "No asistieron"], autopct='%1.1f%%')#dibuja el diagrama igual que en anterior los que cambia es que este es con los que asistieron 
    plt.title("Asistencia de votantes")#el titulo del diagrama
    plt.show()#muestra el diagrama
#esta funcion sirve para ver los resultados desde un archivo csv
def cargarResultados():
    try:
        with open("resultados.csv", newline="", encoding="utf-8") as archivo:# abre el archivo y usa utf-8 para que los asentos se lean bien
            lector = csv.DictReader(archivo)#crea un lector que interpreta cada fila como un diccionario
            resultados = {f"res{i}": {"Sí": 0, "No": 0} for i in range(1, 10)} #crea un diccionario con 9 preguntas cada una con un contador de si y no

            for fila in lector:# recorre cada fila 
                for i in range(1, 10):# recorre las preguntas de respusesta1(res) a respuesta9(res)
                    respuesta = fila[f"res{i}"].strip().capitalize()#carrigue la escritura por si pone espaciones o se ponen minusculas por ejemplo "si "
                    if respuesta in ["Sí", "No"]:#verisfica si la respuesta el valida
                        resultados[f"res{i}"][respuesta] += 1 #suma 1 al contador correspondiente

#genera un grafico de barras horizontales
        preguntas = [f"Persona{i}" for i in range(1, 10)]#crea una lista con los nombres de las preguntas para mostrarlas como persona 1 persona 2 ...
        si = [resultados[f"res{i}"]["Sí"] for i in range(1, 10)]#crea una lista con la cantidad de respuestas "Si" por cada una de las preguntas
        no = [resultados[f"res{i}"]["No"] for i in range(1, 10)]#lo mismo con esta solo que con el "No"

        plt.figure(figsize=(10, 6))#crea un nuevo grafico
        plt.barh(preguntas, si, label="Sí", color="green")#crea las barra y la hace con color verde para la respuesta si
        plt.barh(preguntas, no, left=si, label="No", color="red")# y para estas las crea con el color rojo
        plt.xlabel("Cantidad de respuestas")# es una etiqueta para el eje x
        plt.title("Resultados de votación por pregunta")#es un titulo para el grafico
        plt.legend()#ayuda a identificar los diferentes elementos de la linea
        plt.tight_layout()#ajusta el grafico para que no se corte el texto
        plt.show()#muestra el grafico

    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo resultados.csv no fue encontrado.")


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
boton_guardar.pack() #guarda la estructura mediante un archivo json

boton_cargar = t.Button(ventana, text="cargar estructura", command=cargarEstructura)
boton_cargar.pack() #carga el archivo y si no existe manda un error

boton_cargar_votantes=t.Button(ventana, text="cargar votantes", command=cargarvotantescsv)
boton_cargar_votantes.pack() #carga un archivo csv que contenga los votantes

botonAsistencia=t.Button(ventana, text="registrar asistencia", command=rigistrarAsistencia)
botonAsistencia.pack()

botondelresumenestadistico=t.Button(ventana, text="resumen estadistico", command=resumenEstadistico)
botondelresumenestadistico.pack()

botonGraficos=t.Button(ventana, text="generar graficos", command=generarGraficos)
botonGraficos.pack()

boton_resultados = t.Button(ventana, text="Cargar resultados", command=cargarResultados)
boton_resultados.pack()

frame_estructura = t.Frame(ventana)
frame_estructura.pack(pady=10)  # crea un frame o marco en el que se colocan los botones de los salones, mesas y jurados

ventana.mainloop()  # mantiene la ventana abierta mientras el programa esté corriendo
