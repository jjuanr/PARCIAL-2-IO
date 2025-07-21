import numpy as np
from scipy.optimize import linprog

# Problema de Transporte - Distrito Aguas
print("=== PROBLEMA DE TRANSPORTE - DISTRITO AGUAS ===")
print()

# Datos del problema
print("Datos del problema:")

# Ríos y ciudades
rios = ["Río Colombo", "Río Piave", "Río Calorie"]
ciudades = ["Po", "Ancona", "Edolo", "Pienza"]

# Disponibilidad de agua de los ríos (m3)
disponible = [50, 60, 50]
print("Disponibilidad de agua por río (m3):")
for i, rio in enumerate(rios):
    print(f"  {rio}: {disponible[i]} m3")
print(f"Disponibilidad total: {sum(disponible)} m3")
print()

# Necesidades de las ciudades (m3)
necesidad = [30, 70, 0, 10]
print("Necesidades por ciudad (m3):")
for i, ciudad in enumerate(ciudades):
    print(f"  {ciudad}: {necesidad[i]} m3")
print(f"Necesidad total: {sum(necesidad)} m3")
print()

# Matriz de costos de transporte (por m3)
costos = [
    [5, 2, 7, 3],  # Río Colombo a todas las ciudades
    [3, 6, 6, 1],  # Río Piave a todas las ciudades
    [6, 1, 2, 4]   # Río Calorie a todas las ciudades
]

print("Matriz de costos de transporte (por m3):")
print("Desde/Hacia        ", end="")
for ciudad in ciudades:
    print(f"{ciudad:>8}", end="")
print()
for i, rio in enumerate(rios):
    print(f"{rio:<15}", end="")
    for j in range(len(ciudades)):
        print(f"{costos[i][j]:>8}", end="")
    print()
print()

# Verificar balance del problema
print("ANÁLISIS DEL PROBLEMA:")
print(f"Total disponible: {sum(disponible)} m3")
print(f"Total necesario: {sum(necesidad)} m3")
if sum(disponible) > sum(necesidad):
    print("Problema con exceso de oferta - se puede satisfacer toda la demanda")
    exceso = sum(disponible) - sum(necesidad)
    print(f"Exceso de oferta: {exceso} m3")
elif sum(disponible) < sum(necesidad):
    print("Problema con déficit de oferta - no se puede satisfacer toda la demanda")
else:
    print("Problema balanceado - oferta = demanda")
print()

# Variables de decisión: x_ij donde i=río, j=ciudad
# x11, x12, x13, x14, x21, x22, x23, x24, x31, x32, x33, x34
# (12 variables en total)

# Función objetivo (minimizar costos)
c = []
for i in range(3):  # 3 ríos
    for j in range(4):  # 4 ciudades
        c.append(costos[i][j])

print(f"Coeficientes de la función objetivo: {c}")
print()

# Restricciones de desigualdad y igualdad
A_ub = []
b_ub = []
A_eq = []
b_eq = []

# Restricciones de disponibilidad (cada río no puede exceder su disponibilidad)
for i in range(3):  # Para cada río
    restriccion = [0] * 12
    for j in range(4):  # Para cada ciudad
        restriccion[i * 4 + j] = 1
    A_ub.append(restriccion)
    b_ub.append(disponible[i])

# Restricciones de demanda (cada ciudad debe recibir al menos su necesidad)
# Para ciudades con demanda > 0, usar restricciones de igualdad
for j in range(4):  # Para cada ciudad
    if necesidad[j] > 0:
        restriccion = [0] * 12
        for i in range(3):  # Para cada río
            restriccion[i * 4 + j] = 1
        A_eq.append(restriccion)
        b_eq.append(necesidad[j])

# Convertir a arrays numpy
A_ub = np.array(A_ub) if A_ub else None
b_ub = np.array(b_ub) if b_ub else None
A_eq = np.array(A_eq) if A_eq else None
b_eq = np.array(b_eq) if b_eq else None

print("Restricciones de disponibilidad (cada río no excede su capacidad):")
for i, rio in enumerate(rios):
    ecuacion = ""
    for j, ciudad in enumerate(ciudades):
        if j > 0:
            ecuacion += " + "
        ecuacion += f"x{i+1}{j+1}"
    print(f"  {ecuacion} ≤ {disponible[i]} ({rio})")
print()

print("Restricciones de demanda (satisfacer necesidades mínimas):")
for j, ciudad in enumerate(ciudades):
    if necesidad[j] > 0:
        ecuacion = ""
        for i, rio in enumerate(rios):
            if i > 0:
                ecuacion += " + "
            ecuacion += f"x{i+1}{j+1}"
        print(f"  {ecuacion} = {necesidad[j]} ({ciudad})")
