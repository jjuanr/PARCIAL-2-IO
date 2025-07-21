import numpy as np
from scipy.optimize import linprog

# Problema de transporte - Maxi Cervezas
# 4 plantas (fuentes) hacia 4 ciudades (destinos)

print("=== PROBLEMA DE TRANSPORTE - MAXI CERVEZAS ===")
print()

# Datos del problema
# Costos de transporte (planta i hacia ciudad j) por cada mil cervezas
costos = [
    [5, 2, 7, 3],  # Montería hacia [Montería, Bogotá, Medellín, Barranquilla]
    [3, 6, 6, 1],  # Bogotá hacia [Montería, Bogotá, Medellín, Barranquilla]
    [6, 1, 2, 4],  # Medellín hacia [Montería, Bogotá, Medellín, Barranquilla]
    [4, 3, 6, 6]   # Barranquilla hacia [Montería, Bogotá, Medellín, Barranquilla]
]

# Capacidad de producción de cada planta (miles de cervezas por día)
produccion = [80, 30, 60, 45]  # [Montería, Bogotá, Medellín, Barranquilla]

# Demanda de cada ciudad (miles de cervezas por día)
demanda = [70, 40, 70, 35]  # [Montería, Bogotá, Medellín, Barranquilla]

print("Costos de transporte (por mil cervezas):")
ciudades = ["Montería", "Bogotá", "Medellín", "Barranquilla"]
plantas = ["Montería", "Bogotá", "Medellín", "Barranquilla"]

for i, planta in enumerate(plantas):
    print(f"{planta:12}", end="")
    for j, ciudad in enumerate(ciudades):
        print(f"{costos[i][j]:8}", end="")
    print(f"  Producción: {produccion[i]} mil")

print()
print("Demandas por ciudad:")
for j, ciudad in enumerate(ciudades):
    print(f"{ciudad}: {demanda[j]} mil cervezas")

print(f"\nTotal producción: {sum(produccion)} mil cervezas")
print(f"Total demanda: {sum(demanda)} mil cervezas")

# Verificar si el problema está balanceado
if sum(produccion) == sum(demanda):
    print("Problema balanceado ✓")
else:
    print(f"Problema no balanceado - Exceso de producción: {sum(produccion) - sum(demanda)} mil")

# Variables de decisión: x[i][j] = cantidad (miles) de cerveza de la planta i hacia la ciudad j
# Aplanamos la matriz para linprog: x00, x01, x02, x03, x10, x11, x12, x13, x20, x21, x22, x23, x30, x31, x32, x33

# Función objetivo: minimizar costo total
c = []
for i in range(4):  # 4 plantas
    for j in range(4):  # 4 ciudades
        c.append(costos[i][j])

print(f"\nCoeficientes de la función objetivo: {c}")

# Restricciones de desigualdad (Ax <= b)
A_ub = []
b_ub = []

# 1. Restricciones de capacidad de producción (suma por fila <= producción)
for i in range(4):  # Para cada planta
    fila = [0] * 16
    for j in range(4):  # Para cada ciudad
        fila[i*4 + j] = 1
    A_ub.append(fila)
    b_ub.append(produccion[i])

print(f"\nRestricciones de capacidad de producción:")
for i, fila in enumerate(A_ub):
    print(f"Planta {plantas[i]}: suma <= {b_ub[i]} mil")

# 2. Restricción especial: no más de 25 mil de Montería a Bogotá
# Variable x01 (Montería hacia Bogotá) <= 25
fila_especial = [0] * 16
fila_especial[1] = 1  # x01 (índice 1 = Montería hacia Bogotá)
A_ub.append(fila_especial)
b_ub.append(25)

print(f"\nRestricción especial:")
print(f"Montería -> Bogotá: <= 25 mil cervezas")

# Restricciones de igualdad (Ax = b)
# Restricciones de demanda (suma por columna = demanda)
A_eq = []
b_eq = []

for j in range(4):  # Para cada ciudad
    fila = [0] * 16
    for i in range(4):  # Para cada planta
        fila[i*4 + j] = 1
    A_eq.append(fila)
    b_eq.append(demanda[j])

print(f"\nRestricciones de demanda:")
for j, fila in enumerate(A_eq):
    print(f"Ciudad {ciudades[j]}: suma = {b_eq[j]} mil")

# Límites de las variables (no negativas)
bounds = [(0, None) for _ in range(16)]

print("\n=== RESOLVIENDO EL PROBLEMA ===")

# Resolver el problema de programación lineal
resultado = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

if resultado.success:
    print("¡Solución encontrada!")
    print(f"Costo mínimo total: {resultado.fun:.2f}")
    
    # Reorganizar la solución en matriz
    solucion = np.array(resultado.x).reshape(4, 4)
    
    print("\nDistribución óptima de cervezas (miles):")
    print("Desde/Hacia    Montería  Bogotá  Medellín  Barranquilla   Total")
    print("-" * 70)
    
    for i in range(4):
        print(f"{plantas[i]:12}", end="")
        total_planta = 0
        for j in range(4):
            cantidad = solucion[i][j]
            print(f"{cantidad:9.1f}", end="")
            total_planta += cantidad
        print(f"{total_planta:11.1f}")
    
    print("-" * 70)
    print("Total        ", end="")
    for j in range(4):
        total_ciudad = sum(solucion[i][j] for i in range(4))
        print(f"{total_ciudad:9.1f}", end="")
    print(f"{sum(demanda):11.1f}")
    
    print(f"\n=== RESPUESTA ===")
    print(f"Menor costo de transporte: {resultado.fun:.0f}")
    
    # Verificación de restricciones
    print(f"\n=== VERIFICACIÓN ===")
    print("Cumplimiento de demandas:")
    for j, ciudad in enumerate(ciudades):
        total_ciudad = sum(solucion[i][j] for i in range(4))
        cumple = "✓" if abs(total_ciudad - demanda[j]) < 0.01 else "✗"
        print(f"  {ciudad}: {total_ciudad:.1f} mil (demanda {demanda[j]} mil) {cumple}")
    
    print("Uso de capacidad de producción:")
    for i, planta in enumerate(plantas):
        total_planta = sum(solucion[i][j] for j in range(4))
        cumple = "✓" if total_planta <= produccion[i] + 0.01 else "✗"
        print(f"  {planta}: {total_planta:.1f} mil (máximo {produccion[i]} mil) {cumple}")
    
    print("Restricción especial:")
    monteria_bogota = solucion[0][1]  # Montería hacia Bogotá
    cumple = "✓" if monteria_bogota <= 25.01 else "✗"
    print(f"  Montería -> Bogotá: {monteria_bogota:.1f} mil (máximo 25 mil) {cumple}")
    
    # Cálculo detallado del costo
    print(f"\n=== DESGLOSE DE COSTOS ===")
    costo_total = 0
    for i in range(4):
        for j in range(4):
            if solucion[i][j] > 0.01:  # Solo mostrar envíos positivos
                costo = solucion[i][j] * costos[i][j]
                costo_total += costo
                print(f"{plantas[i]} -> {ciudades[j]}: {solucion[i][j]:.1f} mil × {costos[i][j]} = {costo:.1f}")
    print(f"Costo total calculado: {costo_total:.1f}")
    
else:
    print("No se pudo encontrar una solución óptima")
    print(f"Estado: {resultado.message}")
