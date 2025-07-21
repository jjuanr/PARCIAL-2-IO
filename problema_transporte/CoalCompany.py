import numpy as np
from scipy.optimize import linprog

# Problema de Transporte - Coal Company
print("=== PROBLEMA DE TRANSPORTE - COAL COMPANY ===")
print()

# Datos del problema
print("Datos del problema:")
print("Demanda de los centros (toneladas):")
demanda = [80, 65, 70, 85]  # Centro 1, 2, 3, 4
print(f"Centro 1: {demanda[0]} toneladas")
print(f"Centro 2: {demanda[1]} toneladas")
print(f"Centro 3: {demanda[2]} toneladas")
print(f"Centro 4: {demanda[3]} toneladas")
print(f"Demanda total: {sum(demanda)} toneladas")
print()

print("Oferta de las minas (toneladas):")
oferta = [75, 125, 100]  # Mina 1, 2, 3
print(f"Mina 1: {oferta[0]} toneladas")
print(f"Mina 2: {oferta[1]} toneladas")
print(f"Mina 3: {oferta[2]} toneladas")
print(f"Oferta total: {sum(oferta)} toneladas")
print()

# Matriz de costos de transporte
costos = [
    [866, 861, 612, 590],  # Mina 1 a Centros 1,2,3,4
    [547, 622, 433, 570],  # Mina 2 a Centros 1,2,3,4
    [707, 664, 426, 779]   # Mina 3 a Centros 1,2,3,4
]

print("Matriz de costos de transporte:")
print("        Centro 1  Centro 2  Centro 3  Centro 4")
for i, fila in enumerate(costos):
    print(f"Mina {i+1}:    {fila[0]:3d}      {fila[1]:3d}      {fila[2]:3d}      {fila[3]:3d}")
print()

# Variables de decisión: x_ij donde i=mina, j=centro
# x11, x12, x13, x14, x21, x22, x23, x24, x31, x32, x33, x34
# (12 variables en total)

# Función objetivo (minimizar costos)
# Coeficientes de la función objetivo (costos aplanados)
c = []
for i in range(3):  # 3 minas
    for j in range(4):  # 4 centros
        c.append(costos[i][j])

print(f"Coeficientes de la función objetivo: {c}")
print()

# Restricciones de igualdad (Ax = b)
# Restricciones de demanda (4 restricciones) + Restricciones de oferta (3 restricciones)
A_eq = []
b_eq = []

# Restricciones de demanda (cada centro debe recibir exactamente su demanda)
for j in range(4):  # Para cada centro
    restriccion = [0] * 12
    for i in range(3):  # Para cada mina
        restriccion[i * 4 + j] = 1
    A_eq.append(restriccion)
    b_eq.append(demanda[j])

# Restricciones de oferta (cada mina no puede exceder su capacidad)
for i in range(3):  # Para cada mina
    restriccion = [0] * 12
    for j in range(4):  # Para cada centro
        restriccion[i * 4 + j] = 1
    A_eq.append(restriccion)
    b_eq.append(oferta[i])

A_eq = np.array(A_eq)
b_eq = np.array(b_eq)

print("Matriz de restricciones A_eq:")
print(A_eq)
print()
print(f"Vector de términos independientes b_eq: {b_eq}")
print()

# Límites de las variables (todas no negativas)
bounds = [(0, None) for _ in range(12)]

# Resolver el problema de programación lineal
print("Resolviendo el problema de optimización...")
resultado = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

print(f"Estado de la optimización: {resultado.message}")
print(f"Costo mínimo total: {resultado.fun:.2f}")
print()

# Mostrar la solución
solucion = resultado.x.reshape(3, 4)
print("Solución óptima (toneladas transportadas):")
print("        Centro 1  Centro 2  Centro 3  Centro 4   Total")
total_minas = []
for i in range(3):
    total_mina = sum(solucion[i])
    total_minas.append(total_mina)
    print(f"Mina {i+1}:   {solucion[i][0]:6.1f}    {solucion[i][1]:6.1f}    {solucion[i][2]:6.1f}    {solucion[i][3]:6.1f}   {total_mina:6.1f}")

print("Total:  ", end="")
for j in range(4):
    total_centro = sum(solucion[i][j] for i in range(3))
    print(f"{total_centro:6.1f}    ", end="")
total_general = sum(total_minas)
print(f"{total_general:6.1f}")
print()

# Respuesta específica de la pregunta
mina2_centro4 = solucion[1][3]  # Mina 2 (índice 1) al Centro 4 (índice 3)
print("=" * 60)
print("RESPUESTA A LA PREGUNTA:")
print(f"Toneladas de carbón que deben transportarse de la Mina 2 al Centro 4: {mina2_centro4:.1f}")
print("=" * 60)
print()

# Verificación de la solución
print("VERIFICACIÓN:")
print("1. Verificando restricciones de demanda:")
for j in range(4):
    total_demanda = sum(solucion[i][j] for i in range(3))
    print(f"   Centro {j+1}: {total_demanda:.1f} = {demanda[j]} ✓" if abs(total_demanda - demanda[j]) < 0.001 else f"   Centro {j+1}: {total_demanda:.1f} ≠ {demanda[j]} ✗")

print("2. Verificando restricciones de oferta:")
for i in range(3):
    total_oferta = sum(solucion[i][j] for j in range(4))
    print(f"   Mina {i+1}: {total_oferta:.1f} ≤ {oferta[i]} ✓" if total_oferta <= oferta[i] + 0.001 else f"   Mina {i+1}: {total_oferta:.1f} > {oferta[i]} ✗")

print(f"3. Costo total mínimo: ${resultado.fun:,.2f}")
print(f"4. Respuesta final: {mina2_centro4:.1f} toneladas")
