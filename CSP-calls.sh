#!/bin/bash

#Unos cuantos casos sobre soluciones posibles y soluciones varias:
# Primer ejemplo del pdf, un caso bastante complejo
python3 CSPParking.py datos/parking01.dat
# Un parking pequeño con solo 3 soluciones
python3 CSPParking.py datos/parking02.dat
# Otro caso con 38 soluciones
python3 CSPParking.py datos/parking03.dat
# Caso de prueba para un parking con una sola fila y múltiples plazas con conexión eléctrica:
python3 CSPParking.py datos/parking04.dat
# Caso de prueba para un parking pequeño con pocas plazas y varios vehículos con y sin congelador:
python3 CSPParking.py datos/parking06.dat
# Caso de prueba con mas ambulancias con congelador que plazas electricas
python3 CSPParking.py datos/parking07.dat
# Caso de prueba que obliga a infringir la segunda restriccion
python3 CSPParking.py datos/parking08.dat
echo "Ejecución de casos de prueba completada."