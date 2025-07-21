# Problema de ruta mínima - Escape de la mina
import heapq
import pulp

print("=== PROBLEMA DE RUTA MÍNIMA - ESCAPE DE LA MINA ===")
print("Encontrar la ruta más corta desde el nodo 0 hasta el nodo 8")
print()

# Parámetros dados
a, b = 4, 3

print("PARÁMETROS:")
print(f"a = {a}, b = {b}")
print()

# Definir el grafo basado en la imagen
# Lista de arcos (origen, destino, tiempo)
arcos = [
    # Desde nodo 0
    (0, 1, 4),    # 0 -> 1: 4 min
    (0, 2, 2),    # 0 -> 2: 2 min
    
    # Desde nodo 1
    (1, 2, 2),    # 1 -> 2: 4 min (rojo)
    (1, 3, 2),    # 1 -> 3: 2 min (amarillo)
    (1, 3, 7),    # 1 -> 5: 1 min (morado)
    
    # Desde nodo 2
    (2, 1, 4),    # 2 -> 1: 4 min (rojo, bidireccional)
    (2, 4, b),    # 2 -> 4: b min (rojo)
    (2, 3, 9),    # 2 -> 7: 2 min (verde)
    
    # Desde nodo 3
    (3, 5, 1),    # 3 -> 1: 7 min (amarillo, bidireccional)
    (3, 6, 5),    # 3 -> 4: 2 min (verde)
    
    # Desde nodo 4
    (4, 3, 2),    # 4 -> 3: 2 min (verde, bidireccional)
    (4, 6, 3),    # 4 -> 6: 3 min
    (4, 7, 2),    # 4 -> 7: 3 min (verde)
    (4, 5, 4),
    # Desde nodo 5
    (5, 6, 1),    # 5 -> 6: 1 min (morado)
    (5, 8, 5),    # 5 -> 8: 5 min (magenta)
    
    # Desde nodo 6
    (6, 5, 4),    # 6 -> 5: 4 min (azul)
    (6, 7, 3),    # 6 -> 7: 3 min (azul)
    (6, 8, 5),    # 6 -> 8: 5 min (azul)
    
    # Desde nodo 7
    (7, 8, a),    # 7 -> 8: b = 3 min
    
    (7, 6, 3),    # 8 -> 7: a = 4 min (magenta, bidireccional)
]

print("ESTRUCTURA DEL GRAFO:")
print("Nodos: 0, 1, 2, 3, 4, 5, 6, 7, 8")
print("Origen: 0, Destino: 8")
print()

print("ARCOS Y TIEMPOS:")
for origen, destino, tiempo in arcos:
    print(f"  {origen} -> {destino}: {tiempo} min")

# Crear grafo como diccionario de adyacencias
grafo = {}
for i in range(9):
    grafo[i] = []

for origen, destino, tiempo in arcos:
    grafo[origen].append((destino, tiempo))

print(f"\n=== ALGORITMO DE DIJKSTRA ===")

def dijkstra(grafo, inicio, fin):
    # Inicializar distancias
    distancias = {nodo: float('infinity') for nodo in range(9)}
    distancias[inicio] = 0
    
    # Para reconstruir la ruta
    predecesor = {nodo: None for nodo in range(9)}
    
    # Cola de prioridad: (distancia, nodo)
    cola = [(0, inicio)]
    visitados = set()
    
    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)
        
        if nodo_actual in visitados:
            continue
            
        visitados.add(nodo_actual)
        
        # Si llegamos al destino, terminamos
        if nodo_actual == fin:
            break
            
        # Revisar todos los vecinos
        for vecino, peso in grafo[nodo_actual]:
            if vecino not in visitados:
                nueva_distancia = distancia_actual + peso
                
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    predecesor[vecino] = nodo_actual
                    heapq.heappush(cola, (nueva_distancia, vecino))
    
    return distancias, predecesor

# Ejecutar Dijkstra
distancias, predecesor = dijkstra(grafo, 0, 8)

# Reconstruir la ruta más corta
def reconstruir_ruta(predecesor, inicio, fin):
    ruta = []
    actual = fin
    while actual is not None:
        ruta.append(actual)
        actual = predecesor[actual]
    ruta.reverse()
    return ruta if ruta[0] == inicio else []

ruta_optima = reconstruir_ruta(predecesor, 0, 8)
tiempo_minimo = distancias[8]

print(f"\n=== SOLUCIÓN ===")
print(f"Tiempo mínimo de escape: {tiempo_minimo:.1f} minutos")
print(f"Ruta óptima: {' -> '.join(map(str, ruta_optima))}")

# Mostrar detalles de la ruta
print(f"\nDETALLE DE LA RUTA:")
tiempo_acumulado = 0
for i in range(len(ruta_optima) - 1):
    nodo_actual = ruta_optima[i]
    nodo_siguiente = ruta_optima[i + 1]
    
    # Buscar el tiempo de este tramo
    tiempo_tramo = None
    for origen, destino, tiempo in arcos:
        if origen == nodo_actual and destino == nodo_siguiente:
            tiempo_tramo = tiempo
            break
    
    tiempo_acumulado += tiempo_tramo
    print(f"  {nodo_actual} -> {nodo_siguiente}: {tiempo_tramo} min (acumulado: {tiempo_acumulado} min)")

print(f"\n*** RESPUESTA FINAL: {tiempo_minimo:.1f} minutos ***")

# Verificación adicional con programación lineal (método alternativo)
print(f"\n=== VERIFICACIÓN CON PROGRAMACIÓN LINEAL ===")

# Crear modelo de flujo de costo mínimo
prob = pulp.LpProblem("Ruta_Minima", pulp.LpMinimize)

# Variables binarias para cada arco
x = {}
for origen, destino, tiempo in arcos:
    x[origen, destino] = pulp.LpVariable(f"x_{origen}_{destino}", cat='Binary')

# Función objetivo: minimizar tiempo total
prob += pulp.lpSum(tiempo * x[origen, destino] for origen, destino, tiempo in arcos)

# Restricciones de flujo
for nodo in range(9):
    flujo_entrante = pulp.lpSum(x[origen, nodo] for origen, destino, tiempo in arcos if destino == nodo)
    flujo_saliente = pulp.lpSum(x[nodo, destino] for origen, destino, tiempo in arcos if origen == nodo)
    
    if nodo == 0:  # Nodo origen
        prob += flujo_saliente - flujo_entrante == 1
    elif nodo == 8:  # Nodo destino
        prob += flujo_entrante - flujo_saliente == 1
    else:  # Nodos intermedios
        prob += flujo_entrante - flujo_saliente == 0

# Resolver
prob.solve(pulp.PULP_CBC_CMD(msg=0))

if prob.status == pulp.LpStatusOptimal:
    tiempo_pl = pulp.value(prob.objective)
    print(f"Tiempo mínimo (PL): {tiempo_pl:.1f} minutos")
    
    print("Arcos usados en la solución óptima:")
    for origen, destino, tiempo in arcos:
        if x[origen, destino].varValue > 0.5:
            print(f"  {origen} -> {destino}: {tiempo} min")
            
    if abs(tiempo_pl - tiempo_minimo) < 0.001:
        print("✓ Ambos métodos coinciden")
    else:
        print("⚠ Discrepancia entre métodos")
else:
    print("No se encontró solución con PL")