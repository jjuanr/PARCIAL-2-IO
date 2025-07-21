import heapq
from collections import defaultdict

def encontrar_ruta_minima():
    # Crear el grafo con los costos de seguros
    grafo = defaultdict(list)
    
    # Desde A
    grafo['A'].append(('B', 2))
    grafo['A'].append(('C', 4))
    grafo['A'].append(('D', 4))
    
    # Desde B
    grafo['B'].append(('E', 7))
    grafo['B'].append(('F', 4))
    grafo['B'].append(('G', 6))
    
    # Desde C
    grafo['C'].append(('E', 3))
    grafo['C'].append(('F', 2))
    grafo['C'].append(('G', 4))
    
    # Desde D
    grafo['D'].append(('E', 4))
    grafo['D'].append(('F', 1))
    grafo['D'].append(('G', 5))
    
    # Desde E
    grafo['E'].append(('H', 1))
    grafo['E'].append(('I', 4))
    
    # Desde F
    grafo['F'].append(('H', 6))
    grafo['F'].append(('I', 3))
    
    # Desde G
    grafo['G'].append(('H', 3))
    grafo['G'].append(('I', 3))
    
    # Desde H
    grafo['H'].append(('J', 3))
    
    # Desde I
    grafo['I'].append(('J', 4))
    
    # Algoritmo de Dijkstra
    distancias = defaultdict(lambda: float('inf'))
    distancias['A'] = 0
    rutas = defaultdict(list)
    rutas['A'] = ['A']
    
    # Cola de prioridad: (distancia, ciudad)
    cola = [(0, 'A')]
    visitados = set()
    
    while cola:
        dist_actual, ciudad_actual = heapq.heappop(cola)
        
        if ciudad_actual in visitados:
            continue
            
        visitados.add(ciudad_actual)
        
        # Si llegamos a J, terminamos
        if ciudad_actual == 'J':
            break
            
        # Explorar vecinos
        for vecino, costo in grafo[ciudad_actual]:
            nueva_distancia = dist_actual + costo
            
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                rutas[vecino] = rutas[ciudad_actual] + [vecino]
                heapq.heappush(cola, (nueva_distancia, vecino))
    
    return distancias['J'], rutas['J']

# Ejecutar el algoritmo
costo_minimo, ruta_optima = encontrar_ruta_minima()

print(f"Ruta óptima: {' -> '.join(ruta_optima)}")
print(f"Costo mínimo del seguro: {costo_minimo}")
print(f"Respuesta redondeada a 1 cifra decimal: {costo_minimo:.1f}")

# Verificar manualmente algunas rutas posibles
print("\nVerificación de rutas:")
print("A -> D -> F -> I -> J:", 4 + 1 + 3 + 4, "= 12")
print("A -> C -> E -> H -> J:", 4 + 3 + 1 + 3, "= 11")
print("A -> C -> F -> I -> J:", 4 + 2 + 3 + 4, "= 13")