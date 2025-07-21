import numpy as np
from scipy.optimize import linprog

# Definir el valor de a
a = 7

# Definir la red de suministro
# Nodos: 1, 2, 3, 4, 5, 6, 7
# Oferta: Nodo 1 = 5000, Nodo 2 = 6000
# Demanda: Nodo 6 = 2000, Nodo 7 = 9000
# Total oferta = 11000, Total demanda = 11000 (balanceado)

# Variables de decisión: flujo en cada arco
# x_ij representa el flujo del nodo i al nodo j
# Arcos: (1,7), (1,3), (2,3), (2,6), (3,7), (3,5), (4,7), (5,4), (5,6)

# Coeficientes de la función objetivo (costos)
c = [20,  # x_17: 1->7, costo 20
     3,   # x_13: 1->3, costo 3
     9,   # x_23: 2->3, costo 9
     30,  # x_26: 2->6, costo 30
     40,  # x_37: 3->7, costo 40
     10,  # x_35: 3->5, costo 10
     8,   # x_47: 4->7, costo 8
     a,   # x_54: 5->4, costo a=7
     2]   # x_56: 5->6, costo 2

# Restricciones de balance de flujo (Ax = b)
# Para cada nodo: flujo_entrada - flujo_salida = oferta - demanda

# Matriz A: restricciones de conservación de flujo
A_eq = [
    # Nodo 1: -x_17 - x_13 = -5000
    [-1, -1, 0, 0, 0, 0, 0, 0, 0],
    
    # Nodo 2: -x_23 - x_26 = -6000
    [0, 0, -1, -1, 0, 0, 0, 0, 0],
    
    # Nodo 3: x_13 + x_23 - x_37 - x_35 = 0
    [0, 1, 1, 0, -1, -1, 0, 0, 0],
    
    # Nodo 4: x_54 - x_47 = 0
    [0, 0, 0, 0, 0, 0, -1, 1, 0],
    
    # Nodo 5: x_35 - x_54 - x_56 = 0
    [0, 0, 0, 0, 0, 1, 0, -1, -1],
    
    # Nodo 6: x_26 + x_56 = 2000
    [0, 0, 0, 1, 0, 0, 0, 0, 1],
    
    # Nodo 7: x_17 + x_37 + x_47 = 9000
    [1, 0, 0, 0, 1, 0, 1, 0, 0]
]

# Vector b: lado derecho de las restricciones
b_eq = [-5000, -6000, 0, 0, 0, 2000, 9000]

# Límites de las variables (todas no negativas)
bounds = [(0, None) for _ in range(len(c))]

# Resolver el problema de programación lineal
result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

if result.success:
    print(f"Costo mínimo: {result.fun:.1f}")
    print("\nFlujos óptimos:")
    arcos = ['1->7', '1->3', '2->3', '2->6', '3->7', '3->5', '4->7', '5->4', '5->6']
    for i, flujo in enumerate(result.x):
        if flujo > 0.1:  # Solo mostrar flujos significativos
            print(f"{arcos[i]}: {flujo:.0f} unidades")
else:
    print("No se encontró solución óptima")
    print(result.message)

# Verificar balance
print(f"\nVerificación:")
print(f"Total oferta: {5000 + 6000} unidades")
print(f"Total demanda: {2000 + 9000} unidades")
print(f"Balance: {'✓' if 5000 + 6000 == 2000 + 9000 else '✗'}")