import numpy as np
from scipy.optimize import linprog

# Definir el problema de transbordo
# Variables de decisión: x_ij representa el flujo del nodo i al nodo j

# Costos por unidad de flujo
costos = {
    'a': 19,  # Ref.1 -> cc.1
    'b': 29,  # Ref.1 -> cc.2
    'c': 64,  # Ref.2 -> cc.1
    'd': 19,  # Ref.2 -> cc.2
    'e': 59,  # cc.1 -> Bari
    'f': 63,  # cc.1 -> Porto
    'g': 39,  # cc.1 -> Vita
    'h': 12,  # cc.1 -> Siena
    'i': 46,  # cc.2 -> Bari
    'k': 34,  # cc.2 -> Porto
    'm': 58,  # cc.2 -> Vita
    'n': 32   # cc.2 -> Siena
}

# Oferta y demanda
oferta_ref1 = 600
oferta_ref2 = 400
demanda_bari = 200
demanda_porto = 150
demanda_vita = 350
demanda_siena = 300

# Variables: [a, b, c, d, e, f, g, h, i, k, m, n]
# Función objetivo: minimizar costo total
c = [19, 29, 64, 19, 59, 63, 39, 12, 46, 34, 58, 32]

# Restricciones de igualdad (Ax = b)
# Conservación de flujo en cada nodo

# Nodo Ref.1: a + b = 600
# Nodo Ref.2: c + d = 400
# Nodo cc.1: e + f + g + h = a + c
# Nodo cc.2: i + k + m + n = b + d
# Nodo Bari: e + i = 200
# Nodo Porto: f + k = 150
# Nodo Vita: g + m = 350
# Nodo Siena: h + n = 300

A_eq = [
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Ref.1
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # Ref.2
    [-1, 0, -1, 0, 1, 1, 1, 1, 0, 0, 0, 0],  # cc.1
    [0, -1, 0, -1, 0, 0, 0, 0, 1, 1, 1, 1],  # cc.2
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],  # Bari
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],  # Porto
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],  # Vita
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]   # Siena
]

b_eq = [600, 400, 0, 0, 200, 150, 350, 300]

# Restricciones de no negatividad (bounds)
bounds = [(0, None) for _ in range(12)]

# Resolver el problema
resultado = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

if resultado.success:
    print("Solución óptima encontrada:")
    print(f"Costo mínimo: {resultado.fun:.1f}")
    
    variables = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'm', 'n']
    print("\nFlujos óptimos:")
    for i, var in enumerate(variables):
        if resultado.x[i] > 0.001:  # Solo mostrar flujos positivos
            print(f"{var}: {resultado.x[i]:.1f}")
    
    print(f"\nRespuesta: {resultado.fun:.1f}")
else:
    print("No se encontró solución óptima")