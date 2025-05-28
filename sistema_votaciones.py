import tkinter as t
from tkinter import messagebox, simpledialog
import json
#esta parte sirve para guardar los datos
estructura={}
#esta funcion sirve para generar la estructura 
def CrearEstructura():
    try:
        salones=int(entry_salones.get())
        mesas=int(entry_mesas.get())
        jurados=int(entry_jurados.get())
        if salones <=0 or mesas <=0 or jurados <=0:
            raise ValueError
        for limwindow in frame_estructura.winfo_children():
            limwindow.destroy()
            estructura.clear()

        for s in range(1, salones+1):
            salonNombre=f"salon{s}"
            estructura[salonNombre]={}
            t.label(frame_estructura, text=salonNombre).pack()
            for m in range(1, salones+1):
                mesaNombre=f"salon{m}"
                estructura[salonNombre][mesaNombre]={"jurados":[]}
                boton_mesa=t.Button(frame_estructura, text=mesaNombre, 
                                    command=lambda s=salonNombre, m=mesaNombre:verjurados(s,m))
                boton_mesa.pack(padx=10, pady=2)
                for j in range(1, jurados+1):
                    boton_jurado=t.Button(frame_estructura, text=f"{mesaNombre} - Jurado {j}", 
                                          command=lambda s=salonNombre, m=mesaNombre: RegistroDeJurados(s,m)) 
                    boton_jurado.pack(padx=20, pady=1)
    except ValueError:
        messagebox.showerror("error","solo puedes ingresar numeros enteros positivos")

def RegistroDeJurados(salon,mesa):
    nombre= simpledialog.askstring("nombre","ingrese el nombre")
    cedula= simpledialog.askstring("cedula","ingrese la cedula")
    telefono= simpledialog.askstring("telefono","ingrese el telefono")
    direccion= simpledialog.askstring("direccion","ingrese la direccion")
    if not all([nombre,cedula,telefono,direccion]):
        messagebox.showerror("error","tienes que llenar todos los campos es obligatorio")
        return
    jurado={"nombre":nombre,"cedula":cedula,"telefono":telefono,"direccion":direccion}
    estructura[salon][mesa]["jurados"].append(jurado)
    messagebox.showinfo("exito","el jurado fue registrado con exito")
def verjurados(salon,mesa):
    jurados= estructura[salon][mesa]["jurados"]
    if not jurados:
        messagebox.showinfo("informacion",f"no hay jurados en {mesa}")
    else: 
        texto="\n".join([f"{j['nombre']}, cedula: {j['cedula']}" for j in jurados])
        messagebox.showinfo("jurados",f"jurados en {mesa}:\n{texto}")

ventana = t.Tk()
ventana.title("centro de votacion")
t.Label(ventana, text="numero de salones:").pack()
entry_salones= t.Entry(ventana)
entry_salones.pack()

t.Label(ventana, text="mesas por salon:").pack()
entry_mesas= t.Entry(ventana)
entry_mesas.pack()

t.Label(ventana, text="jurados por mesa:").pack()
entry_jurados= t.Entry(ventana)
entry_jurados.pack()

crearboton=t.Button(ventana, text="generar", command=CrearEstructura)
crearboton.pack(pady=10)

frame_estructura = t.Frame(ventana)
frame_estructura.pack(pady=10)
ventana.mainloop