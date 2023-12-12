import csv
import heapq
import sys
import time

# Definimos el mapa como una variable global
mapa = []

class Estado:
    def __init__(self, ubicacion, energia, pacientes_a_bordo, pacientes_restantes):
        self.ubicacion = ubicacion
        self.energia = energia
        self.pacientes_a_bordo = pacientes_a_bordo
        self.pacientes_restantes = pacientes_restantes
    
    def es_meta(self):
        return not self.pacientes_restantes and not self.pacientes_a_bordo and self.ubicacion == encontrar_p(mapa)

    # devuelve una lista de ubicaciones a las que puedes moverte desde `self.ubicacion`
    def ubicaciones_adyacentes(self):
        adyacentes = []
        x, y = self.ubicacion
        # Asumimos que 'mapa' es una lista de listas que representa tu mapa
        # y que 'libre' es una función que devuelve True si la ubicación está libre
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Movimientos posibles: arriba, abajo, izquierda, derecha
            nueva_x, nueva_y = x + dx, y + dy
            if 0 <= nueva_x < len(mapa) and 0 <= nueva_y < len(mapa[0]) and libre(mapa[nueva_x][nueva_y]):
                adyacentes.append((nueva_x, nueva_y))
        return adyacentes
    
    def agregar_paciente_a_bordo(self, paciente):
        if not paciente:
            return False
        tipo, _ = paciente
        if len(self.pacientes_a_bordo) >= 10:
            return False 
        # Verificar si el paciente es contagioso y ya hay pacientes contagiosos a bordo
        if tipo == 'C' and sum(1 for tipo2, _ in self.pacientes_a_bordo if tipo2 == 'C') >= 2:
            return False  # No se puede agregar paciente contagioso si ya hay 2 contagiosos a bordo
        if tipo == 'N' and any(tipo3 == 'C' for tipo3, _ in self.pacientes_a_bordo):
            return False
        # Verificar si las plazas especiales para contagiosos están ocupadas por no contagiosos
        if tipo == 'N' and sum(1 for tipo2, _ in self.pacientes_a_bordo if tipo2 == 'N') >= 8 and any(tipo3 == 'C' for tipo3, _ in self.pacientes_a_bordo):
            # Hay al menos dos plazas especiales disponibles
            return False  # No se puede agregar paciente no contagioso si ya hay no contagiosos a bordo
        #entonces di que si se puede agregar pacientes
        return True

    def pacientes_en(self, ubicacion):
        x, y = ubicacion
        if mapa[x][y] == 'N' and 'N' in self.pacientes_restantes and ubicacion in self.pacientes_restantes['N'] and not any(tipo3 == 'C' for tipo3, _ in self.pacientes_a_bordo):
            return ('N', ubicacion)
        elif mapa[x][y] == 'C'  and 'C' in self.pacientes_restantes and ubicacion in self.pacientes_restantes['C']:
            return ('C', ubicacion)
        return None


    def copiar_pacientes_restantes(self, excluir_paciente=None):
    # Devuelve una copia independiente del diccionario de pacientes restantes
        copia_pacientes = {tipo: ubicaciones.copy() for tipo, ubicaciones in self.pacientes_restantes.items()}
        if excluir_paciente:
            tipo_excluir, ubicacion_excluir = excluir_paciente
            if tipo_excluir in copia_pacientes and ubicacion_excluir in copia_pacientes[tipo_excluir]:
                copia_pacientes[tipo_excluir].remove(ubicacion_excluir)
                if not copia_pacientes[tipo_excluir]:
                    del copia_pacientes[tipo_excluir]
        return copia_pacientes

    def centro_atencion_en(self, ubicacion):
        x, y = ubicacion
        if mapa[x][y] == 'CN':
            return ('CN', ubicacion)
        elif mapa[x][y] == 'CC':
            return ('CC', ubicacion)
        return None
    def dejar_en_centro_atencion(self, centro_atencion):
        if not centro_atencion:
            return False
        tipo, ubicacion = centro_atencion
        if any(tipo2 == 'C' for tipo2, _ in self.pacientes_a_bordo) and tipo == 'CN':
            return False
        if not any(tipo2 == 'C' for tipo2, _ in self.pacientes_a_bordo) and tipo == 'CC':
            return False
        return True
    def eliminar_pacientes(self, centro_atencion):
        tipo, ubicacion = centro_atencion
        if tipo == 'CC':
            nuevos_pacientes_a_bordo = [p for p in self.pacientes_a_bordo if p[0] != 'C']
        elif tipo == 'CN':
            nuevos_pacientes_a_bordo = []
        return nuevos_pacientes_a_bordo

    def sucesores(self):
        sucesores = []
        for ubicacion in self.ubicaciones_adyacentes():
            if self.energia > 0:  # Solo puedes moverte si tienes energía
                paciente = self.pacientes_en(ubicacion)
                centro_atencion = self.centro_atencion_en(ubicacion)
                energia_nueva = self.energia - 1 if energia_handler(ubicacion) else 50
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
        return (self.ubicacion == otro.ubicacion and self.energia == otro.energia and 
                self.pacientes_a_bordo == otro.pacientes_a_bordo and self.pacientes_restantes == otro.pacientes_restantes)
    def __hash__(self):
        return hash((self.ubicacion, self.energia, tuple(self.pacientes_a_bordo), tuple(self.pacientes_restantes)))
    def __str__(self):
        return f"Ubicacion: {self.ubicacion}, Energia: {self.energia}, Pacientes a Bordo: {self.pacientes_a_bordo}, Pacientes Restantes: {self.pacientes_restantes}"
        # return f"{self.ubicacion} :{mapa[self.ubicacion[0]][self.ubicacion[1]]}: {self.energia}"
    def __lt__(self, otro):
        # Implementa tu lógica de comparación aquí. Por ejemplo, podrías comparar los estados
        # basándote en la energía:
        return self.energia < otro.energia




