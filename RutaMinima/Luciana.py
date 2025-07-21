import heapq

def dijkstra(graph, start, end):
    # Inicializar distancias
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {}
    
    # Cola de prioridad: (distancia, nodo)
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        # Si llegamos al destino, retornamos la distancia
        if current_node == end:
            return current_distance
            
        # Explorar vecinos
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    
    return distances[end]

# Definir el grafo basado en la imagen
# a = 12, b = 2
a = 12
b = 2

graph = {
    'A': {'B': a, 'C': 4},  # a=12 km a B, 4 km a C
    'B': {'D': 5, 'E': 3},  # 5 km a D, 3 km a E
    'C': {'D': 2, 'F': 10}, # 2 km a D, 10 km a F
    'D': {},                # D no tiene salidas directas
    'E': {'G': b},          # b=2 km a G
    'F': {'G': 4},          # 4 km a G
    'G': {}                 # Destino
}

# Encontrar la distancia mínima de A a G
distancia_minima = dijkstra(graph, 'A', 'G')
print(f"La distancia mínima de A a G es: {distancia_minima:.1f} km")

# Verificar algunos caminos posibles para validar:
print("\nAlgunos caminos posibles:")
print(f"A -> B -> E -> G: {a + 3 + b} = {12 + 3 + 2} = 17 km")
print(f"A -> C -> F -> G: {4 + 10 + 4} = 18 km")
print("A -> C -> D -> E -> G: No es posible (D no tiene salidas)")