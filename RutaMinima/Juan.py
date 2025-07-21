import heapq
from collections import defaultdict

def dijkstra_con_parada_obligatoria():
    # Definir el grafo con los costos de cada trayecto
    grafo = {
        'A': {'B': 2, 'C': 5, 'D': 4},
        'B': {'E': 7, 'F': 4, 'G': 6},
        'C': {'E': 3, 'F': 2, 'G': 4},
        'D': {'E': 4, 'F': 1, 'G': 5},
        'E': {'H': 1, 'I': 4},
        'F': {'H': 6, 'I': 3},
        'G': {'H': 3, 'I': 3},
        'H': {'J': 2},
        'I': {'J': 1}
    }
    
    # Fase 1: Encontrar el costo mínimo de A a B (obligatorio)
    # En este caso es directo: A -> B = 2
    costo_A_B = 2
    
    # Fase 2: Encontrar el costo mínimo de B a J usando Dijkstra
    def dijkstra(inicio, destino):
        distancias = defaultdict(lambda: float('inf'))
        distancias[inicio] = 0
        cola = [(0, inicio)]
        visitados = set()
        
        while cola:
            dist_actual, nodo_actual = heapq.heappop(cola)
            
            if nodo_actual in visitados:
                continue
                
            visitados.add(nodo_actual)
            
            if nodo_actual == destino:
                return dist_actual
            
            for vecino, peso in grafo.get(nodo_actual, {}).items():
                if vecino not in visitados:
                    nueva_dist = dist_actual + peso
                    if nueva_dist < distancias[vecino]:
                        distancias[vecino] = nueva_dist
                        heapq.heappush(cola, (nueva_dist, vecino))
        
        return float('inf')
    
    # Calcular el costo mínimo de B a J
    costo_B_J = dijkstra('B', 'J')
    
    # Costo total de la ruta A -> B -> ... -> J
    costo_total = costo_A_B + costo_B_J
    
    print(f"Costo A -> B: {costo_A_B}")
    print(f"Costo mínimo B -> J: {costo_B_J}")
    print(f"Costo total mínimo: {costo_total}")
    
    # Encontrar la ruta específica
    def encontrar_ruta(inicio, destino):
        distancias = defaultdict(lambda: float('inf'))
        predecesores = {}
        distancias[inicio] = 0
        cola = [(0, inicio)]
        visitados = set()
        
        while cola:
            dist_actual, nodo_actual = heapq.heappop(cola)
            
            if nodo_actual in visitados:
                continue
                
            visitados.add(nodo_actual)
            
            if nodo_actual == destino:
                # Reconstruir ruta
                ruta = []
                actual = destino
                while actual in predecesores:
                    ruta.append(actual)
                    actual = predecesores[actual]
                ruta.append(inicio)
                return list(reversed(ruta)), dist_actual
            
            for vecino, peso in grafo.get(nodo_actual, {}).items():
                if vecino not in visitados:
                    nueva_dist = dist_actual + peso
                    if nueva_dist < distancias[vecino]:
                        distancias[vecino] = nueva_dist
                        predecesores[vecino] = nodo_actual
                        heapq.heappush(cola, (nueva_dist, vecino))
        
        return None, float('inf')
    
    ruta_B_J, _ = encontrar_ruta('B', 'J')
    ruta_completa = ['A'] + ruta_B_J
    
    print(f"Ruta óptima: {' -> '.join(ruta_completa)}")
    print(f"Respuesta (redondeada a 1 decimal): {round(costo_total, 1)}")
    
    return round(costo_total, 1)

# Ejecutar la función
resultado = dijkstra_con_parada_obligatoria()