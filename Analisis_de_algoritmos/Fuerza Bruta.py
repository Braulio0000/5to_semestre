import tkinter as tk
from tkinter import messagebox
import math

def distancia(p1, p2):
    # Recibe dos puntos 
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def par_mas_cercano(puntos):
    # Si tenemos menos de 2 puntos, no podemos comparar nada.
    if len(puntos) < 2:
        return None, 0
        
    #distancia infinita cualquier distancia es menor.
    min_dist = float('inf')
    par = None
    
    # comparación toma un punto y el segundo ciclo lo compara con todos los siguientes.
    for i in range(len(puntos)):
        for j in range(i + 1, len(puntos)):
            # Calculamos la distancia 
            d = distancia(puntos[i], puntos[j])
            
            # encontrar distancia mas corta
            if d < min_dist:
                min_dist = d          # guarda la distancia
                par = (puntos[i], puntos[j]) 
                
    # distancia mas corta
    return par, min_dist

#funcion para obtener puntos o valores
def obtener_puntos():
    puntos = []
    try:
        for entry_x, entry_y in zip(entradas_x, entradas_y):
            val_x = entry_x.get()
            val_y = entry_y.get()
            if val_x and val_y:
                x = float(val_x)
                y = float(val_y)
                puntos.append((x, y)) # Agregamos el punto a nuestra lista
        
        if len(puntos) < 2:
            messagebox.showwarning("Atención", "Ingrese al menos 2 puntos completos.")
            return None
            
        return puntos
    except ValueError:
        messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
        return None

def calcular():
    puntos = obtener_puntos()
    if puntos:
        par, distancia_min = par_mas_cercano(puntos)
        if par:
            label_resultado.config(
                text=f"Par más cercano:\n{par[0]} y {par[1]}\nDistancia: {distancia_min:.4f}",
                fg="blue" 
            )
# Creamos la ventana principal
ventana = tk.Tk()
ventana.title("Par más cercano") # Título de la ventana
ventana.geometry("300x450")      # Tamaño (ancho x alto)

# Texto de instrucción arriba
tk.Label(ventana, text="Ingrese los puntos (x, y):", font=("Arial", 12)).pack(pady=10)

# Un marco invisible para organizar las cajitas de entrada
marco_entradas = tk.Frame(ventana)
marco_entradas.pack(pady=5)

# Encabezados de la tabla 
tk.Label(marco_entradas, text="Coordenadas X", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10)
tk.Label(marco_entradas, text="Coordenadas Y", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=10)

# Listas
entradas_x = []
entradas_y = []

for i in range(5): 
    # Creamos la cajita para X 
    e_x = tk.Entry(marco_entradas, width=12)
    e_x.grid(row=i+1, column=0, padx=10, pady=3)
    entradas_x.append(e_x)
    
    # Creamos la cajita para Y 
    e_y = tk.Entry(marco_entradas, width=12)
    e_y.grid(row=i+1, column=1, padx=10, pady=3)
    entradas_y.append(e_y)

# Creamos el botón.
boton = tk.Button(ventana, text="Calcular Distancia Mínima", command=calcular, bg="#dddddd", fg="black", font=("Arial", 10))
boton.pack(pady=15)

#respuesta final
label_resultado = tk.Label(ventana, text="Esperando", font=("Arial", 10))
label_resultado.pack(pady=5)

ventana.mainloop()