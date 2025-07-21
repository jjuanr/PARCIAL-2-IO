from collections import deque, defaultdict

def edmonds_karp_no_inversos(grafo, origen, sumidero):
    flujo_total = 0
    capacidad = defaultdict(dict)
    originales = set()

    # Crear copia de capacidades y registrar solo las aristas originales (permitidas)
    for u in grafo:
        for v in grafo[u]:
            capacidad[u][v] = grafo[u][v]
            originales.add((u, v))
            if v not in capacidad or u not in capacidad[v]:
                capacidad[v][u] = 0  # residuales, pero no permitidas en BFS

    while True:
        padre = {}
        visitado = set()
        cola = deque([origen])
        visitado.add(origen)

        # BFS restringido SOLO a aristas originales
        while cola:
            u = cola.popleft()
            for v in capacidad[u]:
                if v not in visitado and capacidad[u][v] > 0 and (u, v) in originales:
                    padre[v] = u
                    visitado.add(v)
                    cola.append(v)
                    if v == sumidero:
                        break
        if sumidero not in padre:
            break

        # Encontrar flujo mínimo
        f = float('inf')
        v = sumidero
        camino = []
        while v != origen:
            u = padre[v]
            f = min(f, capacidad[u][v])
            camino.append((u, v))
            v = u

        # Mostrar camino válido
        print(f"Camino usado: {list(reversed(camino))}, flujo: {f}")

        # Actualizar capacidades (incluye residuales para bloquear más adelante)
        v = sumidero
        while v != origen:
            u = padre[v]
            capacidad[u][v] -= f
            capacidad[v][u] += f  # esta se usará para bloquear loops, no para buscar más camino
            v = u

        flujo_total += f

    return flujo_total

# Definir el grafo original (calles unidireccionales)
grafo = {
    'ai': {'b': 6, 'c': 4, 'd': 3}, #El 1 va a 2 con un valor de 16, 1 va a 3 con valor de 20 y 1 va a 4 con valor de 6
    'b': {'e': 4},
    'c': {'d': 3, 'e': 1, 'f': 3},
    'd': {'f': 4},
    'e': {'gt': 3},
    'f': {'gt': 9},
    'gt': {}
}

# Ejecutar algoritmo corregido
print("\nFlujo máximo:", edmonds_karp_no_inversos(grafo, 'ai', 'gt')) #Poner el primer y ultimo grafo 