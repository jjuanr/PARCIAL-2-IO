import numpy as np
from scipy.optimize import linprog

# Problema de Transporte - Maxi Cervezas
print("=== PROBLEMA DE TRANSPORTE - MAXI CERVEZAS ===")
print()

# Datos del problema
print("Datos del problema:")

# Plantas y ciudades
plantas = ["Montería", "Bogotá", "Medellín", "Barranquilla"]
ciudades = ["Montería", "Bogotá", "Medellín", "Barranquilla"]

# Capacidad de producción de las plantas (miles de cervezas diarias)
oferta = [80, 30, 60, 45]
print("Capacidad de producción por planta (miles de cervezas diarias):")
for i, planta in enumerate(plantas):
    print(f"  {planta}: {oferta[i]} mil cervezas")
print(f"Oferta total: {sum(oferta)} mil cervezas")
print()

# Demanda de las ciudades (miles de cervezas diarias)
demanda = [70, 40, 70, 35]
print("Necesidades por ciudad (miles de cervezas diarias):")
for i, ciudad in enumerate(ciudades):
    print(f"  {ciudad}: {demanda[i]} mil cervezas")
print(f"Demanda total: {sum(demanda)} mil cervezas")
print()

# Matriz de costos de transporte (por cada mil unidades)
costos = [
    [2, 5, 2, 3],  # Montería a todas las ciudades
    [5, 5, 7, 1],  # Bogotá a todas las ciudades
    [6, 1, 2, 4],  # Medellín a todas las ciudades
    [5, 1, 6, 2]   # Barranquilla a todas las ciudades
]

print("Matriz de costos de transporte (por cada mil unidades):")
print("Desde/Hacia     ", end="")
for ciudad in ciudades:
    print(f"{ciudad:>10}", end="")
print()
for i, planta in enumerate(plantas):
    print(f"{planta:<12}", end="")
    for j in range(len(ciudades)):
        print(f"{costos[i][j]:>10}", end="")
    print()
print()

# Variables de decisión: x_ij donde i=planta, j=ciudad
# x11, x12, x13, x14, x21, x22, x23, x24, x31, x32, x33, x34, x41, x42, x43, x44
# (16 variables en total)

# Función objetivo (minimizar costos)
# Coeficientes de la función objetivo (costos aplanados)
c = []
for i in range(4):  # 4 plantas
    for j in range(4):  # 4 ciudades
        c.append(costos[i][j])

print(f"Coeficientes de la función objetivo: {c}")
print()

# Restricciones de igualdad (Ax = b)
# Restricciones de demanda (4 restricciones) + Restricciones de oferta (4 restricciones)
A_eq = []
b_eq = []

# Restricciones de demanda (cada ciudad debe recibir exactamente su demanda)
for j in range(4):  # Para cada ciudad
    restriccion = [0] * 16
    for i in range(4):  # Para cada planta
        restriccion[i * 4 + j] = 1
    A_eq.append(restriccion)
    b_eq.append(demanda[j])

# Restricciones de oferta (cada planta no puede exceder su capacidad)
for i in range(4):  # Para cada planta
    restriccion = [0] * 16
    for j in range(4):  # Para cada ciudad
        restriccion[i * 4 + j] = 1
    A_eq.append(restriccion)
    b_eq.append(oferta[i])

A_eq = np.array(A_eq)
b_eq = np.array(b_eq)

print("Restricciones de demanda (cada ciudad recibe exactamente lo que necesita):")
for j, ciudad in enumerate(ciudades):
    ecuacion = ""
    for i, planta in enumerate(plantas):
        if i > 0:
            ecuacion += " + "
        ecuacion += f"x{i+1}{j+1}"
    print(f"  {ecuacion} = {demanda[j]} ({ciudad})")
print()

print("Restricciones de oferta (cada planta no excede su capacidad):")
for i, planta in enumerate(plantas):
    ecuacion = ""
    for j, ciudad in enumerate(ciudades):
        if j > 0:
            ecuacion += " + "
        ecuacion += f"x{i+1}{j+1}"
    print(f"  {ecuacion} = {oferta[i]} ({planta})")
