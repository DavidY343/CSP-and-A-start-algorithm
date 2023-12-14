import csv
import heapq
import sys
import time
import math

# Definimos el mapa como una variable global
mapa = []

factor_heuristico = 100

class Estado:
    def __init__(self, ubicacion, energia, pacientes_a_bordo, pacientes_restantes):
        self.ubicacion = ubicacion
        self.energia = energia
        self.pacientes_a_bordo = pacientes_a_bordo
        self.pacientes_restantes = pacientes_restantes
    
    def es_meta(self):
        """Decimos que el estado solucion tiene 0 pacientes restantes, 0 pacientes a bordo y
        la ubicacion se encuentra en el parking"""
        return not self.pacientes_restantes and not self.pacientes_a_bordo and self.ubicacion == encontrar_p()

    def ubicaciones_adyacentes(self):
        """devuelve una lista de ubicaciones a las que puedes moverte desde `self.ubicacion`"""
        adyacentes = []
        x, y = self.ubicacion
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Movimientos posibles: arriba, abajo, izquierda, derecha
            nueva_x, nueva_y = x + dx, y + dy
            if 0 <= nueva_x < len(mapa) and 0 <= nueva_y < len(mapa[0]) and libre(mapa[nueva_x][nueva_y]):
                adyacentes.append((nueva_x, nueva_y))
        return adyacentes
    
    def agregar_paciente_a_bordo(self, paciente):
        """una funcion booleana que te dice si se puede recoger al paciente al estar en esa casilla"""
        if not paciente:
            return False
        tipo, _ = paciente
        # No puedes tener mas de 10 pacientes a bordo
        if len(self.pacientes_a_bordo) >= 10:
            return False 
        # Verificar si el paciente es contagioso y ya hay pacientes contagiosos a bordo
        if tipo == 'C' and sum(1 for tipo2, _ in self.pacientes_a_bordo if tipo2 == 'C') >= 2:
            return False
        # Verificar si el paciente es no contagioso y ya hay pacientes contagiosos a bordo
        if tipo == 'N' and any(tipo3 == 'C' for tipo3, _ in self.pacientes_a_bordo):
            return False
        # Verificar si las plazas especiales para contagiosos están ocupadas por no contagiosos
        if tipo == 'N' and sum(1 for tipo2, _ in self.pacientes_a_bordo if tipo2 == 'N') >= 8 and any(tipo3 == 'C' for tipo3, _ in self.pacientes_a_bordo):
            return False
        # Entonces di que si se puede agregar pacientes
        return True

    def pacientes_en(self, ubicacion):
        """Ver si hay un paciente en la casilla y si se pueden recoger"""
        x, y = ubicacion
        if mapa[x][y] == 'N' and 'N' in self.pacientes_restantes and ubicacion in self.pacientes_restantes['N'] and not any(tipo3 == 'C' for tipo3, _ in self.pacientes_a_bordo):
            return ('N', ubicacion)
        elif mapa[x][y] == 'C'  and 'C' in self.pacientes_restantes and ubicacion in self.pacientes_restantes['C'] and sum(1 for tipo2, _ in self.pacientes_a_bordo if tipo2 == 'C') < 2:
            return ('C', ubicacion)
        return None

    def copiar_pacientes_restantes(self, excluir_paciente=None):
        """Devuelve una copia del diccionario de pacientes restantes con o sin excluir pacientes"""
        copia_pacientes = {tipo: ubicaciones.copy() for tipo, ubicaciones in self.pacientes_restantes.items()}
        if excluir_paciente:
            tipo_excluir, ubicacion_excluir = excluir_paciente
            if tipo_excluir in copia_pacientes and ubicacion_excluir in copia_pacientes[tipo_excluir]:
                copia_pacientes[tipo_excluir].remove(ubicacion_excluir)
                if not copia_pacientes[tipo_excluir]:
                    del copia_pacientes[tipo_excluir]
        return copia_pacientes

    def centro_atencion_en(self, ubicacion):
        """Ver si hay un centro de atencion en la casilla y si se pueden recoger"""
        x, y = ubicacion
        if mapa[x][y] == 'CN':
            return ('CN', ubicacion)
        elif mapa[x][y] == 'CC':
            return ('CC', ubicacion)
        return None

    def dejar_en_centro_atencion(self, centro_atencion):
        """una funcion booleana que te dice si se puede dejar al paciente en la casilla de centro de atencion"""
        if not centro_atencion:
            return False
        tipo, ubicacion = centro_atencion
        if any(tipo2 == 'C' for tipo2, _ in self.pacientes_a_bordo) and tipo == 'CN':
            return False
        if not any(tipo2 == 'C' for tipo2, _ in self.pacientes_a_bordo) and tipo == 'CC':
            return False
        return True

    def eliminar_pacientes(self, centro_atencion):
        """Devuelve una copia del diccionario de pacientes a bordor con o sin excluir pacientes"""
        tipo, ubicacion = centro_atencion
        if tipo == 'CC':
            nuevos_pacientes_a_bordo = [p for p in self.pacientes_a_bordo if p[0] != 'C']
        elif tipo == 'CN':
            nuevos_pacientes_a_bordo = []
        return nuevos_pacientes_a_bordo

    def energia_en(self, ubicacion):
        """Ver el coste de energia en la casilla"""
        x, y = ubicacion
        costo_transicion = 1  # Costo por defecto de transición
        if mapa[x][y].isdigit():
            costo_transicion = int(mapa[x][y])
        return costo_transicion
    
    def sucesores(self):
        """Crea los sucesores de un estado, cumpliendo todas las restricciones del proyecto"""
        sucesores = []
        for ubicacion in self.ubicaciones_adyacentes():
            if self.energia > 0:  # Solo puedes moverte si tienes energía
                paciente = self.pacientes_en(ubicacion)
                centro_atencion = self.centro_atencion_en(ubicacion)

                energia_nueva = self.energia - self.energia_en(ubicacion) if energia_handler(ubicacion) else 50
                if self.agregar_paciente_a_bordo(paciente):
                    nuevos_pacientes_a_bordo = list(self.pacientes_a_bordo) + [paciente] 
                else:
                    if self.dejar_en_centro_atencion(centro_atencion):
                        nuevos_pacientes_a_bordo = self.eliminar_pacientes(centro_atencion)
                    else:
                        nuevos_pacientes_a_bordo = list(self.pacientes_a_bordo)
                pacientes_restantes_nuevos = self.copiar_pacientes_restantes(excluir_paciente=paciente)
                paciente = self.pacientes_en(ubicacion)
                nuevo_estado = Estado(
                    ubicacion, 
                    energia_nueva, 
                    nuevos_pacientes_a_bordo,
                    pacientes_restantes_nuevos
                )
                sucesores.append(nuevo_estado)

        return sucesores

    def __eq__(self, otro):
        return (self.ubicacion == otro.ubicacion and 
                self.pacientes_a_bordo == otro.pacientes_a_bordo and self.pacientes_restantes == otro.pacientes_restantes)
    def __hash__(self):
        return hash((self.ubicacion, self.energia, tuple(self.pacientes_a_bordo), tuple(self.pacientes_restantes)))
    def __str__(self):
        #return f"Ubicacion: {self.ubicacion}, Energia: {self.energia}, Pacientes a Bordo: {self.pacientes_a_bordo}, Pacientes Restantes: {self.pacientes_restantes}"
        return f"({self.ubicacion[0]},{self.ubicacion[0]}) :{mapa[self.ubicacion[0]][self.ubicacion[1]]}: {self.energia}"

    def __lt__(self, otro):
        return ((50 - self.energia) < (50 - otro.energia))

