import pulp
from itertools import permutations

# Problema: Asignación de integrantes del equipo a pruebas de relevo con restricción
# Tenemos 4 integrantes y 4 pruebas
# Restricción especial: Pedro DEBE hacer la prueba de fuerza
# Cada prueba debe ser asignada a exactamente un integrante
# Cada integrante puede hacer máximo una prueba
# Objetivo: minimizar el tiempo total del relevo

# Definir los tiempos de ejecución por integrante y prueba (en minutos)
# Filas: integrantes (Pedro, Juliana, Leonardo, Diana)
# Columnas: pruebas (Natación, Equilibrio, Aire, Fuerza)
tiempos = [
    [27, 27.5, 25.9, 26.5],     # Pedro
    [28.5, 28.5, 26, 26],       # Juliana
    [25, 26.5, 27, 28],         # Leonardo
    [28, 30, 27.5, 28.5]        # Diana
]

nombres_integrantes = ["Pedro", "Juliana", "Leonardo", "Diana"]
nombres_pruebas = ["Natación", "Equilibrio", "Aire", "Fuerza"]

print("Matriz de tiempos (minutos):")
print("            Natación  Equilibrio   Aire     Fuerza")
for i, fila in enumerate(tiempos):
    print(f"{nombres_integrantes[i]:10}:   {fila[0]:6}    {fila[1]:6}     {fila[2]:6}   {fila[3]:6}")
print()

print("RESTRICCIÓN ESPECIAL: Pedro debe realizar la prueba de Fuerza")
print(f"Tiempo fijo: Pedro -> Fuerza = {tiempos[0][3]} minutos")
print()

# Crear el problema de minimización usando PuLP
prob = pulp.LpProblem("Pruebas_Relevo_Restriccion", pulp.LpMinimize)

# Definir las variables de decisión
# x[i][j] = 1 si el integrante i es asignado a la prueba j, 0 en caso contrario
integrantes = range(4)  # 4 integrantes
pruebas = range(4)      # 4 pruebas

x = {}
for i in integrantes:
    for j in pruebas:
        x[i, j] = pulp.LpVariable(f"x_{i}_{j}", cat='Binary')

# Función objetivo: minimizar el tiempo total
prob += pulp.lpSum(tiempos[i][j] * x[i, j] for i in integrantes for j in pruebas)

# Restricciones:
# 1. Cada integrante puede realizar máximo una prueba
for i in integrantes:
    prob += pulp.lpSum(x[i, j] for j in pruebas) <= 1

# 2. Cada prueba debe ser asignada a exactamente un integrante
for j in pruebas:
    prob += pulp.lpSum(x[i, j] for i in integrantes) == 1

# 3. RESTRICCIÓN ESPECIAL: Pedro (índice 0) DEBE hacer Fuerza (índice 3)
prob += x[0, 3] == 1

# Resolver el problema
print("Resolviendo el problema de optimización...")
prob.solve()

# Mostrar el estado de la solución
print("Estado de la solución:", pulp.LpStatus[prob.status])

if prob.status == pulp.LpStatusOptimal:
    # Mostrar la asignación óptima
    print("\nAsignación óptima:")
    tiempo_total = 0
    
    for i in integrantes:
        for j in pruebas:
            if x[i, j].varValue == 1:
                print(f"{nombres_integrantes[i]} -> {nombres_pruebas[j]}, Tiempo: {tiempos[i][j]} minutos")
                tiempo_total += tiempos[i][j]
    
    print(f"\nTiempo total mínimo: {tiempo_total} minutos")
    print(f"Tiempo total mínimo (redondeado a 1 decimal): {round(tiempo_total, 1)} minutos")
    
    print(f"\n*** RESPUESTA: {round(tiempo_total, 1)} ***")

else:
    print("No se encontró una solución óptima")

# Verificación manual
print("\n--- Verificación Manual ---")
print("Como Pedro debe hacer Fuerza, solo necesitamos asignar las otras 3 pruebas")
print("a los otros 3 integrantes de manera óptima.")
print()

