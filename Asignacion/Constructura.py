import pulp
from itertools import combinations, permutations

# Problema: Asignación de trabajadores a procesos constructivos
# Tenemos 5 candidatos y 4 procesos constructivos
# Cada proceso debe ser asignado a exactamente un trabajador
# Cada trabajador puede ser asignado a máximo un proceso
# Objetivo: minimizar el tiempo total

# Definir los tiempos de ejecución por trabajador y proceso (en minutos)
# Filas: trabajadores (Denis, Yuly, Lucía, Carlos, Ariel)
# Columnas: procesos (Mampostería, Enchape, Pintura, Baldosado)
tiempos = [
    [10, 9, 6, 7],   # Denis
    [8, 7, 6, 8],    # Yuly
    [8, 6, 5, 9],    # Lucía
    [5, 7, 7, 10],   # Carlos
    [8, 7, 6, 3]     # Ariel
]

nombres_trabajadores = ["Denis", "Yuly", "Lucía", "Carlos", "Ariel"]
nombres_procesos = ["Mampostería", "Enchape", "Pintura", "Baldosado"]

print("Matriz de tiempos (minutos):")
print("         Mampostería  Enchape  Pintura  Baldosado")
for i, fila in enumerate(tiempos):
    print(f"{nombres_trabajadores[i]:8}: {fila[0]:10} {fila[1]:8} {fila[2]:8} {fila[3]:9}")
print()

# Crear el problema de minimización usando PuLP
prob = pulp.LpProblem("Constructora_Asignacion", pulp.LpMinimize)

# Definir las variables de decisión
# x[i][j] = 1 si el trabajador i es asignado al proceso j, 0 en caso contrario
trabajadores = range(5)  # 5 trabajadores
procesos = range(4)      # 4 procesos

x = {}
for i in trabajadores:
    for j in procesos:
        x[i, j] = pulp.LpVariable(f"x_{i}_{j}", cat='Binary')

# Función objetivo: minimizar el tiempo total
prob += pulp.lpSum(tiempos[i][j] * x[i, j] for i in trabajadores for j in procesos)

# Restricciones:
# 1. Cada trabajador puede ser asignado a máximo un proceso
for i in trabajadores:
    prob += pulp.lpSum(x[i, j] for j in procesos) <= 1

# 2. Cada proceso debe ser asignado a exactamente un trabajador
for j in procesos:
    prob += pulp.lpSum(x[i, j] for i in trabajadores) == 1

# Resolver el problema
print("Resolviendo el problema de optimización...")
prob.solve()

# Mostrar el estado de la solución
print("Estado de la solución:", pulp.LpStatus[prob.status])

if prob.status == pulp.LpStatusOptimal:
    # Mostrar la asignación óptima
    print("\nAsignación óptima:")
    tiempo_total = 0
    
    for i in trabajadores:
        for j in procesos:
            if x[i, j].varValue == 1:
                print(f"{nombres_trabajadores[i]} -> {nombres_procesos[j]}, Tiempo: {tiempos[i][j]} minutos")
                tiempo_total += tiempos[i][j]
    
    print(f"\nTiempo total mínimo: {tiempo_total} minutos")
    print(f"Tiempo total mínimo (redondeado a 1 decimal): {round(tiempo_total, 1)} minutos")
    
    # Mostrar quién no fue seleccionado
    trabajadores_asignados = set()
    for i in trabajadores:
        for j in procesos:
            if x[i, j].varValue == 1:
                trabajadores_asignados.add(i)
    
    trabajadores_no_asignados = set(range(5)) - trabajadores_asignados
    if trabajadores_no_asignados:
        print(f"\nTrabajador(es) no seleccionado(s): {[nombres_trabajadores[i] for i in trabajadores_no_asignados]}")
    
    print(f"\n*** RESPUESTA: {round(tiempo_total, 1)} ***")

else:
    print("No se encontró una solución óptima")

# Verificación manual - generar todas las asignaciones posibles
print("\n--- Verificación Manual ---")
print("Generando todas las posibles asignaciones válidas:")

