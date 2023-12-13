#!/bin/bash

# Probamos un mapa sin solucion que no expande ninguno nodo, da igual la heuristica
python3 ASTARTraslados.py ./ASTAR-tests/mapa_NS1.csv 1
# Probamos un mapa sin solucion que su meta final es inaccesible, da igual la heuristica
python3 ASTARTraslados.py ./ASTAR-tests/mapa_NS2.csv 1
# Probamos un mapa sin solucion que su unico paciente esta a mas de 50 de energia del parking, da igual la heuristica
python3 ASTARTraslados.py ./ASTAR-tests/mapa_NS3.csv 1
# Probamos unos mapas pequeños, 4x4 y 5x5
python3 ASTARTraslados.py ./ASTAR-tests/mapa_small.csv 1
python3 ASTARTraslados.py ./ASTAR-tests/mapa_small.csv 2
python3 ASTARTraslados.py ./ASTAR-tests/mapa_small2.csv 1
python3 ASTARTraslados.py ./ASTAR-tests/mapa_small2.csv 2
# Probamos unos mapas medianos, 6x6 y 7x7
python3 ASTARTraslados.py ./ASTAR-tests/mapa_mid.csv 1
python3 ASTARTraslados.py ./ASTAR-tests/mapa_mid2.csv 1
python3 ASTARTraslados.py ./ASTAR-tests/mapa_mid.csv 2
python3 ASTARTraslados.py ./ASTAR-tests/mapa_mid2.csv 2
# Probamos el mapa grande, 10x10
python3 ASTARTraslados.py ./ASTAR-tests/mapa_big.csv 1
python3 ASTARTraslados.py ./ASTAR-tests/mapa_big.csv 2