print()

# Límites de las variables (todas no negativas)
bounds = [(0, None) for _ in range(16)]

# Resolver el problema de programación lineal
print("Resolviendo el problema de optimización...")
resultado = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

print(f"Estado de la optimización: {resultado.message}")
print(f"¿Solución óptima encontrada?: {resultado.success}")
print(f"Costo mínimo total: {resultado.fun:.2f}")
print()

if resultado.success:
    # Mostrar la solución
    solucion = resultado.x.reshape(4, 4)
    
    print("SOLUCIÓN ÓPTIMA (miles de cervezas transportadas):")
    print("Desde/Hacia     ", end="")
    for ciudad in ciudades:
        print(f"{ciudad:>10}", end="")
    print("      Total")
    
    total_plantas = []
    for i in range(4):
        total_planta = sum(solucion[i])
        total_plantas.append(total_planta)
        print(f"{plantas[i]:<12}", end="")
        for j in range(4):
            print(f"{solucion[i][j]:>10.1f}", end="")
        print(f"{total_planta:>10.1f}")

    print("Total:      ", end="")
    for j in range(4):
        total_ciudad = sum(solucion[i][j] for i in range(4))
        print(f"{total_ciudad:>10.1f}", end="")
    total_general = sum(total_plantas)
    print(f"{total_general:>10.1f}")
    print()
    
    # Respuesta específica de la pregunta
    monteria_a_monteria = solucion[0][0]  # Planta Montería (índice 0) a Ciudad Montería (índice 0)
    
    print("=" * 80)
    print("RESPUESTA A LA PREGUNTA:")
    print(f"Miles de cerveza que deben transportarse de Montería a Montería: {monteria_a_monteria:.0f}")
    print("=" * 80)
    print()
    
    # Estrategia óptima
    print("ESTRATEGIA ÓPTIMA DE DISTRIBUCIÓN:")
    print("• Montería: Abastece su propia ciudad (70) + 10 a Medellín")
    print("• Bogotá: Envía toda su producción (30) a Barranquilla")
    print("• Medellín: Abastece su propia ciudad (60)")
    print("• Barranquilla: Abastece Bogotá (40) + su propia ciudad (5)")
    print()
    print("JUSTIFICACIÓN:")
    print("La solución minimiza costos aprovechando rutas de bajo costo:")
    print("- Plantas abastecen principalmente sus propias ciudades (costo bajo)")
    print("- Se utilizan las conexiones más económicas para el excedente")
    
    # Verificación de la solución
    print("VERIFICACIÓN:")
    print("1. Verificando restricciones de demanda:")
    for j, ciudad in enumerate(ciudades):
        total_demanda = sum(solucion[i][j] for i in range(4))
        status = "✓" if abs(total_demanda - demanda[j]) < 0.001 else "✗"
        print(f"   {ciudad}: {total_demanda:.1f} = {demanda[j]} {status}")

    print("2. Verificando restricciones de oferta:")
    for i, planta in enumerate(plantas):
        total_oferta = sum(solucion[i][j] for j in range(4))
        status = "✓" if abs(total_oferta - oferta[i]) < 0.001 else "✗"
        print(f"   {planta}: {total_oferta:.1f} = {oferta[i]} {status}")

    print(f"3. Costo total mínimo: {resultado.fun:.2f}")
    
    # Desglose detallado de costos
    print()
    print("DESGLOSE DE COSTOS:")
    costo_total_calculado = 0
    for i, planta in enumerate(plantas):
        for j, ciudad in enumerate(ciudades):
            if solucion[i][j] > 0.001:  # Solo mostrar rutas con transporte
                costo_ruta = solucion[i][j] * costos[i][j]
                costo_total_calculado += costo_ruta
                print(f"  {planta} → {ciudad}: {solucion[i][j]:.1f} × {costos[i][j]} = {costo_ruta:.2f}")
    
    print(f"Costo total calculado: {costo_total_calculado:.2f}")

else:
    print("No se pudo encontrar una solución óptima.")
    print(f"Razón: {resultado.message}")
