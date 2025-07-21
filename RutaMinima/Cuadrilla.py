import heapq

def dijkstra(graph, start, end):
    # Inicializar distancias
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    # Cola de prioridad: (distancia, nodo)
    pq = [(0, start)]
    
    # Para reconstruir el camino
    previous = {node: None for node in graph}
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        # Si llegamos al destino
        if current_node == end:
            break
            
        # Si ya encontramos una ruta más corta, continuar
        if current_distance > distances[current_node]:
            continue
            
        # Examinar vecinos
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            # Si encontramos una ruta más corta
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    
    return distances, previous

def get_path(previous, start, end):
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path if path[0] == start else []

# Definir el grafo con las distancias dadas
# a=16, b=17, c=9, d=4, e=3, f=10, g=13, h=4, i=2
graph = {
    1: {2: 16, 3: 17},  # zona 1 conectada a zona 2 (a=16) y zona 3 (b=17)
    2: {1: 16, 3: 9, 4: 4, 6: 13},  # zona 2 conectada a zona 1, 3 (c=9), 4 (d=4), 6 (g=13)
    3: {1: 17, 2: 9, 5: 3},  # zona 3 conectada a zona 1, 2, 5 (e=3)
    4: {2: 4, 5: 10, 6: 4},  # zona 4 conectada a zona 2, 5 (f=10), 6 (h=4)
    5: {3: 3, 4: 10, 6: 2},  # zona 5 conectada a zona 3, 4, 6 (i=2)
    6: {2: 13, 4: 4, 5: 2}   # zona 6 conectada a zona 2, 4, 5
}

# Encontrar la ruta más corta de zona 1 a zona 6
distances, previous = dijkstra(graph, 1, 6)
path = get_path(previous, 1, 6)

print(f"Tiempo mínimo para llegar a la zona 6: {distances[6]} minutos")
print(f"Ruta óptima: {' -> '.join(map(str, path))}")

# Verificar el cálculo paso a paso
print("\nDetalles de la ruta:")
total_time = 0
for i in range(len(path) - 1):
    from_zone = path[i]
    to_zone = path[i + 1]
    time = graph[from_zone][to_zone]
    total_time += time
    print(f"Zona {from_zone} -> Zona {to_zone}: {time} minutos")

print(f"\nTiempo total: {total_time} minutos")