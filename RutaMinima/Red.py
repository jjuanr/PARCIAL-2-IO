# Algoritmo de Dijkstra para encontrar la ruta mínima
import heapq

def dijkstra(grafo, origen, destino):
    # Inicializar distancias
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[origen] = 0
    
    # Cola de prioridad: (distancia, nodo)
    pq = [(0, origen)]
    visitados = set()
    
    while pq:
        dist_actual, nodo_actual = heapq.heappop(pq)
        
        if nodo_actual in visitados:
            continue
            
        visitados.add(nodo_actual)
        
        if nodo_actual == destino:
            return dist_actual
            
        for vecino, peso in grafo[nodo_actual].items():
            if vecino not in visitados:
                nueva_distancia = dist_actual + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    heapq.heappush(pq, (nueva_distancia, vecino))
    
    return float('inf')

# Definir el grafo basado en la imagen (corregido con todas las conexiones)
# a = 2, b = 1
a = 2
b = 1

grafo = {
    'O': {'A': 4, 'C': a, 'B': 3},  
    'A': {'D': 3, 'C': 5},  
    'B': {'C': 4, 'E': 6},  # Eliminé el duplicado 'E': 6
    'C': {'D': 2, 'F': 2, 'E': 5},  # Eliminé los duplicados 'F': 2, 'E': 5
    'D': {'G': 4, 'F': 2},  
    'E': {'F': 1, 'H': 2, 'I': 5}, 
    'F': {'G': 2, 'H': 5},  
    'G': {'T': 7},  
    'H': {'G': 2, 'T': b, 'I': 3},  
    'I': {'T': 4},
    'T': {}  # Nodo destino
}

# Encontrar la ruta mínima de O a T (no O a I)
distancia_minima = dijkstra(grafo, 'O', 'T')
print(f"La distancia mínima de O a T es: {distancia_minima}")

# Verificar algunas rutas posibles manualmente de O a T
rutas = [
    ('O-A-D-G-T', 4 + 3 + 4 + 7),  # = 18
    ('O-C-F-G-T', 2 + 2 + 2 + 7),  # = 13
    ('O-C-E-H-T', 2 + 5 + 2 + 1),  # = 10 (b=1)
    ('O-B-E-H-T', 3 + 6 + 2 + 1),  # = 12 (b=1)
    ('O-C-F-H-T', 2 + 2 + 5 + 1),  # = 10 (b=1)
    ('O-B-E-I-T', 3 + 6 + 5 + 4),  # = 18
    ('O-C-E-I-T', 2 + 5 + 5 + 4)   # = 16
]

print("\nVerificación de rutas de O a T:")
for ruta, distancia in rutas:
    print(f"{ruta}: {distancia}")