from constraint import Problem, AllDifferentConstraint, InSetConstraint
from constraint import *
import sys
import csv
import random

filas = None  # Declare filas as a global variable
columnas = None  # Declare columnas as a global variable

# Comprobar si los vehículos están en la misma fila y uno detrás del otro
def vehiculos_en_pared(a1, a2):
    return (a1[0] in [1, filas] and a2[0] == a1[0] + (1 if a1[0] == 1 else -1)) and (a2[1] == a1[1])

# Comprobar si los vehículos están en filas adyacentes pero en columnas diferentes
#Esra funcion ayuda a relajar carga de trabajo 
def vehiculos_adyacentes(a1, a2):
    return (abs(a1[0] - a2[0]) == 1) and (a1[1] != a2[1])

# Comprobar si los vehículos están bloqueados entre sí
def vehiculos_bloqueados(a1, a2, a3):
    return ((a1[0] + 1 == a2[0]) and (a1[1] == a2[1])) and ((a1[0] - 1 == a3[0]) and (a1[1] == a3[1]))
    
def maniobrabilidad(a1, a2, a3):
    if vehiculos_en_pared(a1, a2) or vehiculos_en_pared(a1, a3):
        return False
    if vehiculos_adyacentes(a1, a2) or vehiculos_adyacentes(a1, a3):
        return True
    if vehiculos_bloqueados(a1, a2, a3) or vehiculos_bloqueados(a1, a3, a2):
        return False
    return True

    
def imprimir_soluciones(soluciones, archivo):
    # Crear el nombre del archivo de salida
    archivo_salida = archivo.split('.')[0] + '.csv'

    # Abrir el archivo de salida en modo escritura
    with open(archivo_salida, 'w', newline='') as f:
        writer = csv.writer(f)

        # Escribir el número de soluciones en la primera línea
        writer.writerow(["N. Sol: ", len(soluciones)])
        #Escogemos dos soluciones al azar
        if len(soluciones) > 2:
            soluciones = random.sample(soluciones, 2)
        # Para cada solución, escribir las filas del parking
        for solucion in soluciones:
            # Crear una matriz para representar el parking
            parking = [['-'] * columnas for _ in range(filas)]
            # Rellenar la matriz con los vehículos de la solución
            for vehiculo, plaza in solucion.items():
                parking[plaza[0]-1][plaza[1]-1] = vehiculo
            # Escribir la matriz en el archivo
            for fila in parking:
                writer.writerow(fila)

def resolver_problema(plazas_electricas, ambulancias):
    problem = Problem()
    # Crear el parking como una lista de tuplas que representan las plazas
    parking = [(i, j) for i in range(1, filas+1) for j in range(1, columnas+1)]

    #Añadimos las variables
    for ambulancia in ambulancias:
        congelador = ambulancia[1]
        if congelador:  # Si la ambulancia tiene congelador, entonces restringimos su dominio
            problem.addVariable(ambulancia[2], plazas_electricas)
        else: # Si no el dominio completo
            problem.addVariable(ambulancia[2], parking)

    #Añadimos la restriccion de valor unico
    problem.addConstraint(AllDifferentConstraint())
    for ambulancia in ambulancias:
        if ambulancia[0] == 'TSU':  # Si el vehículo es de tipo TSU
            for ambulancia2 in ambulancias:
                if ambulancia2 != ambulancia and ambulancia2[0] != 'TSU':  # Si el otro vehículo no es el mismo y no es de tipo TSU
                    # 2da restricción
                    problem.addConstraint(lambda v1, v2: v1[0] != v2[0] or v1[1] >= v2[1], (ambulancia[2], ambulancia2[2]))
        for ambulancia2 in ambulancias:
            if ambulancia2 != ambulancia:
                for ambulancia3 in ambulancias:
                    if ambulancia3 != ambulancia and ambulancia3 != ambulancia2:
                        problem.addConstraint(maniobrabilidad, (ambulancia[2], ambulancia2[2], ambulancia3[2]))
    #devolvemos las soluciones encontradas
    return problem.getSolutions()

def leer_fichero():
    global filas, columnas

    # Comprobar si se ha proporcionado un argumento de línea de comandos
    if len(sys.argv) != 2:
        print("Uso: python CSPParking.py <archivo>")
        return
    
    # Leer el archivo (Se Considera que el archivo viene en el formato correcto)
    archivo = sys.argv[1]
    with open(archivo, 'r') as f:
        lines = f.readlines()

    # Procesar las líneas del archivo para obtener los datos del problema
    size = lines[0].strip().split('x')
    filas = int(size[0])
    columnas = int(size[1])
    plazas_electricas = lines[1].strip()[4:-1].split(')(')
    plazas_electricas = [(int(plaza.split(',')[0]), int(plaza.split(',')[1])) for plaza in plazas_electricas]
    ambulancias = []
    for line in lines[2:]:
        str_sol = line.strip() #Va a ser el id de nuestra variable
        ambulancia = line.strip().split('-')
        tipo = ambulancia[1]
        congelador = ambulancia[2] == 'C'
        ambulancias.append((tipo, congelador, str_sol))

    # Llamar a la función que resuelve el problema
    soluciones = resolver_problema(plazas_electricas, ambulancias)
    imprimir_soluciones(soluciones, archivo)



if __name__ == "__main__":
    leer_fichero()
