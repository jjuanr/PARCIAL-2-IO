import pulp
from itertools import permutations

# Problema de asignación de traductores con restricciones
print("=== PROBLEMA DE ASIGNACIÓN DE TRADUCTORES CON RESTRICCIONES ===")

# Matriz de horas: filas = traductores, columnas = capítulos
# Traductores: 0=Bibiana, 1=Dayana, 2=Mario, 3=Juan
# Capítulos: 0=Cap14, 1=Cap15, 2=Cap16, 3=Cap17
horas = [
    [90, 88, 105, 110],   # Bibiana: Cap14, 15, 16, 17
    [116, 109, 107, 96],  # Dayana: Cap14, 15, 16, 17
    [120, 102, 113, 111], # Mario: Cap14, 15, 16, 17
    [114, 105, 118, 115]  # Juan: Cap14, 15, 16, 17
]

nombres_traductores = ['Bibiana', 'Dayana', 'Mario', 'Juan']
nombres_capitulos = ['Capítulo 14', 'Capítulo 15', 'Capítulo 16', 'Capítulo 17']

print("Matriz de horas de trabajo:")
print("         Cap 14  Cap 15  Cap 16  Cap 17")
for i, nombre in enumerate(nombres_traductores):
    print(f"{nombre:8} : {horas[i][0]:6} {horas[i][1]:6} {horas[i][2]:6} {horas[i][3]:6}")

print("\nRESTRICCIONES ESPECIALES:")
print("- Traductor 1 (Bibiana) NO puede realizar el Capítulo 14")
print("- Traductor 4 (Juan) NO puede realizar el Capítulo 17")

print("\nANÁLISIS DEL PROBLEMA:")
print("- 4 traductores disponibles")
print("- 4 capítulos para traducir")
print("- Cada traductor se asigna a máximo un capítulo")
print("- Cada capítulo debe ser atendido por exactamente un traductor")
print("- Objetivo: minimizar las horas totales")

# Definir índices
traductores = range(4)  # 4 traductores
capitulos = range(4)    # 4 capítulos

print("\n=== SOLUCIÓN CON PuLP ===")

# Crear modelo de optimización
prob = pulp.LpProblem("Asignacion_Traductores_Restricciones", pulp.LpMinimize)

# Variables de decisión: x[i,j] = 1 si traductor i se asigna a capítulo j
x = {}
for i in traductores:
    for j in capitulos:
        x[i, j] = pulp.LpVariable(f"x_{i}_{j}", cat='Binary')

# Función objetivo: minimizar horas totales
prob += pulp.lpSum(horas[i][j] * x[i, j] for i in traductores for j in capitulos)

# Restricciones básicas
# 1. Cada traductor se asigna a máximo un capítulo
for i in traductores:
    prob += pulp.lpSum(x[i, j] for j in capitulos) <= 1

# 2. Cada capítulo debe ser atendido por exactamente un traductor
for j in capitulos:
    prob += pulp.lpSum(x[i, j] for i in traductores) == 1

# Restricciones especiales
# 3. Bibiana (traductor 0) NO puede hacer Capítulo 14 (capítulo 0)
prob += x[0, 0] == 0

# 4. Juan (traductor 3) NO puede hacer Capítulo 17 (capítulo 3)
prob += x[3, 3] == 0

# Resolver el problema
prob.solve()

if prob.status == pulp.LpStatusOptimal:
    print(f"Solución óptima encontrada!")
    horas_total = pulp.value(prob.objective)
    print(f"Horas totales mínimas: {horas_total}")
    
    print("\nAsignación óptima:")
    asignaciones = {}
    for j in capitulos:
        for i in traductores:
            if x[i, j].varValue == 1:
                asignaciones[j] = i
                print(f"  {nombres_capitulos[j]}: {nombres_traductores[i]} ({horas[i][j]} horas)")
    
    print(f"\n*** RESPUESTA: {horas_total:.1f} horas ***")

else:
    print("No se encontró solución factible")

print("\n=== VERIFICACIÓN MANUAL ===")
print("Evaluando todas las asignaciones válidas:")

mejor_horas = float('inf')
mejor_asignacion = None
mejor_detalle = None

# Evaluar todas las permutaciones posibles respetando las restricciones
contador_validas = 0
for perm in permutations(range(4)):
    # Verificar restricciones
    # Bibiana (0) no puede hacer Cap 14 (posición 0)
    if perm[0] == 0:  # Si Bibiana está asignada al Cap 14
        continue
    
    # Juan (3) no puede hacer Cap 17 (posición 3)  
    if perm[3] == 3:  # Si Juan está asignado al Cap 17
        continue
    
    contador_validas += 1
    
    # Calcular costo total de esta asignación
    horas_total = sum(horas[perm[j]][j] for j in range(4))
    
    detalle = []
    for j in range(4):
        traductor_asignado = perm[j]
        detalle.append(f"{nombres_capitulos[j]}: {nombres_traductores[traductor_asignado]} ({horas[traductor_asignado][j]}h)")
    
    print(f"Asignación {contador_validas}: {' | '.join(detalle)} = {horas_total} horas")
    
    if horas_total < mejor_horas:
        mejor_horas = horas_total
        mejor_asignacion = perm
        mejor_detalle = detalle.copy()

print(f"\nTotal de asignaciones válidas evaluadas: {contador_validas}")
print(f"\nMejor asignación manual:")
for detalle in mejor_detalle:
    print(f"  {detalle}")
print(f"Horas totales mínimas: {mejor_horas}")

print(f"\n*** CONFIRMACIÓN: {mejor_horas:.1f} horas ***")