# Funciones del programa
def energia_handler(ubicacion):
    """Funcion booleana para saber si estoy en el parking"""
    x, y = ubicacion
    return mapa[x][y] != 'P'

def libre(celda):
    """Funcion booleana para saber si puede transitar por la casilla"""
    return celda != 'X'

def inicializar_pacientes_restantes(mapa):
    pacientes_restantes = {}
    for i, fila in enumerate(mapa):
        for j, celda in enumerate(fila):
            if celda in ['N', 'C']:
                tipo_paciente = celda
                if tipo_paciente not in pacientes_restantes:
                    pacientes_restantes[tipo_paciente] = []
                pacientes_restantes[tipo_paciente].append((i, j))
    return pacientes_restantes

def leer_mapa(nombre_archivo):
    mapa = []
    with open(nombre_archivo, 'r') as archivo:
        lector = csv.reader(archivo, delimiter=';')
        for fila in lector:
            mapa.append(fila)
    return mapa

def distancia(pos_ini, pos_fin):
    x, y = pos_fin
    v, w = pos_ini
    return pow(pow(abs(v - x), 2) + pow(abs(w - y), 2), 0.5)

def todos_los_centros():
    todos_los_centros = {}
    for x, fila in enumerate(mapa):
        for y, valor in enumerate(fila):
            if valor in ['CN', 'CC']:
                if valor not in todos_los_centros:
                    todos_los_centros[valor] = []
                todos_los_centros[valor].append((x, y))
    return todos_los_centros

