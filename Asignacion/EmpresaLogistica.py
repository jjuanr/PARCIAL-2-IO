import pulp
from itertools import combinations, permutations

# Problema: Asignación de transportistas a ciudades en dos días
# 4 transportistas, 3 ciudades, 2 días (lunes y jueves)
# Restricciones:
# - Cada transportista puede asignarse a una única ciudad por día
# - Cada ciudad debe ser atendida por algún transportista cada día (3 asignaciones por día)
# - TODOS los transportistas deben ser asignados AMBOS días (nueva restricción)
# Objetivo: minimizar el costo total

# Definir los costos por transportista, ciudad y día
# Índices: [día][transportista][ciudad]
# Día 0 = Lunes, Día 1 = Jueves
# Transportistas: 0, 1, 2, 3 (Transportista 1, 2, 3, 4)
# Ciudades: 0, 1, 2 (Bogotá, Medellín, Cali)

costos = [
    # Día lunes (índice 0)
    [
        [5, 3, 7],   # Transportista 1
        [7, 9, 5],   # Transportista 2
        [6, 7, 2],   # Transportista 3
        [2, 12, 6]   # Transportista 4
    ],
    # Día jueves (índice 1)
    [
        [2, 7, 10],  # Transportista 1
        [8, 5, 7],   # Transportista 2
        [9, 6, 8],   # Transportista 3
        [6, 8, 6]    # Transportista 4
    ]
]

nombres_transportistas = ["Transportista 1", "Transportista 2", "Transportista 3", "Transportista 4"]
nombres_ciudades = ["Bogotá", "Medellín", "Cali"]
nombres_dias = ["Lunes", "Jueves"]

print("Matrices de costos:")
for d, dia in enumerate(nombres_dias):
    print(f"\n{dia}:")
    print("               Bogotá  Medellín  Cali")
    for t, transportista in enumerate(nombres_transportistas):
        print(f"{transportista:15}: {costos[d][t][0]:5} {costos[d][t][1]:8} {costos[d][t][2]:5}")

print()

# INTERPRETACIÓN CORRECTA DEL PROBLEMA:
# Todos los transportistas deben trabajar AMBOS días
# Cada ciudad debe ser atendida por al menos un transportista cada día
# Esto significa que algunas ciudades pueden tener múltiples transportistas

print("ANÁLISIS DEL PROBLEMA:")
print("- 4 transportistas deben trabajar AMBOS días")
print("- 3 ciudades deben ser atendidas cada día")
print("- Cada ciudad debe tener al menos un transportista por día")
print("- Esto significa que algunas ciudades tendrán múltiples transportistas")
print()

# Crear el problema de minimización usando PuLP
prob = pulp.LpProblem("Logistica_Imbarco", pulp.LpMinimize)

# Definir las variables de decisión
# x[d][t][c] = 1 si el transportista t es asignado a la ciudad c en el día d, 0 en caso contrario
dias = range(2)           # 2 días
transportistas = range(4) # 4 transportistas  
ciudades = range(3)       # 3 ciudades

x = {}
for d in dias:
    for t in transportistas:
        for c in ciudades:
            x[d, t, c] = pulp.LpVariable(f"x_{d}_{t}_{c}", cat='Binary')

# Función objetivo: minimizar el costo total
prob += pulp.lpSum(costos[d][t][c] * x[d, t, c] for d in dias for t in transportistas for c in ciudades)

# Restricciones:
# 1. Cada transportista debe ser asignado a exactamente una ciudad por día
for d in dias:
    for t in transportistas:
        prob += pulp.lpSum(x[d, t, c] for c in ciudades) == 1

# 2. Cada ciudad debe ser atendida por al menos un transportista cada día
for d in dias:
    for c in ciudades:
        prob += pulp.lpSum(x[d, t, c] for t in transportistas) >= 1

# Resolver el problema
print("Resolviendo el problema de optimización...")
prob.solve()

# Mostrar el estado de la solución
print("Estado de la solución:", pulp.LpStatus[prob.status])

if prob.status == pulp.LpStatusOptimal:
    # Mostrar la asignación óptima
    print("\nAsignación óptima:")
    costo_total = 0
    
    for d in dias:
        print(f"\n{nombres_dias[d]}:")
        for t in transportistas:
            for c in ciudades:
                if x[d, t, c].varValue == 1:
                    print(f"  {nombres_transportistas[t]} -> {nombres_ciudades[c]}, Costo: {costos[d][t][c]}")
                    costo_total += costos[d][t][c]
    
    print(f"\nCosto total mínimo: {costo_total}")
    
    # Verificar cobertura de ciudades
    print("\nCobertura de ciudades:")
    for d in dias:
        print(f"\n{nombres_dias[d]}:")
        for c in ciudades:
            transportistas_asignados = []
            for t in transportistas:
                if x[d, t, c].varValue == 1:
                    transportistas_asignados.append(nombres_transportistas[t])
            print(f"  {nombres_ciudades[c]}: {', '.join(transportistas_asignados) if transportistas_asignados else 'Ninguno'}")
    
    # Verificar que todos los transportistas trabajen ambos días
    print("\nVerificación - Todos los transportistas deben trabajar ambos días:")
    todos_trabajan_ambos = True
    for t in transportistas:
        dias_trabajados = 0
        trabajos = []
        for d in dias:
            trabajo_del_dia = False
            for c in ciudades:
                if x[d, t, c].varValue == 1:
                    trabajo_del_dia = True
                    trabajos.append(f"{nombres_dias[d]}({nombres_ciudades[c]})")
                    break
            if trabajo_del_dia:
                dias_trabajados += 1
        
        estado = "✅" if dias_trabajados == 2 else "❌"
        print(f"{nombres_transportistas[t]}: {dias_trabajados} día(s) {estado} - {', '.join(trabajos) if trabajos else 'No asignado'}")
        
        if dias_trabajados != 2:
            todos_trabajan_ambos = False
    
    if todos_trabajan_ambos:
        print("\n✅ Todos los transportistas trabajan ambos días")
    else:
        print("\n❌ No todos los transportistas trabajan ambos días")
    
    print(f"\n*** RESPUESTA: {costo_total} ***")

else:
    print("No se encontró una solución óptima")

# Verificación manual adicional
print(f"\n--- Verificación Manual ---")

# Calcular los costos mínimos posibles
print("Costos por transportista y día:")
for d, dia in enumerate(nombres_dias):
    print(f"\n{dia}:")
    for t, transportista in enumerate(nombres_transportistas):
        costos_transportista = costos[d][t]
        min_costo = min(costos_transportista)
        mejor_ciudad = nombres_ciudades[costos_transportista.index(min_costo)]
        print(f"  {transportista}: mejor opción {mejor_ciudad} (costo {min_costo})")

print(f"\nCálculo del costo mínimo teórico:")
print("Si cada transportista va a su mejor ciudad cada día:")

costo_teorico = 0
for d, dia in enumerate(nombres_dias):
    print(f"{dia}:")
    for t, transportista in enumerate(nombres_transportistas):
        mejor_costo = min(costos[d][t])
        costo_teorico += mejor_costo
        mejor_ciudad = nombres_ciudades[costos[d][t].index(mejor_costo)]
        print(f"  {transportista} -> {mejor_ciudad}: {mejor_costo}")

print(f"\nCosto teórico total: {costo_teorico}")
print("(Este sería el costo si no hubiera restricción de cobertura de ciudades)")