print()

# Límites de las variables (todas no negativas)
bounds = [(0, None) for _ in range(12)]

# Resolver el problema de programación lineal
print("Resolviendo el problema de optimización...")
resultado = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

print(f"Estado de la optimización: {resultado.message}")
print(f"¿Solución óptima encontrada?: {resultado.success}")
if resultado.success:
    print(f"Costo mínimo total: {resultado.fun:.2f}")
print()

if resultado.success:
    # Mostrar la solución
    solucion = resultado.x.reshape(3, 4)
    
    print("SOLUCIÓN ÓPTIMA (m3 de agua transportados):")
    print("Desde/Hacia        ", end="")
    for ciudad in ciudades:
        print(f"{ciudad:>8}", end="")
    print("   Total")
    
    total_rios = []
    for i in range(3):
        total_rio = sum(solucion[i])
        total_rios.append(total_rio)
        print(f"{rios[i]:<15}", end="")
        for j in range(4):
            print(f"{solucion[i][j]:>8.1f}", end="")
        print(f"{total_rio:>8.1f}")

    print("Total:             ", end="")
    for j in range(4):
        total_ciudad = sum(solucion[i][j] for i in range(3))
        print(f"{total_ciudad:>8.1f}", end="")
    total_general = sum(total_rios)
    print(f"{total_general:>8.1f}")
    print()
    
    # Respuesta específica de la pregunta
    colombo_a_ancona = solucion[0][1]  # Río Colombo (índice 0) a Ancona (índice 1)
    
    print("=" * 80)
    print("RESPUESTA A LA PREGUNTA:")
    print(f"m3 de agua que deben llevarse desde el Río Colombo hasta Ancona: {colombo_a_ancona:.0f}")
    print("=" * 80)
    print()
    
    # Verificación de la solución
    print("VERIFICACIÓN:")
    print("1. Verificando restricciones de disponibilidad:")
    for i, rio in enumerate(rios):
        total_usado = sum(solucion[i][j] for j in range(4))
        status = "✓" if total_usado <= disponible[i] + 0.001 else "✗"
        print(f"   {rio}: {total_usado:.1f} ≤ {disponible[i]} {status}")

    print("2. Verificando restricciones de demanda:")
    for j, ciudad in enumerate(ciudades):
        total_recibido = sum(solucion[i][j] for i in range(3))
        if necesidad[j] > 0:
            status = "✓" if abs(total_recibido - necesidad[j]) < 0.001 else "✗"
            print(f"   {ciudad}: {total_recibido:.1f} = {necesidad[j]} {status}")
        else:
            status = "✓" if total_recibido >= 0 else "✗"
            print(f"   {ciudad}: {total_recibido:.1f} ≥ {necesidad[j]} {status}")

    print(f"3. Costo total mínimo: {resultado.fun:.2f}")
    
    # Desglose detallado de costos
    print()
    print("DESGLOSE DE COSTOS:")
    costo_total_calculado = 0
    for i, rio in enumerate(rios):
        for j, ciudad in enumerate(ciudades):
            if solucion[i][j] > 0.001:  # Solo mostrar rutas con transporte
                costo_ruta = solucion[i][j] * costos[i][j]
                costo_total_calculado += costo_ruta
                print(f"  {rio} → {ciudad}: {solucion[i][j]:.1f} × {costos[i][j]} = {costo_ruta:.2f}")
    
    print(f"Costo total calculado: {costo_total_calculado:.2f}")
    
    # Estrategia óptima
    print()
    print("ESTRATEGIA ÓPTIMA DE DISTRIBUCIÓN:")
    print("• Po (30 m3): Abastecida completamente por Río Piave (costo 3)")
    print("• Ancona (70 m3): Combinación óptima:")
    print("  - 20 m3 desde Río Colombo (costo 2 - más barato)")
    print("  - 50 m3 desde Río Calorie (costo 1 - el más barato)")
    print("• Edolo (0 m3): No recibe agua (no tiene necesidad)")
    print("• Pienza (10 m3): Abastecida por Río Piave (costo 1 - más barato)")
    print()
    print("JUSTIFICACIÓN:")
    print("La estrategia aprovecha las rutas más baratas disponibles:")
    print("- Río Calorie → Ancona (costo 1): máximo uso posible (50 m3)")
    print("- Río Piave → Pienza (costo 1): ruta más barata para Pienza")
    print("- Se minimizan los costos totales priorizando rutas económicas")

else:
    print("No se pudo encontrar una solución óptima.")
    print(f"Razón: {resultado.message}")
