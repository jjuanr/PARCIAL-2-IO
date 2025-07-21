from scipy.optimize import linprog
import numpy as np

# Datos del problema
# Oferta en minas
oferta_M1 = 1000
oferta_M2 = 1200
total_oferta = oferta_M1 + oferta_M2  # 2200 toneladas

# Demanda en destinos
demanda_D1 = 800
demanda_D2 = 900
demanda_D3 = 500
total_demanda = demanda_D1 + demanda_D2 + demanda_D3  # 2200 toneladas

# Costos de transporte
a, b, c, d, e, f, g, h, i, k, m = 9, 11, 9, 4, 3, 4, 13, 3, 15, 2, 10

# Variables de decisión (flujos):
# x0: M1 -> CC1 (a)
# x1: M1 -> CC2 (b)
# x2: M2 -> CC1 (c)
# x3: M2 -> CC2 (d)
# x4: CC1 -> D1 (e)
# x5: CC1 -> D2 (f)
# x6: CC1 -> CC2 (g)
# x7: CC2 -> D2 (h)
# x8: CC2 -> D3 (i)
# x9: D2 -> D3 (m)
# x10: D1 -> D2 (k)

# Función objetivo (minimizar costo total)
c_obj = [a, b, c, d, e, f, g, h, i, m, k]  # Corregido el orden: m para x9, k para x10

# Restricciones de igualdad (balance de flujo)
# M1: x0 + x1 = 1000
# M2: x2 + x3 = 1200
# CC1: x0 + x2 - x4 - x5 - x6 = 0
# CC2: x1 + x3 + x6 - x7 - x8 = 0
# D1: x4 - x10 = 800
# D2: x5 + x7 + x10 - x9 = 900
# D3: x8 + x9 = 500

A_eq = np.array([
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # M1 balance
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],    # M2 balance
    [1, 0, 1, 0, -1, -1, -1, 0, 0, 0, 0], # CC1 balance
    [0, 1, 0, 1, 0, 0, 1, -1, -1, 0, 0],  # CC2 balance
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, -1],   # D1 balance
    [0, 0, 0, 0, 0, 1, 0, 1, 0, -1, 1],   # D2 balance
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]     # D3 balance
])

b_eq = np.array([1000, 1200, 0, 0, 800, 900, 500])

# Restricciones de no negatividad (bounds)
bounds = [(0, None) for _ in range(11)]

# Resolver el problema
resultado = linprog(c_obj, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

if resultado.success:
    print("Solución óptima encontrada:")
    print(f"Costo mínimo: ${resultado.fun:.1f}")
    print("\nFlujos óptimos:")
    variables = ['M1->CC1 (a)', 'M1->CC2 (b)', 'M2->CC1 (c)', 'M2->CC2 (d)', 
                'CC1->D1 (e)', 'CC1->D2 (f)', 'CC1->CC2 (g)', 
                'CC2->D2 (h)', 'CC2->D3 (i)', 'D2->D3 (m)', 'D1->D2 (k)']
    
    for i, var in enumerate(variables):
        if resultado.x[i] > 1e-6:  # Solo mostrar flujos positivos
            print(f"{var}: {resultado.x[i]:.1f} toneladas")
    
    print(f"\nRespuesta: {resultado.fun:.1f}")
else:
    print("No se encontró solución óptima")