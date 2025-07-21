import pulp
from itertools import product

# Problema: Asignación de integrantes del equipo a pruebas de relevo
# Tenemos 4 integrantes y 4 pruebas
# Cada prueba debe ser asignada a exactamente un integrante
# Cada integrante puede ser asignado a máximo 2 pruebas
# Objetivo: minimizar el tiempo total del relevo

# Definir los tiempos de ejecución por integrante y prueba (en minutos)
# Filas: integrantes (Pedro, Juliana, Leonardo, Diana)
# Columnas: pruebas (Natación, Equilibrio, Aire, Fuerza)
tiempos = [
    [27, 30, 26.5, 26.5],     # Pedro
    [26.5, 28.5, 26, 26],     # Juliana
    [28, 28.5, 27, 28],       # Leonardo
    [27, 27, 27.5, 28.5]      # Diana
]

nombres_integrantes = ["Pedro", "Juliana", "Leonardo", "Diana"]
nombres_pruebas = ["Natación", "Equilibrio", "Aire", "Fuerza"]

print("Matriz de tiempos (minutos):")
print("            Natación  Equilibrio   Aire     Fuerza")
for i, fila in enumerate(tiempos):
    print(f"{nombres_integrantes[i]:10}:   {fila[0]:6}    {fila[1]:6}     {fila[2]:6}   {fila[3]:6}")
print()

# Crear el problema de minimización usando PuLP
prob = pulp.LpProblem("Pruebas_Relevo", pulp.LpMinimize)

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
# 1. Cada integrante puede realizar máximo 2 pruebas
for i in integrantes:
    prob += pulp.lpSum(x[i, j] for j in pruebas) <= 2

# 2. Cada prueba debe ser asignada a exactamente un integrante
for j in pruebas:
    prob += pulp.lpSum(x[i, j] for i in integrantes) == 1

# Resolver el problema
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
    
    # Mostrar distribución de pruebas por integrante
    print("\nDistribución de pruebas por integrante:")
    for i in integrantes:
        pruebas_asignadas = []
        for j in pruebas:
            if x[i, j].varValue == 1:
                pruebas_asignadas.append(nombres_pruebas[j])
        print(f"{nombres_integrantes[i]}: {len(pruebas_asignadas)} prueba(s) - {', '.join(pruebas_asignadas)}")
    
    print(f"\n*** RESPUESTA: {round(tiempo_total, 1)} ***")

# Verificación manual - encontrar todas las asignaciones válidas
print("\n--- Verificación Manual ---")

def generar_asignaciones_validas():
    """Genera todas las asignaciones válidas donde cada prueba se asigna a exactamente 
    un integrante y cada integrante puede hacer máximo 2 pruebas"""
    
    asignaciones_validas = []
    
    # Para cada prueba, puede ser asignada a cualquiera de los 4 integrantes
    for asignacion in product(range(4), repeat=4):
        # Contar cuántas pruebas tiene cada integrante
        contador_integrantes = [0] * 4
        for integrante in asignacion:
            contador_integrantes[integrante] += 1
        
        # Verificar que ningún integrante tenga más de 2 pruebas
        if all(count <= 2 for count in contador_integrantes):
            asignaciones_validas.append(asignacion)
    
    return asignaciones_validas

print("Generando todas las asignaciones válidas...")
asignaciones_validas = generar_asignaciones_validas()
print(f"Número total de asignaciones válidas: {len(asignaciones_validas)}")

# Evaluar todas las asignaciones válidas
mejor_tiempo = float('inf')
mejor_asignacion = None
resultados = []

for asignacion in asignaciones_validas:
    tiempo_total_temp = sum(tiempos[integrante][prueba] for prueba, integrante in enumerate(asignacion))
    
    asignacion_desc = []
    for prueba, integrante in enumerate(asignacion):
        asignacion_desc.append((nombres_pruebas[prueba], nombres_integrantes[integrante], tiempos[integrante][prueba]))
    
    resultados.append((tiempo_total_temp, asignacion_desc, asignacion))
    
    if tiempo_total_temp < mejor_tiempo:
        mejor_tiempo = tiempo_total_temp
        mejor_asignacion = asignacion_desc

# Ordenar resultados por tiempo total
resultados.sort()

print(f"\nMejores 5 asignaciones encontradas:")
for i, (tiempo, asignacion_desc, asignacion) in enumerate(resultados[:5]):
    print(f"\nOpción {i+1}: Tiempo total = {tiempo}")
    for prueba, integrante, tiempo_individual in asignacion_desc:
        print(f"  {prueba} -> {integrante} ({tiempo_individual} min)")
    
    # Mostrar distribución de pruebas por integrante
    distribucion = {}
    for prueba, integrante, _ in asignacion_desc:
        if integrante not in distribucion:
            distribucion[integrante] = []
        distribucion[integrante].append(prueba)
    
    print("  Distribución:", end=" ")
    for integrante in nombres_integrantes:
        if integrante in distribucion:
            print(f"{integrante}({len(distribucion[integrante])})", end=" ")
        else:
            print(f"{integrante}(0)", end=" ")

print(f"\n\nMejor asignación encontrada:")
for prueba, integrante, tiempo_individual in mejor_asignacion:
    print(f"{prueba} -> {integrante} ({tiempo_individual} minutos)")

print(f"\nTiempo mínimo verificado: {mejor_tiempo}")
print(f"Tiempo mínimo verificado (redondeado a 1 decimal): {round(mejor_tiempo, 1)}")

print(f"\n*** CONFIRMACIÓN: El tiempo mínimo es {round(mejor_tiempo, 1)} minutos ***")
