# Practica 1 - Medicion empirica de complejidad
# Analisis de Algoritmos
# Codigo base de ejemplo
# Lenguaje: Python 3

import time #tiempo de ejecucion
import random #genera numeros aleatorios

def recorrido_simple(lista):#Define una lista
    total = 0
    for x in lista:
        total += x #suma el total a x
    return total #devuelve el total de la lista

def doble_ciclo(lista):#define una lista como argumento
    contador = 0
    for i in range(len(lista)):
        for j in range(len(lista)):
            contador += lista[i] * lista[j] #multiplica los elementos de la lista
    return contador #devuelve el vslor final del contador

def experimento():#define una funcion
    tamanios = [2000, 6000, 20000, 40000] #los tamanios de la funcion
    print("Tamano | Recorrido simple (s) | Doble ciclo (s)") #Texto que se escribira en la terminal para asimilar una tabla
    print("----------------------------------------------") #Texto que se escribira en la terminal para asimilar una tabla

    for n in tamanios: #Toma cada elemento n de la lista tamanios
        datos = [random.randint(1, 100) for _ in range(n)] #genera una lista de datos del 1 al 100 aleatoriamente

        inicio = time.time() #registra el tiempo de inicio de la lista
        recorrido_simple(datos) #llama a la funcion recorrido_simple con lops datos generados
        t1 = time.time() - inicio #guarda el tiempo para el primer recorrido

        inicio = time.time() #registra el tiempo de inicio de la lista
        doble_ciclo(datos) #llama a la funcion doble_ciclo con los datos generados
        t2 = time.time() - inicio #guarda el tiempo para el primer recorrido

        print(f"{n:6d} | {t1:20.6f} | {t2:15.6f}") #escribe en la terminal el tamano y los tiempos de los recorridos tomando en cuenta los valores ingresados

if __name__ == "__main__": #comprueba si la funcion se ejecuto correctamente
    experimento() #si se ejecuto directamente manda a llamar la funcion experimento

    #Dentro del mismo codigo observe que al ser una cantidad n mayor a los 5000 dentro de mi maquina el ejecutarse en doble ciclo duraba un segundo y aunque al duplicar la carga de datos uno esperaria que
    #solo el doble de tiempo pues en realidad se realentiza mucho el proceso del mismo ya que por poner un ejemplo 5000 me dura un segundo en doble ciclo y 10000 ya dura un total de 6 segundos
    #ademas de que el codigo nos sirve para medir el tiempo de procesamiento de los datos dentro del mismo computador y este mismo expresarlo al usuario