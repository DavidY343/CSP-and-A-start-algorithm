from constraint import Problem, AllDifferentConstraint, InSetConstraint
from constraint import *
import sys

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
    solutions = problem.getSolutions()
    i = 0
    for sol in solutions:
        i += 1
    print(i)



"""
def resolver_problema(filas, columnas, plazas_electricas, vehiculos):
    problem = Problem()

    # Crear el parking como una lista de tuplas que representan las plazas
    parking = [(i, j) for i in range(1, filas+1) for j in range(1, columnas+1)]

    # Añadir las variables al problema. Cada vehículo es una variable y las plazas de parking son sus dominios
    for id, tipo, congelador in vehiculos:
        problem.addVariable(id, parking)

    # Añadir la restricción de que todos los vehículos deben estar en plazas diferentes
    problem.addConstraint(AllDifferentConstraint(), [id for id, tipo, congelador in vehiculos])
    # Añadir las restricciones específicas del problema
    for id1, tipo1, congelador1 in vehiculos:
        if tipo1 == 'TSU':
            for id2, tipo2, congelador2 in vehiculos:
                if id1 != id2:
                    # Restricción 4
                    problem.addConstraint(lambda x, y: x[0] <= y[0] or x[1] != y[1], (id1, id2))
        if congelador1:
            # Restricción 3
            problem.addConstraint(lambda x: x in plazas_electricas, (id1,))
        for id2, tipo2, congelador2 in vehiculos:
            for id3, tipo3, congelador3 in vehiculos:
                if id1 != id2 and id1 != id3 and id2 != id3:
                    # Restricción 5
                    problem.addConstraint(lambda x, y, z: x[1] != y[1] or x[1] != z[1], (id1, id2, id3))

    # Resolver el problema
    soluciones = problem.getSolutions()

    return soluciones
"""

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

    # Imprimir las soluciones
    #    for solucion in soluciones:
     #   print(solucion)


if __name__ == "__main__":
    leer_fichero()
