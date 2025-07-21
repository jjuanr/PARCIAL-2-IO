import pulp

# Definir los costos de instalación por empresa y comunidad
# Filas: empresas (1, 2, 3)
# Columnas: comunidades (1, 2, 3)
costos = [
    [183, 210, 277],  # Empresa 1
    [138, 173, 494],  # Empresa 2
    [385, 113, 156]   # Empresa 3
]

# Crear el problema de minimización
prob = pulp.LpProblem("Asignacion_Comunidades", pulp.LpMinimize)

# Definir las variables de decisión
# x[i][j] = 1 si la empresa i es asignada a la comunidad j, 0 en caso contrario
empresas = range(3)
comunidades = range(3)

x = {}
for i in empresas:
    for j in comunidades:
        x[i, j] = pulp.LpVariable(f"x_{i+1}_{j+1}", cat='Binary')

# Función objetivo: minimizar el costo total
prob += pulp.lpSum(costos[i][j] * x[i, j] for i in empresas for j in comunidades)

# Restricciones:
# 1. Cada empresa puede ser asignada a máximo una comunidad
for i in empresas:
    prob += pulp.lpSum(x[i, j] for j in comunidades) <= 1

# 2. Cada comunidad debe ser asignada a exactamente una empresa
for j in comunidades:
    prob += pulp.lpSum(x[i, j] for i in empresas) == 1

# Resolver el problema
prob.solve()

# Mostrar el estado de la solución
print("Estado de la solución:", pulp.LpStatus[prob.status])

# Mostrar la asignación óptima
print("\nAsignación óptima:")
costo_total = 0
for i in empresas:
    for j in comunidades:
        if x[i, j].varValue == 1:
            print(f"Empresa {i+1} -> Comunidad {j+1}, Costo: {costos[i][j]}")
            costo_total += costos[i][j]

print(f"\nCosto mínimo total: {costo_total}")
print(f"Costo mínimo total (redondeado a 1 decimal): {round(costo_total, 1)}")

# Verificar todas las posibles asignaciones para validar
print("\n--- Verificación manual de todas las posibles asignaciones ---")
import itertools

# Generar todas las permutaciones posibles de asignar 3 empresas a 3 comunidades
todas_asignaciones = list(itertools.permutations(range(3)))

min_costo = float('inf')
mejor_asignacion = None

print("Todas las posibles asignaciones:")
for asignacion in todas_asignaciones:
    costo = sum(costos[empresa][comunidad] for empresa, comunidad in enumerate(asignacion))
    print(f"Empresas {[i+1 for i in range(3)]} -> Comunidades {[j+1 for j in asignacion]}, Costo: {costo}")
    
    if costo < min_costo:
        min_costo = costo
        mejor_asignacion = asignacion

print(f"\nMejor asignación encontrada manualmente:")
for empresa, comunidad in enumerate(mejor_asignacion):
    print(f"Empresa {empresa+1} -> Comunidad {comunidad+1}, Costo: {costos[empresa][comunidad]}")

print(f"Costo mínimo verificado: {min_costo}")
print(f"Costo mínimo verificado (redondeado a 1 decimal): {round(min_costo, 1)}")
