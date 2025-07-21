import pulp
import itertools

# Problema: Asignación de líderes a clientes
# Tenemos 4 líderes y 3 clientes
# Cada cliente debe ser asignado a exactamente un líder
# Cada líder puede ser asignado a máximo un cliente
# Objetivo: minimizar el tiempo total requerido

# Definir los tiempos de ejecución por líder y cliente
# Filas: líderes (1, 2, 3, 4)
# Columnas: clientes (1, 2, 3)
tiempos = [
    [14, 5, 19],  # Líder 1
    [18, 8, 18],  # Líder 2
    [17, 6, 10],  # Líder 3
    [7, 3, 5]     # Líder 4
]

print("Matriz de tiempos (meses):")
print("           Cliente 1  Cliente 2  Cliente 3")
for i, fila in enumerate(tiempos):
    print(f"Líder {i+1}:        {fila[0]}         {fila[1]}         {fila[2]}")
print()

# Crear el problema de minimización
prob = pulp.LpProblem("Asignacion_Lideres_Clientes", pulp.LpMinimize)

# Definir las variables de decisión
# x[i][j] = 1 si el líder i es asignado al cliente j, 0 en caso contrario
lideres = range(4)  # 4 líderes
clientes = range(3)  # 3 clientes

x = {}
for i in lideres:
    for j in clientes:
        x[i, j] = pulp.LpVariable(f"x_lider{i+1}_cliente{j+1}", cat='Binary')

# Función objetivo: minimizar el tiempo total
prob += pulp.lpSum(tiempos[i][j] * x[i, j] for i in lideres for j in clientes)

# Restricciones:
# 1. Cada líder puede ser asignado a máximo un cliente
for i in lideres:
    prob += pulp.lpSum(x[i, j] for j in clientes) <= 1

# 2. Cada cliente debe ser asignado a exactamente un líder
for j in clientes:
    prob += pulp.lpSum(x[i, j] for i in lideres) == 1

# Resolver el problema
prob.solve()

# Mostrar el estado de la solución
print("Estado de la solución:", pulp.LpStatus[prob.status])

# Mostrar la asignación óptima
print("\nAsignación óptima:")
tiempo_total = 0
asignaciones = {}

for i in lideres:
    for j in clientes:
        if x[i, j].varValue == 1:
            print(f"Líder {i+1} -> Cliente {j+1}, Tiempo: {tiempos[i][j]} meses")
            tiempo_total += tiempos[i][j]
            asignaciones[j+1] = i+1  # Cliente -> Líder

print(f"\nTiempo total mínimo: {tiempo_total} meses")

# Mostrar qué líder no fue asignado
lideres_asignados = set(asignaciones.values())
lideres_disponibles = set(range(1, 5))
lider_no_asignado = lideres_disponibles - lideres_asignados

print(f"Líder(es) no asignado(s): {list(lider_no_asignado)}")

# Respuesta específica para la pregunta
print(f"\n*** RESPUESTA: El líder asignado al Cliente 1 es el Líder {asignaciones[1]} ***")

# Verificación manual explorando todas las combinaciones posibles
print("\n--- Verificación manual ---")
print("Explorando todas las combinaciones posibles de asignar 3 líderes a 3 clientes:")

# Generar todas las combinaciones de 3 líderes de los 4 disponibles
from itertools import combinations, permutations

min_tiempo = float('inf')
mejor_asignacion = None

combinaciones_lideres = list(combinations(range(4), 3))
todas_asignaciones = []

for combo_lideres in combinaciones_lideres:
    # Para cada combinación de 3 líderes, generar todas las permutaciones
    for perm in permutations(combo_lideres):
        tiempo = sum(tiempos[lider][cliente] for cliente, lider in enumerate(perm))
        asignacion_desc = [(cliente+1, lider+1, tiempos[lider][cliente]) for cliente, lider in enumerate(perm)]
        todas_asignaciones.append((tiempo, asignacion_desc))
        
        if tiempo < min_tiempo:
            min_tiempo = tiempo
            mejor_asignacion = asignacion_desc

# Ordenar por tiempo total
todas_asignaciones.sort()

print(f"\nTodas las posibles asignaciones (ordenadas por tiempo total):")
for i, (tiempo, asignacion) in enumerate(todas_asignaciones):
    print(f"Opción {i+1}: Tiempo total = {tiempo}")
    for cliente, lider, tiempo_individual in asignacion:
        print(f"  Cliente {cliente} -> Líder {lider} ({tiempo_individual} meses)")
    print()

print(f"Mejor asignación encontrada manualmente:")
for cliente, lider, tiempo_individual in mejor_asignacion:
    print(f"Cliente {cliente} -> Líder {lider} ({tiempo_individual} meses)")

print(f"Tiempo mínimo verificado: {min_tiempo} meses")

# Confirmar respuesta
cliente_1_lider = None
for cliente, lider, _ in mejor_asignacion:
    if cliente == 1:
        cliente_1_lider = lider
        break

print(f"\n*** CONFIRMACIÓN: El líder asignado al Cliente 1 es el Líder {cliente_1_lider} ***")