def min_centro_paciente(paciente_min_id, paciente_min_ubi):
    todos = todos_los_centros()
    centro_paciente = 'C' + paciente_min_id
    return min(distancia(paciente_min_ubi, centro) for centro in todos[centro_paciente])


def heuristica2(estado):
    """Esta función debería devolver una estimación del coste,
    calcular la distancia mínima desde la ubicación actual del vehículo hasta el domicilio más cercano de un paciente
     que aún no ha sido recogido y hasta su centro de atencion mas cercano"""
    dist_min_paciente = math.inf
    paciente_min_id = None
    paciente_min_ubi = None
    for tipo_paciente, ubicaciones in estado.pacientes_restantes.items():
        for paciente in ubicaciones:
            aux = distancia(estado.ubicacion, paciente)
            if aux < dist_min_paciente:
                dist_min_paciente = aux
                paciente_min_id = tipo_paciente
                paciente_min_ubi = paciente
    if paciente_min_id is not None and paciente_min_ubi is not None:
        return (dist_min_paciente + min_centro_paciente(paciente_min_id, paciente_min_ubi)) * factor_heuristico
    else:
        return (0)
def heuristica3(estado):
    """Esta función debería devolver una estimación del coste, calcular la distancia mínima 
    desde la ubicación actual del vehículo hasta el domicilio más cercano de un paciente que aún no ha sido recogido"""
    dist_min_paciente = math.inf
    paciente_min_id = None
    paciente_min_ubi = None
    for tipo_paciente, ubicaciones in estado.pacientes_restantes.items():
        for paciente in ubicaciones:
            aux = distancia(estado.ubicacion, paciente)
            if aux < dist_min_paciente:
                dist_min_paciente = aux
    if estado.pacientes_restantes is not None:
        return (dist_min_paciente) * factor_heuristico
    else:
        return (0)

def heuristica4(estado):
    """Estimación del costo considerando la distancia a los pacientes y la distribución de tipos de pacientes"""
    pacientes_C = estado.pacientes_restantes.get('C', [])
    pacientes_N = estado.pacientes_restantes.get('N', [])

    # Calcular la distancia promedio a los pacientes restantes
    distancia_promedio = 0
    total_pacientes = len(pacientes_C) + len(pacientes_N)

    if total_pacientes > 0:
        for paciente in pacientes_C + pacientes_N:
            distancia_promedio += distancia(estado.ubicacion, paciente)
        distancia_promedio /= total_pacientes

    # Priorizar la recogida de pacientes y su colocación en el destino adecuado
    estimacion_recogida = (total_pacientes * factor_heuristico) / (distancia_promedio + 1)

    return estimacion_recogida

def heuristica1(estado):
    """Esta función debería devolver una estimación del coste, 
    devuelve el numero de pacientes que quedan por recoger en cada estado multiplicado por un factor multiplicativo"""
    pacientes_C = 0
    pacientes_N = 0
    if (estado.pacientes_restantes.get('N', 0) != 0):
        pacientes_N = len(estado.pacientes_restantes['N'])
    if (estado.pacientes_restantes.get('C', 0) != 0):
        pacientes_C = len(estado.pacientes_restantes['C'])
    return ((pacientes_C + pacientes_N) * factor_heuristico)

def encontrar_p():
    """Encuentra el parking en el mapa"""
    for i, fila in enumerate(mapa):
        for j, celda in enumerate(fila):
            if celda == 'P':
                return (i, j)
    return None

def escribir_solucion(solucion, nombre_fichero):
    """Imprime el camino de la solucion"""
    with open(nombre_fichero, 'w') as f:
        if solucion is not None:
            for s in solucion:
                f.write(str(s) + '\n')

def escribir_estadisticas(tiempo_total, coste_total, longitud_plan, nodos_expandidos, nombre_fichero):
    """Imprime las estadisticas basicas de la solucion"""
    with open(nombre_fichero, 'w') as f:
        f.write(f'Tiempo total: {tiempo_total}\n')
        f.write(f'Coste total: {coste_total}\n')
        f.write(f'Longitud del plan: {longitud_plan}\n')
        f.write(f'Nodos expandidos: {nodos_expandidos}\n')

