from constraint import Problem, AllDifferentConstraint, InSetConstraint
from constraint import *
import sys
import csv
import random

filas = None  # Declare filas as a global variable
columnas = None  # Declare columnas as a global variable

# Comprobar si los vehículos están en la misma fila y uno detrás del otro
def vehiculos_en_pared(vehi_a, vehi_b):
    return (vehi_a[0] in [1, filas] and vehi_b[0] == vehi_a[0] + (1 if vehi_a[0] == 1 else -1)) and (vehi_b[1] == vehi_a[1])

# Comprobar si los vehículos están en filas adyacentes pero en columnas diferentes
def vehiculos_adyacentes(vehi_a, vehi_b):
    return (abs(vehi_a[0] - vehi_b[0]) == 1) and (vehi_a[1] != vehi_b[1])

# Comprobar si los vehículos están bloqueados entre sí
def vehiculos_bloqueados(vehi_a, vehi_b, vehi_c):
    return ((vehi_a[0] + 1 == vehi_b[0]) and (vehi_a[1] == vehi_b[1])) and ((vehi_a[0] - 1 == vehi_c[0]) and (vehi_a[1] == vehi_c[1]))
    
def maniobrabilidad(vehi1, vehi2, vehi3):
    if vehiculos_en_pared(vehi1, vehi2) or vehiculos_en_pared(vehi1, vehi3):
        return False
    if vehiculos_bloqueados(vehi1, vehi2, vehi3) or vehiculos_bloqueados(vehi1, vehi3, vehi2):
        return False
    if vehiculos_adyacentes(vehi1, vehi2) or vehiculos_adyacentes(vehi1, vehi3):
        return True

    return True

    
def imprimir_soluciones(soluciones, archivo):
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

def resolver_problema(plazas_electricas, vehiculos):
    problem = Problem()

    # Crear el parking como una lista de tuplas que representan las plazas
    parking = [(i, j) for i in range(1, filas+1) for j in range(1, columnas+1)]
    #Añadimos las variables
    for vehiculo in vehiculos:
        problem.addVariable(vehiculo[3], parking)
    problem.addConstraint(AllDifferentConstraint())
    #for vehiculo in vehiculos: vehiculo)
    for vehiculo in vehiculos:
        id, tipo, congelador = vehiculo[0], vehiculo[1], vehiculo[2]
        if congelador:  # Si el vehículo tiene congelador
            problem.addConstraint(InSetConstraint(plazas_electricas), [vehiculo[3]])
        if tipo == 'TSU':  # Si el vehículo es de tipo TSU
            for otro_vehiculo in vehiculos:
                if otro_vehiculo != vehiculo and otro_vehiculo[1] != 'TSU':  # Si el otro vehículo no es el mismo y no es de tipo TSU
                    # Añade la restricción
                    problem.addConstraint(lambda v1, v2: v1[0] != v2[0] or v1[1] >= v2[1], (vehiculo[3], otro_vehiculo[3]))
        for vehi2 in vehiculos:
            vehiculo2id = vehi2[0]
            if vehi2 != vehiculo:
                for vehi3 in vehiculos:
                    if vehi3 != vehiculo and vehi3 != vehi2:
                        problem.addConstraint(maniobrabilidad, (vehiculo[3], vehi2[3], vehi3[3]))
    return problem.getSolutions()

def leer_fichero():
    global filas, columnas 
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
        str_sol = line.strip()
        vehiculo = line.strip().split('-')
        id = int(vehiculo[0])
        tipo = vehiculo[1]
        congelador = vehiculo[2] == 'C'
        vehiculos.append((id, tipo, congelador, str_sol))
    # Llamar a la función que resuelve el problema
    soluciones = resolver_problema(plazas_electricas, vehiculos)
    imprimir_soluciones(soluciones, archivo)



if __name__ == "__main__":
    leer_fichero()
