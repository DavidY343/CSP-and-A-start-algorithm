#!/bin/sh

#Unos cuantos casos sobre soluciones posibles y soluciones varias:
# Primer ejemplo del pdf, un caso bastante complejo
python3 CSPParking.py CSP-tests/parking01.dat
# Un parking pequeño con solo 3 soluciones
python3 CSPParking.py CSP-tests/parking02.dat
# Otro caso con 38 soluciones completo pero mucho más corto que el primero.
python3 CSPParking.py CSP-tests/parking03.dat
# Caso de prueba para un parking con una sola fila y múltiples plazas con conexión eléctrica:
python3 CSPParking.py CSP-tests/parking04.dat
# Caso de prueba para un parking sin plazas eléctricas ni vehículos con congelador:
python3 CSPParking.py CSP-tests/parking05.dat
# Caso de prueba con mas ambulancias con congelador que plazas electricas
python3 CSPParking.py CSP-tests/parking06.dat
# Caso de prueba que obliga a infringir la segunda restriccion
python3 CSPParking.py CSP-tests/parking07.dat
echo "Ejecución de casos de prueba completada."