import pulp
from itertools import permutations

# Problema de asignación de proveedores a máquinas
print("=== PROBLEMA DE ASIGNACIÓN DE PROVEEDORES ===")

# Matriz de costos: filas = proveedores, columnas = máquinas
# Máquinas: 0=computador, 1=impresora, 2=plancha industrial
costos = [
    [15, 10, 8],   # Proveedor 1: computador, impresora, plancha
    [1, 8, 3],     # Proveedor 2: computador, impresora, plancha
    [1, 3, 7]      # Proveedor 3: computador, impresora, plancha
]

nombres_proveedores = ['Proveedor 1', 'Proveedor 2', 'Proveedor 3']
nombres_maquinas = ['Computador', 'Impresora', 'Plancha Industrial']

print("Matriz de costos:")
print("              Computador  Impresora  Plancha")
for i, nombre in enumerate(nombres_proveedores):
    print(f"{nombre:12} : {costos[i][0]:8} {costos[i][1]:8} {costos[i][2]:8}")

print("\nANÁLISIS DEL PROBLEMA:")
print("- 3 proveedores disponibles")
print("- 3 máquinas para mantenimiento")
print("- Cada proveedor se asigna a exactamente una máquina")
print("- Cada máquina debe ser atendida por exactamente un proveedor")
print("- Objetivo: minimizar el costo total")

# Definir índices
proveedores = range(3)  # 3 proveedores
maquinas = range(3)     # 3 máquinas

print("\n=== SOLUCIÓN CON PuLP ===")

# Crear modelo de optimización
prob = pulp.LpProblem("Asignacion_Proveedores", pulp.LpMinimize)

# Variables de decisión: x[i,j] = 1 si proveedor i se asigna a máquina j
x = {}
for i in proveedores:
    for j in maquinas:
        x[i, j] = pulp.LpVariable(f"x_{i}_{j}", cat='Binary')

# Función objetivo: minimizar costo total
prob += pulp.lpSum(costos[i][j] * x[i, j] for i in proveedores for j in maquinas)

# Restricciones
# 1. Cada proveedor se asigna a exactamente una máquina
for i in proveedores:
    prob += pulp.lpSum(x[i, j] for j in maquinas) == 1

# 2. Cada máquina debe ser atendida por exactamente un proveedor
for j in maquinas:
    prob += pulp.lpSum(x[i, j] for i in proveedores) == 1

# Resolver el problema
prob.solve()

if prob.status == pulp.LpStatusOptimal:
    print(f"Solución óptima encontrada!")
    costo_total = pulp.value(prob.objective)
    print(f"Costo total mínimo: {costo_total}")
    
    print("\nAsignación óptima:")
    asignaciones = {}
    for j in maquinas:
        for i in proveedores:
            if x[i, j].varValue == 1:
                asignaciones[j] = i
                print(f"  {nombres_maquinas[j]}: {nombres_proveedores[i]} (${costos[i][j]})")
    
    # Respuesta específica
    proveedor_plancha = asignaciones[2] + 1  # +1 porque los proveedores se numeran desde 1
    print(f"\n*** RESPUESTA: El proveedor asignado a la plancha industrial es el Proveedor {proveedor_plancha} ***")
    print(f"*** Costo total: {costo_total:.1f} ***")

else:
    print("No se encontró solución factible")

print("\n=== VERIFICACIÓN MANUAL ===")
print("Evaluando todas las posibles asignaciones:")

mejor_costo = float('inf')
mejor_asignacion = None
mejor_detalle = None

# Evaluar todas las permutaciones posibles
# Cada permutación representa qué proveedor va a cada máquina
for perm in permutations(range(3)):
    costo_total = sum(costos[i][perm[i]] for i in range(3))
    
    detalle = []
    for i in range(3):
        maquina_asignada = perm[i]
        detalle.append(f"{nombres_proveedores[i]} -> {nombres_maquinas[maquina_asignada]} (${costos[i][maquina_asignada]})")
    
    print(f"Asignación: {', '.join(detalle)} | Costo total: ${costo_total}")
    
    if costo_total < mejor_costo:
        mejor_costo = costo_total
        mejor_asignacion = perm
        mejor_detalle = detalle.copy()

print(f"\nMejor asignación manual:")
for detalle in mejor_detalle:
    print(f"  {detalle}")
print(f"Costo total óptimo: ${mejor_costo}")

# Determinar qué proveedor va a la plancha industrial (máquina índice 2)
for i in range(3):
    if mejor_asignacion[i] == 2:  # Plancha industrial
        proveedor_plancha_manual = i + 1
        break

print(f"\n*** CONFIRMACIÓN: Proveedor {proveedor_plancha_manual} asignado a la plancha industrial ***")
print(f"*** Respuesta final: {proveedor_plancha_manual:.1f} ***")
