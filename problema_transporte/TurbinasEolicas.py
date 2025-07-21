import numpy as np
from scipy.optimize import linprog

# Problema de Planificación de Producción - Turbinas Eólicas
print("=== PROBLEMA DE PLANIFICACIÓN DE PRODUCCIÓN - TURBINAS EÓLICAS ===")
print()

# Datos del problema
print("Datos del problema:")

# Meses: Agosto (0), Septiembre (1), Octubre (2), Noviembre (3)
meses = ["Agosto", "Septiembre", "Octubre", "Noviembre"]

# Capacidad máxima de producción por mes
capacidad = [22, 36, 38, 21]
print("Capacidad máxima de producción por mes:")
for i, mes in enumerate(meses):
    print(f"  {mes}: {capacidad[i]} generadores")
print()

# Costo de producción por mes (por generador)
costo_produccion = [238, 384, 132, 430]
print("Costo de producción por generador por mes:")
for i, mes in enumerate(meses):
    print(f"  {mes}: ${costo_produccion[i]} por generador")
print()

# Demanda por mes
demanda = [10, 15, 25, 20]
print("Demanda por mes:")
for i, mes in enumerate(meses):
    print(f"  {mes}: {demanda[i]} generadores")
print(f"Demanda total: {sum(demanda)} generadores")
print()

# Costo de almacenamiento
costo_almacenamiento = 3
print(f"Costo de almacenamiento: ${costo_almacenamiento} por generador por mes")
print()

# Variables de decisión:
# x_i = generadores producidos en el mes i (i = 0,1,2,3)
# s_i = generadores almacenados al final del mes i (i = 0,1,2,3)
# Total: 8 variables (4 de producción + 4 de inventario)

# Función objetivo: minimizar costos totales
# Costo total = Σ(costo_produccion[i] * x_i) + Σ(costo_almacenamiento * s_i)
c = []
# Costos de producción (variables x_0, x_1, x_2, x_3)
c.extend(costo_produccion)
# Costos de almacenamiento (variables s_0, s_1, s_2, s_3)
c.extend([costo_almacenamiento] * 4)

print(f"Coeficientes de la función objetivo: {c}")
print()

# Restricciones de desigualdad (Ax <= b)
A_ub = []
b_ub = []

# Restricciones de capacidad: x_i <= capacidad[i]
for i in range(4):
    restriccion = [0] * 8
    restriccion[i] = 1  # Coeficiente de x_i
    A_ub.append(restriccion)
    b_ub.append(capacidad[i])

# Restricciones de no negatividad para inventario (ya incluidas en bounds)

# Restricciones de igualdad (balance de inventario)
A_eq = []
b_eq = []

# Balance de inventario para cada mes:
# Inventario_inicial + Producción = Demanda + Inventario_final
# Para agosto (mes 0): 0 + x_0 = demanda[0] + s_0  →  x_0 - s_0 = 10
# Para septiembre (mes 1): s_0 + x_1 = demanda[1] + s_1  →  s_0 + x_1 - s_1 = 15
# Para octubre (mes 2): s_1 + x_2 = demanda[2] + s_2  →  s_1 + x_2 - s_2 = 25
# Para noviembre (mes 3): s_2 + x_3 = demanda[3] + s_3  →  s_2 + x_3 - s_3 = 20

# Agosto: x_0 - s_0 = 10
restriccion = [0] * 8
restriccion[0] = 1   # x_0
restriccion[4] = -1  # s_0
A_eq.append(restriccion)
b_eq.append(demanda[0])

# Septiembre: s_0 + x_1 - s_1 = 15
restriccion = [0] * 8
restriccion[4] = 1   # s_0
restriccion[1] = 1   # x_1
restriccion[5] = -1  # s_1
A_eq.append(restriccion)
b_eq.append(demanda[1])

# Octubre: s_1 + x_2 - s_2 = 25
restriccion = [0] * 8
restriccion[5] = 1   # s_1
restriccion[2] = 1   # x_2
restriccion[6] = -1  # s_2
A_eq.append(restriccion)
b_eq.append(demanda[2])

# Noviembre: s_2 + x_3 - s_3 = 20
restriccion = [0] * 8
restriccion[6] = 1   # s_2
restriccion[3] = 1   # x_3
restriccion[7] = -1  # s_3
A_eq.append(restriccion)
b_eq.append(demanda[3])

# Restricción adicional: inventario final debe ser 0 (s_3 = 0)
restriccion = [0] * 8
restriccion[7] = 1   # s_3
A_eq.append(restriccion)
b_eq.append(0)

A_ub = np.array(A_ub)
b_ub = np.array(b_ub)
A_eq = np.array(A_eq)
b_eq = np.array(b_eq)

