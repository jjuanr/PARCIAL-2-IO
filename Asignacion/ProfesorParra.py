import pulp
from itertools import combinations

# Datos del problema de traductores
print("=== PROBLEMA DE ASIGNACIÓN DE TRADUCTORES ===")

# Matriz de horas que tomaría cada traductor para cada capítulo
horas = [
    [120, 105, 107, 110],  # Bibiana: Cap 14, 15, 16, 17
    [116, 109, 107, 110],  # Dayana: Cap 14, 15, 16, 17
    [115, 120, 113, 111],  # Mario: Cap 14, 15, 16, 17
    [122, 109, 118, 115]   # Juan: Cap 14, 15, 16, 17
]

nombres_traductores = ['Bibiana', 'Dayana', 'Mario', 'Juan']
nombres_capitulos = ['Capítulo 14', 'Capítulo 15', 'Capítulo 16', 'Capítulo 17']

print("Matriz de horas de trabajo:")
print("         Cap 14  Cap 15  Cap 16  Cap 17")
for i, nombre in enumerate(nombres_traductores):
    print(f"{nombre:8} : {horas[i][0]:6} {horas[i][1]:6} {horas[i][2]:6} {horas[i][3]:6}")

print("\nANÁLISIS DEL PROBLEMA:")
print("- 4 traductores disponibles")
print("- 4 capítulos para traducir")
print("- Capítulo 14 necesita AL MENOS 2 traductores")
print("- Cada traductor puede trabajar en máximo 1 capítulo")
print("- TODOS los capítulos deben tener traductor asignado")
print("- Como Cap 14 necesita 2+ traductores, mínimo necesitamos 5 traductores")
print("- Pero solo tenemos 4, entonces es IMPOSIBLE satisfacer todos los requisitos")
print("- La pregunta es: ¿cuál capítulo tendrá DÉFICIT de traductores?")

# Definir índices
traductores = range(4)  # 4 traductores
capitulos = range(4)    # 4 capítulos

# Definir índices
traductores = range(4)  # 4 traductores
capitulos = range(4)    # 4 capítulos

print("\nENFOQUE CORRECTO: Análisis de déficit")
print("El problema pregunta qué capítulo tendrá déficit de traductores.")
print("Esto significa que intentaremos asignar de la mejor manera posible,")
print("pero como Cap 14 necesita AL MENOS 2 y solo tenemos 4 traductores,")
print("necesariamente algún capítulo no tendrá la cantidad ideal.")
print()

# Crear modelo de optimización principal
prob = pulp.LpProblem("Asignacion_Traductores", pulp.LpMinimize)

# Variables de decisión: x[i,j] = 1 si traductor i se asigna a capítulo j
x = {}
for i in traductores:
    for j in capitulos:
        x[i, j] = pulp.LpVariable(f"x_{i}_{j}", cat='Binary')

# Función objetivo: minimizar horas totales
prob += pulp.lpSum(horas[i][j] * x[i, j] for i in traductores for j in capitulos)

# Restricciones
# 1. Cada traductor se asigna a máximo un capítulo
for i in traductores:
    prob += pulp.lpSum(x[i, j] for j in capitulos) <= 1

# 2. Capítulo 14 (índice 0) debe tener AL MENOS 2 traductores
prob += pulp.lpSum(x[i, 0] for i in traductores) >= 2

# 3. Los otros capítulos deben tener AL MENOS 1 traductor
for j in [1, 2, 3]:  # Capítulos 15, 16, 17
    prob += pulp.lpSum(x[i, j] for i in traductores) >= 1

# Resolver el problema
print("Resolviendo el modelo de optimización...")
prob.solve()

if prob.status == pulp.LpStatusOptimal:
    print(f"Solución óptima encontrada!")
    print(f"Costo total: {pulp.value(prob.objective)} horas")
    
    print("\nAsignación óptima:")
    asignaciones = {}
    for j in capitulos:
        asignaciones[j] = []
        for i in traductores:
            if x[i, j].varValue == 1:
                asignaciones[j].append(i)
        
        if asignaciones[j]:
            nombres_asig = [nombres_traductores[i] for i in asignaciones[j]]
            horas_cap = sum(horas[i][j] for i in asignaciones[j])
            print(f"  {nombres_capitulos[j]}: {', '.join(nombres_asig)} ({horas_cap} h)")
        else:
            print(f"  {nombres_capitulos[j]}: SIN TRADUCTOR")
    
    # Identificar déficits
    print("\nAnálisis de déficits:")
    deficit_encontrado = False
    for j in capitulos:
        num_traductores = len(asignaciones[j])
        if j == 0:  # Capítulo 14
            if num_traductores < 2:
                print(f"  {nombres_capitulos[j]}: DÉFICIT (tiene {num_traductores}, necesita 2+)")
                deficit_encontrado = True
            else:
                print(f"  {nombres_capitulos[j]}: OK (tiene {num_traductores})")
        else:  # Otros capítulos
            if num_traductores == 0:
                print(f"  {nombres_capitulos[j]}: DÉFICIT (sin traductor)")
                deficit_encontrado = True
            else:
                print(f"  {nombres_capitulos[j]}: OK (tiene {num_traductores})")
    
    if not deficit_encontrado:
        print("  No hay déficits aparentes en la solución óptima")

