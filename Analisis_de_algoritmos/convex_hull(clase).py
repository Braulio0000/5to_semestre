import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

#Función para cargar el archivo CSV
def leer_puntos_csv(ruta_csv):
    puntos = []
    try:
        with open(ruta_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                x = float(row["x"])
                y = float(row["y"])
                puntos.append((x, y))
    except Exception as e:
        print("Error al leer:", e)
    return puntos

def punto_mas_izquierdo(puntos):
    idx = 0
    for i in range(1, len(puntos)):
        if puntos[i][0] < puntos[idx][0] or (puntos[i][0] == puntos[idx][0] and puntos[i][1] < puntos[idx][1]):
            idx = i
    return idx


def orientacion(a, b, c):
    # Producto cruz para determinar el giro
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def distancia2(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def convex_hull(puntos):
    n = len(puntos)
    if n < 3: return puntos
    
    hull = []
    start_idx = punto_mas_izquierdo(puntos)
    p_idx = start_idx
    
    while True:
        hull.append(puntos[p_idx])
        q_idx = (p_idx + 1) % n
        
        for r_idx in range(n):
            if r_idx == p_idx: continue
            o = orientacion(puntos[p_idx], puntos[q_idx], puntos[r_idx])
            # Si r está más a la izquierda que q, r es mejor candidato
            if o > 0 or (o == 0 and distancia2(puntos[p_idx], puntos[r_idx]) > distancia2(puntos[p_idx], puntos[q_idx])):
                q_idx = r_idx
        
        p_idx = q_idx
        if p_idx == start_idx: break
    return hull

# Graficar los puntos y la envolvente
def dibujar(puntos, hull):
    plt.figure("Resultado de Convex Hull")
    # Separar x e y para graficar
    px, py = zip(*puntos)
    plt.scatter(px, py, color='black', label='Puntos')
    
    if hull:
        # Volver al punto inicial para cerrar el polígono
        hx, hy = zip(*(hull + [hull[0]]))
        plt.plot(hx, hy, color='yellow', linewidth=2, label='Envolvente')
    
    plt.title(f"Puntos procesados: {len(puntos)}")
    plt.legend()
    plt.grid(True)
    plt.show()

# Función para el botón de la GUI
def accion_boton():
    ruta = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if ruta:
        puntos = leer_puntos_csv(ruta)
        if puntos:
            hull = convex_hull(puntos)
            dibujar(puntos, hull)
        else:
            messagebox.showwarning("Vacío", "No se encontraron coordenadas válidas.")

# Configuración de la GUI
ventana = tk.Tk()
ventana.title("Analizador de Coordenadas")
ventana.geometry("300x120")

# Elementos de la GUI
instruccion = tk.Label(ventana, text="Carga un archivo CSV (0-1000 x,y)", pady=10)
instruccion.pack()

boton = tk.Button(ventana, text="Seleccionar Archivo y Graficar", command=accion_boton)
boton.pack(pady=10)

# jecutar el programa
ventana.mainloop()