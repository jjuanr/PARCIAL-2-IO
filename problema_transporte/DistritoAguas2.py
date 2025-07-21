import numpy as np
from scipy.optimize import linprog

# Problema de transporte - Distrito de Aguas
# 3 ríos (fuentes) hacia 4 ciudades (destinos)

print("=== PROBLEMA DE TRANSPORTE - DISTRITO DE AGUAS ===")
print()

# Datos del problema
# Costos de transporte (río i hacia ciudad j)
costos = [
    [5, 2, 7, 3],  # Río Colombo hacia [Po, Ancona, Edolo, Pienza]
    [3, 6, 6, 1],  # Río Piave hacia [Po, Ancona, Edolo, Pienza]
    [6, 1, 2, 4]   # Río Calorie hacia [Po, Ancona, Edolo, Pienza]
]

# Disponibilidad de agua en cada río (m³)
disponible = [50, 60, 50]  # [Colombo, Piave, Calorie]

# Necesidad mínima de cada ciudad (m³)
necesidad = [30, 70, 0, 10]  # [Po, Ancona, Edolo, Pienza]

print("Costos de transporte (por m³):")
ciudades = ["Po", "Ancona", "Edolo", "Pienza"]
rios = ["Río Colombo", "Río Piave", "Río Calorie"]

for i, rio in enumerate(rios):
    print(f"{rio:12}", end="")
    for j, ciudad in enumerate(ciudades):
        print(f"{costos[i][j]:8}", end="")
    print(f"  Disponible: {disponible[i]} m³")

print()
print("Necesidades mínimas por ciudad:")
for j, ciudad in enumerate(ciudades):
    print(f"{ciudad}: {necesidad[j]} m³")

print(f"\nTotal disponible: {sum(disponible)} m³")
print(f"Total necesidad: {sum(necesidad)} m³")

# Verificar si el problema está balanceado
if sum(disponible) != sum(necesidad):
    print("Problema no balanceado - ajustando...")

# Variables de decisión: x[i][j] = cantidad de agua del río i hacia la ciudad j
# Aplanamos la matriz para linprog: x11, x12, x13, x14, x21, x22, x23, x24, x31, x32, x33, x34

# Función objetivo: minimizar costo total
c = []
for i in range(3):  # 3 ríos
    for j in range(4):  # 4 ciudades
        c.append(costos[i][j])

print(f"\nCoeficientes de la función objetivo: {c}")

# Restricciones de desigualdad (Ax <= b)
# 1. Restricciones de disponibilidad (suma por fila <= disponibilidad)
A_ub = []
b_ub = []

for i in range(3):  # Para cada río
    fila = [0] * 12
    for j in range(4):  # Para cada ciudad
        fila[i*4 + j] = 1
    A_ub.append(fila)
    b_ub.append(disponible[i])

print(f"\nRestricciones de disponibilidad (A_ub):")
for i, fila in enumerate(A_ub):
    print(f"Río {i+1}: {fila} <= {b_ub[i]}")

# Restricciones de desigualdad adicionales para necesidades mínimas
# Las necesidades son mínimas, no exactas, así que usamos >= (convertido a <= con -1)
for j in range(4):  # Para cada ciudad
    fila = [0] * 12
    for i in range(3):  # Para cada río
        fila[i*4 + j] = -1  # Negativo para convertir >= a <=
    A_ub.append(fila)
    b_ub.append(-necesidad[j])  # Negativo para la conversión

print(f"\nRestricciones de necesidad mínima (convertidas a <=):")
for j in range(4):
    idx = 3 + j  # Las primeras 3 son de disponibilidad
    print(f"Ciudad {ciudades[j]}: {A_ub[idx]} <= {b_ub[idx]} (equivale a >= {necesidad[j]})")

# Restricción de igualdad: usar toda el agua disponible
A_eq = []
b_eq = []

fila_total = [1] * 12
A_eq.append(fila_total)
b_eq.append(sum(disponible))

print(f"\nRestricción de usar toda el agua: {fila_total} = {sum(disponible)}")

# Límites de las variables (no negativas)
bounds = [(0, None) for _ in range(12)]

print("\n=== RESOLVIENDO EL PROBLEMA ===")

# Resolver el problema de programación lineal
resultado = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

if resultado.success:
    print("¡Solución encontrada!")
    print(f"Costo mínimo total: {resultado.fun:.2f}")
    
    # Reorganizar la solución en matriz
    solucion = np.array(resultado.x).reshape(3, 4)
    
    print("\nDistribución óptima de agua (m³):")
    print("Desde/Hacia    Po    Ancona  Edolo  Pienza   Total")
    print("-" * 55)
    
    for i in range(3):
        print(f"{rios[i]:12}", end="")
        total_rio = 0
        for j in range(4):
            cantidad = solucion[i][j]
            print(f"{cantidad:8.1f}", end="")
            total_rio += cantidad
        print(f"{total_rio:8.1f}")
    
    print("-" * 55)
    print("Total        ", end="")
    for j in range(4):
        total_ciudad = sum(solucion[i][j] for i in range(3))
        print(f"{total_ciudad:8.1f}", end="")
    print(f"{sum(disponible):8.1f}")
    
    # Respuesta específica para Ancona
    agua_ancona = sum(solucion[i][1] for i in range(3))
    print(f"\n=== RESPUESTA ===")
    print(f"Cantidad de agua que llegará a Ancona: {agua_ancona:.0f} m³")
    
    # Verificación de las restricciones
    print(f"\n=== VERIFICACIÓN ===")
    print("Cumplimiento de necesidades mínimas:")
    for j, ciudad in enumerate(ciudades):
        total_ciudad = sum(solucion[i][j] for i in range(3))
        cumple = "✓" if total_ciudad >= necesidad[j] else "✗"
        print(f"  {ciudad}: {total_ciudad:.0f} m³ (mínimo {necesidad[j]} m³) {cumple}")
    
    print("Uso de disponibilidad por río:")
    for i, rio in enumerate(rios):
        total_rio = sum(solucion[i][j] for j in range(4))
        cumple = "✓" if total_rio <= disponible[i] else "✗"
        print(f"  {rio}: {total_rio:.0f} m³ (máximo {disponible[i]} m³) {cumple}")
    
else:
    print("No se pudo encontrar una solución óptima")
    print(f"Estado: {resultado.message}")