# Tiempo fijo de Pedro haciendo Fuerza
tiempo_pedro = tiempos[0][3]  # Pedro -> Fuerza
print(f"Tiempo fijo: Pedro -> Fuerza = {tiempo_pedro} minutos")
print()

# Las pruebas restantes: Natación (0), Equilibrio (1), Aire (2)
# Los integrantes restantes: Juliana (1), Leonardo (2), Diana (3)
pruebas_restantes = [0, 1, 2]  # Natación, Equilibrio, Aire
integrantes_restantes = [1, 2, 3]  # Juliana, Leonardo, Diana

print("Matriz de tiempos para asignaciones restantes:")
print("            Natación  Equilibrio   Aire")
for i in integrantes_restantes:
    tiempos_restantes = [tiempos[i][j] for j in pruebas_restantes]
    print(f"{nombres_integrantes[i]:10}:   {tiempos_restantes[0]:6}    {tiempos_restantes[1]:6}     {tiempos_restantes[2]:6}")
print()

# Generar todas las permutaciones posibles de asignación
print("Evaluando todas las posibles asignaciones para las 3 pruebas restantes:")

mejor_tiempo_total = float('inf')
mejor_asignacion = None
todas_asignaciones = []

# Generar todas las permutaciones de los 3 integrantes restantes a las 3 pruebas restantes
for perm in permutations(integrantes_restantes):
    tiempo_asignacion = tiempo_pedro  # Empezar con el tiempo fijo de Pedro
    asignacion_desc = [("Fuerza", "Pedro", tiempo_pedro)]
    
    for idx_prueba, integrante in enumerate(perm):
        prueba = pruebas_restantes[idx_prueba]
        tiempo_individual = tiempos[integrante][prueba]
        tiempo_asignacion += tiempo_individual
        asignacion_desc.append((nombres_pruebas[prueba], nombres_integrantes[integrante], tiempo_individual))
    
    todas_asignaciones.append((tiempo_asignacion, asignacion_desc))
    
    if tiempo_asignacion < mejor_tiempo_total:
        mejor_tiempo_total = tiempo_asignacion
        mejor_asignacion = asignacion_desc

# Ordenar asignaciones por tiempo total
todas_asignaciones.sort()

print("Todas las posibles asignaciones (ordenadas por tiempo total):")
for i, (tiempo, asignacion) in enumerate(todas_asignaciones):
    print(f"\nOpción {i+1}: Tiempo total = {tiempo}")
    for prueba, integrante, tiempo_individual in asignacion:
        print(f"  {prueba} -> {integrante} ({tiempo_individual} min)")

print(f"\nMejor asignación encontrada manualmente:")
for prueba, integrante, tiempo_individual in mejor_asignacion:
    print(f"{prueba} -> {integrante} ({tiempo_individual} minutos)")

print(f"\nTiempo mínimo verificado: {mejor_tiempo_total}")
print(f"Tiempo mínimo verificado (redondeado a 1 decimal): {round(mejor_tiempo_total, 1)}")

print(f"\n*** CONFIRMACIÓN: {round(mejor_tiempo_total, 1)} ***")

# Análisis adicional
print(f"\n--- Análisis Adicional ---")
print("Comparación con la solución sin restricción:")

# Calcular el tiempo óptimo sin restricción (para referencia)
print("Tiempos mínimos por prueba (sin restricciones):")
for j, prueba in enumerate(nombres_pruebas):
    tiempos_prueba = [tiempos[i][j] for i in integrantes]
    min_tiempo = min(tiempos_prueba)
    mejor_integrante = nombres_integrantes[tiempos_prueba.index(min_tiempo)]
    print(f"{prueba}: {min_tiempo} min ({mejor_integrante})")

tiempo_teorico_sin_restriccion = sum(min(tiempos[i][j] for i in integrantes) for j in pruebas)
print(f"Tiempo teórico mínimo sin restricciones: {tiempo_teorico_sin_restriccion} min")

diferencia = mejor_tiempo_total - tiempo_teorico_sin_restriccion
print(f"Diferencia por la restricción de Pedro: {diferencia} min")
print(f"(Costo adicional de que Pedro haga Fuerza en lugar del mejor integrante para esa prueba)")