def generar_asignaciones_validas():
    """Genera todas las asignaciones válidas donde se eligen 4 trabajadores de 5 
    y se asigna cada uno a un proceso diferente"""
    
    asignaciones_validas = []
    
    # Generar todas las combinaciones de 4 trabajadores de 5
    combinaciones_trabajadores = list(combinations(range(5), 4))
    
    for combo_trabajadores in combinaciones_trabajadores:
        # Para cada combinación de trabajadores, generar todas las permutaciones
        # de asignación a los 4 procesos
        for perm in permutations(combo_trabajadores):
            asignaciones_validas.append(perm)
    
    return asignaciones_validas

asignaciones_validas = generar_asignaciones_validas()
print(f"Número total de asignaciones válidas: {len(asignaciones_validas)}")

# Evaluar todas las asignaciones válidas
mejor_tiempo = float('inf')
mejor_asignacion = None
resultados = []

for asignacion in asignaciones_validas:
    tiempo_total_temp = sum(tiempos[trabajador][proceso] for proceso, trabajador in enumerate(asignacion))
    
    asignacion_desc = []
    for proceso, trabajador in enumerate(asignacion):
        asignacion_desc.append((nombres_procesos[proceso], nombres_trabajadores[trabajador], tiempos[trabajador][proceso]))
    
    resultados.append((tiempo_total_temp, asignacion_desc, asignacion))
    
    if tiempo_total_temp < mejor_tiempo:
        mejor_tiempo = tiempo_total_temp
        mejor_asignacion = asignacion_desc

# Ordenar resultados por tiempo total
resultados.sort()

print(f"\nMejores 10 asignaciones encontradas:")
for i, (tiempo, asignacion_desc, asignacion) in enumerate(resultados[:10]):
    print(f"\nOpción {i+1}: Tiempo total = {tiempo}")
    trabajadores_usados = set()
    for proceso, trabajador, tiempo_individual in asignacion_desc:
        print(f"  {proceso} -> {trabajador} ({tiempo_individual} min)")
        trabajadores_usados.add(trabajador)
    
    # Mostrar quién no fue seleccionado
    todos_trabajadores = set(nombres_trabajadores)
    no_seleccionados = todos_trabajadores - trabajadores_usados
    if no_seleccionados:
        print(f"  No seleccionado: {', '.join(no_seleccionados)}")

print(f"\nMejor asignación encontrada manualmente:")
trabajadores_utilizados = set()
for proceso, trabajador, tiempo_individual in mejor_asignacion:
    print(f"{proceso} -> {trabajador} ({tiempo_individual} minutos)")
    trabajadores_utilizados.add(trabajador)

# Mostrar quién no fue seleccionado
todos_trabajadores = set(nombres_trabajadores)
no_seleccionado = todos_trabajadores - trabajadores_utilizados
if no_seleccionado:
    print(f"No seleccionado: {', '.join(no_seleccionado)}")

print(f"Tiempo mínimo verificado: {mejor_tiempo}")
print(f"Tiempo mínimo verificado (redondeado a 1 decimal): {round(mejor_tiempo, 1)}")

print(f"\n*** CONFIRMACIÓN: {round(mejor_tiempo, 1)} ***")

# Análisis adicional
print(f"\n--- Análisis Adicional ---")
print("Tiempos mínimos por proceso (sin considerar restricciones):")
for j, proceso in enumerate(nombres_procesos):
    tiempos_proceso = [tiempos[i][j] for i in trabajadores]
    min_tiempo = min(tiempos_proceso)
    mejor_trabajador = nombres_trabajadores[tiempos_proceso.index(min_tiempo)]
    print(f"{proceso}: {min_tiempo} min ({mejor_trabajador})")

print(f"Suma teórica mínima (sin restricciones): {sum(min(tiempos[i][j] for i in trabajadores) for j in procesos)} min")
print("Nota: Esta suma no es alcanzable porque varios procesos requieren al mismo trabajador.")