else:
    print("No se encontró solución factible")
    print("Esto confirma que es imposible satisfacer todos los requisitos")
    
print("\n" + "="*60)

# Análisis alternativo: Evaluar diferentes interpretaciones
print("ANÁLISIS ALTERNATIVO:")
print("Como el problema es imposible de resolver perfectamente,")
print("evaluemos qué capítulo es mejor dejar con déficit")
print()

# Probar relajando cada capítulo uno por uno
print("Escenarios donde cada capítulo tiene déficit:")
for cap_deficit in range(4):
    print(f"\n--- Escenario: {nombres_capitulos[cap_deficit]} con déficit ---")
    
    prob_alt = pulp.LpProblem(f"Deficit_Cap_{cap_deficit}", pulp.LpMinimize)
    
    # Variables
    y = {}
    for i in traductores:
        for j in capitulos:
            y[i, j] = pulp.LpVariable(f"y_{i}_{j}", cat='Binary')
    
    # Función objetivo
    prob_alt += pulp.lpSum(horas[i][j] * y[i, j] for i in traductores for j in capitulos)
    
    # Restricciones básicas
    for i in traductores:
        prob_alt += pulp.lpSum(y[i, j] for j in capitulos) <= 1
    
    # Restricciones específicas según el escenario
    for j in capitulos:
        if j == cap_deficit:
            # El capítulo con déficit puede tener menos traductores
            if j == 0:  # Si es capítulo 14
                # Debe tener al menos 1 (déficit respecto a los 2 requeridos)
                prob_alt += pulp.lpSum(y[i, j] for i in traductores) >= 1
            # Para otros capítulos, pueden quedar sin traductor (déficit total)
        else:
            # Los otros capítulos deben satisfacer sus requisitos
            if j == 0:  # Capítulo 14
                prob_alt += pulp.lpSum(y[i, j] for i in traductores) >= 2
            else:  # Otros capítulos
                prob_alt += pulp.lpSum(y[i, j] for i in traductores) >= 1
    
    # Resolver
    prob_alt.solve()
    
    if prob_alt.status == pulp.LpStatusOptimal:
        costo = pulp.value(prob_alt.objective)
        print(f"  Costo si {nombres_capitulos[cap_deficit]} tiene déficit: {costo} horas")
        
        # Mostrar asignación
        for j in capitulos:
            asignados = []
            for i in traductores:
                if y[i, j].varValue == 1:
                    asignados.append(i)
            
            if asignados:
                nombres_asig = [nombres_traductores[i] for i in asignados]
                horas_cap = sum(horas[i][j] for i in asignados)
                print(f"    {nombres_capitulos[j]}: {', '.join(nombres_asig)} ({horas_cap} h)")
            else:
                print(f"    {nombres_capitulos[j]}: SIN TRADUCTOR")
    else:
        print(f"  No factible dejar {nombres_capitulos[cap_deficit]} con déficit")

print(f"\n*** ANÁLISIS DE RESULTADOS ***")
print("Costos según qué capítulo tenga déficit:")
print("1. Capítulo 14 con déficit (1 traductor en vez de 2+): 441 horas")
print("2. Capítulo 15 con déficit (0 traductores): 453 horas") 
print("3. Capítulo 16 con déficit (0 traductores): 450 horas")
print("4. Capítulo 17 con déficit (0 traductores): 447 horas")
print()
print("INTERPRETACIÓN CORRECTA:")
print("El problema busca que todos los capítulos tengan traductor,")
print("pero como es imposible satisfacer completamente los requisitos,")
print("la pregunta es sobre qué capítulo tendrá DÉFICIT.")
print()
print("'Déficit' significa no tener la cantidad REQUERIDA:")
print("- Capítulo 14 REQUIERE al menos 2 traductores")
print("- Los otros capítulos requieren 1 traductor cada uno")
print()
print("El Capítulo 14 es el único que puede tener déficit real")
print("(recibir menos de lo requerido) mientras todos los capítulos")
print("mantienen al menos un traductor asignado.")
print()
print("Solución óptima con déficit en Cap 14:")
print("- Capítulo 14: Mario (115 h) - DÉFICIT: tiene 1, necesita 2+")
print("- Capítulo 15: Juan (109 h) - OK")
print("- Capítulo 16: Bibiana (107 h) - OK") 
print("- Capítulo 17: Dayana (110 h) - OK")
print("- Costo total: 441 horas")
print()
print("*** RESPUESTA FINAL: Capítulo 14 tendrá déficit de traductores ***")
print("(Recibirá solo 1 traductor cuando necesita al menos 2)")
