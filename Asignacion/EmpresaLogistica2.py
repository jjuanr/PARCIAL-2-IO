import pulp
from itertools import permutations, product

# Problema simplificado: buscar todas las asignaciones válidas
print("=== ANÁLISIS EXHAUSTIVO DEL PROBLEMA ===")

# Matrices de costos
costos_lunes = [
    [3, 6, 9],  # Transportista 1: Bogotá, Medellín, Cali
    [7, 9, 5],  # Transportista 2: Bogotá, Medellín, Cali  
    [6, 7, 8],  # Transportista 3: Bogotá, Medellín, Cali
    [1, 3, 6]   # Transportista 4: Bogotá, Medellín, Cali
]

costos_jueves = [
    [1, 3, 2],  # Transportista 1: Bogotá, Medellín, Cali
    [8, 5, 7],  # Transportista 2: Bogotá, Medellín, Cali
    [9, 6, 8],  # Transportista 3: Bogotá, Medellín, Cali
    [6, 8, 5]   # Transportista 4: Bogotá, Medellín, Cali
]

nombres_transportistas = ['T1', 'T2', 'T3', 'T4']
nombres_ciudades = ['Bogotá', 'Medellín', 'Cali']

print("ENFOQUE: Generar todas las combinaciones válidas")
print("Restricciones:")
print("- Cada transportista va exactamente a una ciudad cada día")
print("- No puede ir a la misma ciudad ambos días")
print("- Cada ciudad debe tener al menos un transportista cada día")
print()

def evaluar_asignacion(asig_lunes, asig_jueves):
    """Evaluar si una asignación es válida y calcular su costo"""
    # Verificar que no vayan a la misma ciudad ambos días
    for i in range(4):
        if asig_lunes[i] == asig_jueves[i]:
            return False, 0, "Mismo transportista a misma ciudad"
    
    # Verificar que cada ciudad tenga al menos un transportista cada día
    ciudades_lunes = set(asig_lunes)
    ciudades_jueves = set(asig_jueves)
    
    if len(ciudades_lunes) < 3:
        return False, 0, f"Lunes faltan ciudades: {set(range(3)) - ciudades_lunes}"
    if len(ciudades_jueves) < 3:
        return False, 0, f"Jueves faltan ciudades: {set(range(3)) - ciudades_jueves}"
    
    # Calcular costo
    costo_lunes = sum(costos_lunes[i][asig_lunes[i]] for i in range(4))
    costo_jueves = sum(costos_jueves[i][asig_jueves[i]] for i in range(4))
    costo_total = costo_lunes + costo_jueves
    
    return True, costo_total, "Válida"

print("Generando todas las asignaciones posibles...")

# Generar todas las combinaciones posibles
# Cada transportista puede ir a cualquiera de las 3 ciudades
combinaciones_lunes = list(product(range(3), repeat=4))
combinaciones_jueves = list(product(range(3), repeat=4))

print(f"Total combinaciones a evaluar: {len(combinaciones_lunes)} × {len(combinaciones_jueves)} = {len(combinaciones_lunes) * len(combinaciones_jueves):,}")

asignaciones_validas = []
contador = 0

for asig_lunes in combinaciones_lunes:
    for asig_jueves in combinaciones_jueves:
        contador += 1
        if contador % 10000 == 0:
            print(f"Evaluadas: {contador:,}")
        
        valida, costo, razon = evaluar_asignacion(asig_lunes, asig_jueves)
        if valida:
            asignaciones_validas.append((costo, asig_lunes, asig_jueves))

print(f"\nTotal evaluadas: {contador:,}")
print(f"Asignaciones válidas encontradas: {len(asignaciones_validas)}")

if asignaciones_validas:
    # Ordenar por costo
    asignaciones_validas.sort()
    
    print(f"\nMejores 10 asignaciones:")
    for i in range(min(10, len(asignaciones_validas))):
        costo, asig_lunes, asig_jueves = asignaciones_validas[i]
        print(f"\n{i+1}. Costo total: {costo}")
        print("   LUNES:", end=" ")
        for j, ciudad in enumerate(asig_lunes):
            print(f"{nombres_transportistas[j]}->{nombres_ciudades[ciudad]}({costos_lunes[j][ciudad]})", end=" ")
        print()
        print("   JUEVES:", end=" ")
        for j, ciudad in enumerate(asig_jueves):
            print(f"{nombres_transportistas[j]}->{nombres_ciudades[ciudad]}({costos_jueves[j][ciudad]})", end=" ")
        print()
    
    mejor_costo = asignaciones_validas[0][0]
    print(f"\n*** RESPUESTA ÓPTIMA: {mejor_costo} ***")
else:
    print("No se encontraron asignaciones válidas")

print(f"\n*** RESPUESTA FINAL: {mejor_costo if asignaciones_validas else 'No factible'} ***")
