import numpy as np
from scipy.optimize import linprog

# Definir la red y resolver el problema de flujo de costo mínimo

# Datos del problema
# Oferta: O1=1000, O2=1200 (total: 2200)
# Demanda: D1=800, D2=900, D3=500 (total: 2200)

# Costos de transmisión (en milésimas de segundo)
# Rutas posibles:
# O1->T1->D1: 3+8=11, O1->T1->D2: 3+6=9
# O1->T2->D2: 4+4=8, O1->T2->D3: 4+9=13
# O2->T1->D1: 2+8=10, O2->T1->D2: 2+6=8
# O2->T2->D2: 5+4=9, O2->T2->D3: 5+9=14

# También hay rutas directas entre destinos:
# D1->D2: 5, D2->D3: 3

# Variables de decisión (flujos):
# x1: O1->T1->D1, x2: O1->T1->D2, x3: O1->T2->D2, x4: O1->T2->D3
# x5: O2->T1->D1, x6: O2->T1->D2, x7: O2->T2->D2, x8: O2->T2->D3
# x9: D1->D2, x10: D2->D3

# Función objetivo: minimizar costo total
c = [11, 9, 8, 13, 10, 8, 9, 14, 5, 3]  # costos

# Restricciones de igualdad (Ax = b)
# Balance de flujo en cada nodo
A_eq = [
    # O1: salida = 1000
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    # O2: salida = 1200
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
    # D1: entrada - salida = 800
    [1, 0, 0, 0, 1, 0, 0, 0, -1, 0],
    # D2: entrada - salida = 900
    [0, 1, 1, 0, 0, 1, 1, 0, 1, -1],
    # D3: entrada = 500
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
]

b_eq = [1000, 1200, 800, 900, 500]

# Límites (todos los flujos >= 0)
bounds = [(0, None) for _ in range(10)]

# Resolver el problema de programación lineal
resultado = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

print("Estado de la solución:", resultado.message)
print("Costo mínimo:", round(resultado.fun, 1), "milésimas de segundo")
print("\nFlujos óptimos:")
flujos = ["O1->T1->D1", "O1->T1->D2", "O1->T2->D2", "O1->T2->D3",
          "O2->T1->D1", "O2->T1->D2", "O2->T2->D2", "O2->T2->D3",
          "D1->D2", "D2->D3"]

for i, flujo in enumerate(flujos):
    if resultado.x[i] > 0.1:  # mostrar solo flujos significativos
        print(f"{flujo}: {round(resultado.x[i], 1)} mensajes")

# Verificar balance
print(f"\nVerificación:")
print(f"Total enviado desde orígenes: {sum(resultado.x[:4]) + sum(resultado.x[4:8])}")
print(f"Total recibido en destinos: {sum(resultado.x[i] for i in [0,4]) + sum(resultado.x[i] for i in [1,2,5,6,8]) + sum(resultado.x[i] for i in [3,7,9])}")