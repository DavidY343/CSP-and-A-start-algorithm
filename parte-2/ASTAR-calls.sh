#!/bin/sh

# Probamos un mapa sin solucion que no expande ninguno nodo, da igual la heuristica
python3 ASTARTraslados.py ASTAR-tests/mapa_NS1.csv 1
# Probamos un mapa sin solucion que su meta final es inaccesible, da igual la heuristica
python3 ASTARTraslados.py ASTAR-tests/mapa_NS2.csv 2
# Probamos un mapa sin solucion que su unico paciente esta a mas de 50 de energia del parking, da igual la heuristica
python3 ASTARTraslados.py ASTAR-tests/mapa_NS3.csv 3
# Probamos unos mapas pequeños, 4x4 y 5x5 y con pocos pacientes
python3 ASTARTraslados.py ASTAR-tests/mapa_small.csv 1
python3 ASTARTraslados.py ASTAR-tests/mapa_small.csv 2
python3 ASTARTraslados.py ASTAR-tests/mapa_small.csv 3
python3 ASTARTraslados.py ASTAR-tests/mapa_small2.csv 1
python3 ASTARTraslados.py ASTAR-tests/mapa_small2.csv 2
python3 ASTARTraslados.py ASTAR-tests/mapa_small2.csv 3
python3 ASTARTraslados.py ASTAR-tests/mapa_small3.csv 1
python3 ASTARTraslados.py ASTAR-tests/mapa_small3.csv 2
python3 ASTARTraslados.py ASTAR-tests/mapa_small3.csv 3
# Probamos unos mapas medianos, 6x6 y 7x7
python3 ASTARTraslados.py ASTAR-tests/mapa_mid3.csv 4
python3 ASTARTraslados.py ASTAR-tests/mapa_mid.csv 4
python3 ASTARTraslados.py ASTAR-tests/mapa_mid2.csv 4
# Probamos el mapa grande, 10x10, 20x20 y 15x15, probamos con la mejor heuristica que tenemos
# python3 ASTARTraslados.py ASTAR-tests/mapa_big.csv 1
python3 ASTARTraslados.py ASTAR-tests/mapa_big.csv 4
python3 ASTARTraslados.py ASTAR-tests/mapa_big2.csv 4
python3 ASTARTraslados.py ASTAR-tests/mapa_extra_big.csv 4
echo "Ejecución de casos de prueba completada."