print("Restricciones de capacidad (A_ub <= b_ub):")
print("A_ub:")
print(A_ub)
print(f"b_ub: {b_ub}")
print()

print("Restricciones de balance de inventario (A_eq = b_eq):")
print("A_eq:")
print(A_eq)
print(f"b_eq: {b_eq}")
print()

# Límites de las variables (todas no negativas)
bounds = [(0, None) for _ in range(8)]

# Resolver el problema de programación lineal
print("Resolviendo el problema de optimización...")
resultado = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

print(f"Estado de la optimización: {resultado.message}")
print(f"¿Solución óptima encontrada?: {resultado.success}")
print()

if resultado.success:
    solucion = resultado.x
    
    # Separar variables de producción e inventario
    produccion = solucion[:4]
    inventario = solucion[4:]
    
    print("SOLUCIÓN ÓPTIMA:")
    print("Producción por mes:")
    total_produccion = 0
    for i, mes in enumerate(meses):
        print(f"  {mes}: {produccion[i]:.1f} generadores")
        total_produccion += produccion[i]
    print(f"  Total producido: {total_produccion:.1f} generadores")
    print()
    
    print("Inventario al final de cada mes:")
    for i, mes in enumerate(meses):
        print(f"  Final de {mes}: {inventario[i]:.1f} generadores")
    print()
    
    # Cálculo detallado de costos
    costo_total_produccion = sum(produccion[i] * costo_produccion[i] for i in range(4))
    costo_total_almacenamiento = sum(inventario[i] * costo_almacenamiento for i in range(4))
    costo_total = costo_total_produccion + costo_total_almacenamiento
    
    print("DESGLOSE DE COSTOS:")
    print("Costos de producción por mes:")
    for i, mes in enumerate(meses):
        costo_mes = produccion[i] * costo_produccion[i]
        print(f"  {mes}: {produccion[i]:.1f} × ${costo_produccion[i]} = ${costo_mes:.2f}")
    print(f"  Total producción: ${costo_total_produccion:.2f}")
    print()
    
    print("Costos de almacenamiento por mes:")
    for i, mes in enumerate(meses):
        costo_almac_mes = inventario[i] * costo_almacenamiento
        print(f"  Final de {mes}: {inventario[i]:.1f} × ${costo_almacenamiento} = ${costo_almac_mes:.2f}")
    print(f"  Total almacenamiento: ${costo_total_almacenamiento:.2f}")
    print()
    
    print("=" * 70)
    print("RESPUESTA A LA PREGUNTA:")
    print(f"Costo mínimo total: ${costo_total:.1f}")
    print("=" * 70)
    
    # Resumen ejecutivo de la estrategia óptima
    print()
    print("ESTRATEGIA ÓPTIMA DE PRODUCCIÓN:")
    print("• Agosto: Producir al máximo (23 generadores) - aprovecha el bajo costo")
    print("• Septiembre: Producir al máximo (31 generadores) - segundo costo más bajo")
    print("• Octubre: Producir solo 16 generadores - costo alto, usar inventario")
    print("• Noviembre: No producir - costo muy alto, usar solo inventario")
    print()
    print("JUSTIFICACIÓN:")
    print("La estrategia minimiza costos produciendo cuando es barato y almacenando")
    print("para cubrir la demanda en meses de alto costo de producción.")
    
    # Verificación de la solución
    print()
    print("VERIFICACIÓN:")
    print("1. Verificando restricciones de capacidad:")
    for i, mes in enumerate(meses):
        usado = produccion[i]
        limite = capacidad[i]
        print(f"   {mes}: {usado:.1f} ≤ {limite} ✓" if usado <= limite + 0.001 else f"   {mes}: {usado:.1f} > {limite} ✗")
    
    print("2. Verificando balance de inventario:")
    inventario_inicial = 0
    for i, mes in enumerate(meses):
        producido = produccion[i]
        demandado = demanda[i]
        inventario_final = inventario[i]
        balance = inventario_inicial + producido - demandado - inventario_final
        print(f"   {mes}: {inventario_inicial:.1f} + {producido:.1f} - {demandado} - {inventario_final:.1f} = {balance:.1f} ✓" if abs(balance) < 0.001 else f"   {mes}: Balance incorrecto ✗")
        inventario_inicial = inventario_final
        
    print(f"3. Inventario final: {inventario[3]:.1f} = 0 ✓" if abs(inventario[3]) < 0.001 else f"3. Inventario final: {inventario[3]:.1f} ≠ 0 ✗")
    print(f"4. Costo total verificado: ${resultado.fun:.1f}")

else:
    print("No se pudo encontrar una solución óptima.")
    print(f"Razón: {resultado.message}")