def comprobar_mapa(mapa):
    """Comprobamos que el mapa esta en el formato indicado"""
    p_contador = 0
    for _, fila in enumerate(mapa):
        for _, celda in enumerate(fila):
            if celda == 'P':
                p_contador += 1
            elif celda == 'N' or celda == 'CC' or celda == 'CN' or celda == 'X' or celda == 'C' or celda.isdigit():
                pass
            else:
                return False
    return p_contador == 1

def main():
    """La funcion que maneja todo: lee el mapa, crea el estado inicial, 
    llama a la funcion a_estrella e imprime las soluciones"""
    # Captura el tiempo de inicio
    tiempo_inicio = time.time()
    if len(sys.argv) != 3:
        print("Uso: python ASTARTraslados.py <path mapa.csv> <num-h>")
        return
    global mapa
    mapa = leer_mapa(sys.argv[1])
    if (comprobar_mapa(mapa) == False):
        print("Mapa no en el formato indicado")
        return 
    estado_inicial = Estado(ubicacion = encontrar_p(), energia=50, pacientes_a_bordo=[], pacientes_restantes=inicializar_pacientes_restantes(mapa))
    solucion, CERRADA, g = a_estrella(estado_inicial, sys.argv[2])

    tiempo_fin = time.time()
    archivo_salida = sys.argv[1].split('.')[0]
    nombre_fichero_solucion = f'{archivo_salida}-{sys.argv[2]}.output'
    escribir_solucion(solucion, nombre_fichero_solucion)    

    nombre_fichero_estadisticas = f'{archivo_salida}-{sys.argv[2]}.stats'
    tiempo_total = tiempo_fin - tiempo_inicio
    coste_total = 0
    longitud_plan = 0
    nodos_expandidos = 0
    if solucion is not None:
        coste_total = g[solucion[-1]] + 1
        longitud_plan = len(solucion)
    if CERRADA is not None:
        nodos_expandidos = len(CERRADA)
    escribir_estadisticas(tiempo_total, coste_total, longitud_plan, nodos_expandidos, nombre_fichero_estadisticas)

def a_estrella(estado_inicial, numero):
    """Algoritma basico a_estrella, g (diccionario de costes), predecesores para devovler la solucion, 
    una lista abierta y una cerrada para almacenar los estados"""
    ABIERTA = []
    CERRADA = set()
    EXITO = False
    g = {estado_inicial: 0}
    predecesores = {}

    # Inicializamos ABIERTA con el estado inicial
    heapq.heappush(ABIERTA, (0, estado_inicial))

    while ABIERTA and not EXITO:
        # Quitamos el primer nodo de ABIERTA
        f, N = heapq.heappop(ABIERTA)
        if N not in CERRADA:
            # Si N es el estado final, entonces hemos encontrado una solución
            if N.es_meta():
                EXITO = True
                solucion = []
                estado = N
                while estado is not None:  # Reconstruimos el camino desde N hasta el estado inicial
                    solucion.append(estado)
                    estado = predecesores.get(estado)
                solucion.reverse()  # Invertimos el camino para que vaya desde el estado inicial hasta N
            else:
                # Expandimos N y lo metemos en CERRADA
                CERRADA.add(N)
                S = N.sucesores()  # Generamos el conjunto de sucesores de N    
                for s in S:
                    costo_transicion = 1  # Costo por defecto de transición
                    if mapa[s.ubicacion[0]][s.ubicacion[1]].isdigit():
                        costo_transicion = int(mapa[s.ubicacion[0]][s.ubicacion[1]])
                    g_s = g[N] + costo_transicion
                    if (int(numero) == 1):
                        h_s = heuristica1(s)
                    elif (int(numero) == 2):
                        h_s = heuristica2(s)
                    elif (int(numero) == 4):
                        h_s = heuristica4(s)
                    else:
                        h_s = heuristica1(s)
                    f_s = g_s + h_s
                    # Si s no está en ABIERTA ni en CERRADA, lo insertamos en ABIERTA
                    if s not in CERRADA and s not in [estado for _, estado in ABIERTA]:
                        g[s] = g_s  # Actualizamos el coste g de s
                        predecesores[s] = N  # Guardamos N como el predecesor de s
                        heapq.heappush(ABIERTA, (f_s, s))
    if EXITO:
        return solucion, CERRADA, g
    else:
        return None, CERRADA, None  # Fracaso: no se ha encontrado ninguna solución

if __name__ == "__main__":
    main()
