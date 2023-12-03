from constraint import Problem, AllDifferentConstraint, InSetConstraint
from constraint import *
import sys
import csv
import random

def imprimir_soluciones(soluciones, archivo, filas, columnas):
    # Crear el nombre del archivo de salida
    archivo_salida = archivo.split('.')[0] + '.csv'

    # Abrir el archivo de salida en modo escritura
    with open(archivo_salida, 'w', newline='') as f:
        writer = csv.writer(f)

        # Escribir el número de soluciones en la primera línea
        writer.writerow(["N. Sol: ", len(soluciones)])

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

def resolver_problema(filas, columnas, plazas_electricas, vehiculos):
    problem = Problem()

    # Crear el parking como una lista de tuplas que representan las plazas
    parking = [(i, j) for i in range(1, filas+1) for j in range(1, columnas+1)]
    #Añadimos las variables
    for vehiculo in vehiculos:
        problem.addVariable(vehiculo[0], parking)
    problem.addConstraint(AllDifferentConstraint())
    #for vehiculo in vehiculos: vehiculo)
    for vehiculo in vehiculos:
        id, tipo, congelador = vehiculo[0], vehiculo[1], vehiculo[2]
        if congelador:  # Si el vehículo tiene congelador
            problem.addConstraint(InSetConstraint(plazas_electricas), [id])
        if tipo == 'TSU':  # Si el vehículo es de tipo TSU
            for otro_vehiculo in vehiculos:
                if otro_vehiculo != vehiculo and otro_vehiculo[1] != 'TSU':  # Si el otro vehículo no es el mismo y no es de tipo TSU
                    # Añade la restricción
                    problem.addConstraint(lambda v1, v2: v1[0] != v2[0] or v1[1] >= v2[1], (vehiculo[0], otro_vehiculo[0]))
        for vehi2 in vehiculos:
            vehiculo2id = vehi2[0]
            problem.addConstraint(lambda v1, v2: (v1[0]-1!=v2[0] and v1[0]!=1)  or (v1[0]+1!=v2[0] and v1[0]!=filas), (id, vehiculo2id)) 
    return problem.getSolutions()

def leer_fichero():
    # Comprobar si se ha proporcionado un argumento de línea de comandos
    if len(sys.argv) != 2:
        print("Uso: python CSPParking.py <archivo>")
        return
    # Leer el archivo
    archivo = sys.argv[1]
    with open(archivo, 'r') as f:
        lines = f.readlines()

    # Procesar las líneas del archivo para obtener los datos del problema
    size = lines[0].strip().split('x')
    filas = int(size[0])
    columnas = int(size[1])

    plazas_electricas = lines[1].strip()[4:-1].split(')(')
    plazas_electricas = [(int(plaza.split(',')[0]), int(plaza.split(',')[1])) for plaza in plazas_electricas]
    vehiculos = []
    for line in lines[2:]:
        vehiculo = line.strip().split('-')
        id = int(vehiculo[0])
        tipo = vehiculo[1]
        congelador = vehiculo[2] == 'C'
        vehiculos.append((id, tipo, congelador))
    # Llamar a la función que resuelve el problema
    soluciones = resolver_problema(filas, columnas, plazas_electricas, vehiculos)
    imprimir_soluciones(soluciones, archivo, filas, columnas)



if __name__ == "__main__":
    leer_fichero()