def energia_handler(ubicacion):
    x, y = ubicacion
    return mapa[x][y] != 'P'

def libre(celda):
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


def heuristica(estado):
    # Esta función debería devolver una estimación del coste desde el estado hasta el estado objetivo
    # Aquí te dejo un ejemplo genérico, pero tendrás que adaptarlo a tu problema
    #return estado.energia
    # Implementa tu función heurística aquí
    # Puedes probar con la distancia Manhattan, por ejemplo
    # return sum(abs(self.ubicacion[0] - x) + abs(self.ubicacion[1] - y) for x, y in ubicaciones_pacientes)
    return 0

def encontrar_p(mapa):
    for i, fila in enumerate(mapa):
        for j, celda in enumerate(fila):
            if celda == 'P':
                return (i, j)
    return None

def main():
    # Captura el tiempo de inicio
    tiempo_inicio = time.time()

    if len(sys.argv) != 3:
        print("Uso: python ASTARTraslados.py <path mapa.csv> <num-h>")
        return
    global mapa
    mapa = leer_mapa(sys.argv[1])
    estado_inicial = Estado(ubicacion = encontrar_p(mapa), energia=50, pacientes_a_bordo=[], pacientes_restantes=inicializar_pacientes_restantes(mapa))
    solucion = a_estrella(estado_inicial, heuristica)
    if solucion is not None:
        for s in solucion:
            print(s)
    # Captura el tiempo de finalización
    tiempo_fin = time.time()

    # Calcula el tiempo total
    tiempo_total = tiempo_fin - tiempo_inicio

    print(f"El programa tardó {tiempo_total} segundos en ejecutarse.")

def a_estrella(estado_inicial, heuristica):
    ABIERTA = []
    CERRADA = set()
    EXITO = False
    g = {estado_inicial: 0}  # Creamos un diccionario para almacenar los costes g
    predecesores = {}  # Creamos un diccionario para almacenar los predecesores

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
                    h_s = heuristica(s)
                    f_s = g_s + h_s
                    # Si s no está en ABIERTA ni en CERRADA, lo insertamos en ABIERTA
                    if s not in CERRADA and s not in [estado for _, estado in ABIERTA]:
                        g[s] = g_s  # Actualizamos el coste g de s
                        predecesores[s] = N  # Guardamos N como el predecesor de s
                        heapq.heappush(ABIERTA, (f_s, s))
    if EXITO:
        return solucion
    else:
        return None  # Fracaso: no se ha encontrado ninguna solución

if __name__ == "__main__":
    main()