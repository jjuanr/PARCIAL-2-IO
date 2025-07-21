class UnionFind:
    def __init__(self, n):
        self.parent = {i: i for i in range(1, n + 1)}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)
        if rx != ry:
            self.parent[rx] = ry
            return True
        return False

def kruskal_mst(edges, num_nodes):
    edges.sort(key=lambda x: x[2])  # Ordenar por peso
    uf = UnionFind(num_nodes)
    mst_weight = 0
    mst_edges = []

    for u, v, weight in edges:
        if uf.union(u, v):
            mst_weight += weight
            mst_edges.append((u, v, weight))
    
    return mst_weight, mst_edges

# Lista de aristas (u, v, peso)
edges = [
    (1, 2, 16), #1 y 2 estan conectados por 16
    (1, 3, 17), 
    (1, 5, 9),
    (2, 3, 3), #Como ya hay 1 y 2, no se repite el 2 y 1
    (2, 4, 2),
    (2, 5, 10),
    (3, 4, 13),
    (3, 5, 4),
    (4, 5, 4)
]

num_nodes = 5 #Numero de nodos q hay
peso_total, aristas_usadas = kruskal_mst(edges, num_nodes)

print(f"Peso mínimo total del cableado: {peso_total}")
print("Conexiones usadas:")
for u, v, w in aristas_usadas:
    print(f"{u} - {v} (peso {w})")