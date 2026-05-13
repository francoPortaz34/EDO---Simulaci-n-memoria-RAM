import numpy as np
import matplotlib.pyplot as plt
from math import log

print(" MODELO DE USO DE MEMORIA RAM ")
print(" ECUACIÓN DIFERENCIAL: dM/dt = a - bM")

def mostrar_encabezado_resultados(a, b):
    print("\nRESULTADOS")

    print("\nEcuación diferencial:")
    print(f"dM/dt = {a} - {b}M")

    print("\nSolución general:")
    print("M(t) = a/b + Ce^(-bt)")

def mostrar_solucion_particular(a, b, C):
    print("\nSolución particular:")

    if C >= 0:
        print(f"M(t) = {a/b:.4f} + {C:.4f}e^(-{b}t)")
    else:
        print(f"M(t) = {a/b:.4f} - {abs(C):.4f}e^(-{b}t)")

# INGRESO DE PARÁMETROS

a = float(input("\nIngrese el valor de a: "))
b = float(input("Ingrese el valor de b: "))

print("\nSeleccione el tipo de condición:")

print("1) Condición inicial M(0)")
print("2) Valor conocido en otro instante M(t1)")
print("3) Buscar tiempo para alcanzar cierta memoria")

opcion = input("\nOpción: ")

# CASO 1 -> M(0)

if opcion == "1":
    M0 = float(input("\nIngrese M(0): "))

    C = M0 - a/b

    # Solución particular
    def M(t):
        return a/b + C*np.exp(-b*t)

    # Tiempo a evaluar
    t_eval = float(input("Ingrese el tiempo a evaluar: "))

    resultado = M(t_eval)

    mostrar_encabezado_resultados(a, b)

    print("\nConstante C:")
    print(f"C = {C:.4f}")

    mostrar_solucion_particular(a, b, C)

    print(f"\nM({t_eval}) = {resultado:.4f}")

# CASO 2 -> M(t1)

elif opcion == "2":
    t1 = float(input("\nIngrese el tiempo conocido t1: "))
    M1 = float(input(f"Ingrese M({t1}): "))

    C = (M1 - a/b)/np.exp(-b*t1)

    def M(t):
        return a/b + C*np.exp(-b*t)

    t_eval = float(input("Ingrese el tiempo a evaluar: "))

    resultado = M(t_eval)

    mostrar_encabezado_resultados(a, b)

    print("\nConstante C:")
    print(f"C = {C:.4f}")

    mostrar_solucion_particular(a, b, C)

    print(f"\nM({t_eval}) = {resultado:.4f}")

# CASO 3 -> BUSCAR TIEMPO

elif opcion == "3":
    M0 = float(input("\nIngrese M(0): "))

    C = M0 - a/b

    def M(t):
        return a/b + C*np.exp(-b*t)

    memoria_objetivo = float(
        input("Ingrese la memoria que desea alcanzar: ")
    )

    # Despeje de t
    try:
        t_obj = (-1/b) * log(
            (memoria_objetivo - a/b)/C
        )
        mostrar_encabezado_resultados(a, b)

        print("\nConstante C:")
        print(f"C = {C:.4f}")

        mostrar_solucion_particular(a, b, C)

        print(
            f"\nTiempo necesario para alcanzar "
            f"{memoria_objetivo} GB:"
        )

        print(f"t = {t_obj:.4f}")

    except:
        print("\nNo es posible alcanzar ese valor de memoria.")

else:
    print("\nOpción inválida.")
    exit()

# GRÁFICA

t = np.linspace(0, 20, 500)

memoria = M(t)

plt.figure(figsize=(9,5))
plt.plot(t, memoria, label="Uso de RAM")
# Línea de equilibrio
plt.axhline(
    a/b,
    linestyle="--",
    label=f"Equilibrio = {a/b:.2f}"
)
# Punto evaluado
if opcion in ["1", "2"]:
    plt.scatter(
        t_eval,
        resultado,
        color="red",
        label=f"M({t_eval})"
    )
    plt.annotate(
        f"M({t_eval}) = {resultado:.2f}",
        (t_eval, resultado),
        textcoords="offset points",
        xytext=(10, -20),
        ha='left'
    )

# Punto objetivo
if opcion == "3":
    plt.scatter(
        t_obj,
        memoria_objetivo,
        color="green",
        label="Objetivo"
    )
    plt.annotate(
        f"t = {t_obj:.2f}",
        (t_obj, memoria_objetivo),
        textcoords="offset points",
        xytext=(10, -20),
        ha='left'
    )
plt.xlabel("Tiempo")
plt.ylabel("Memoria RAM")
plt.title("Modelo de uso de memoria RAM")

plt.grid(True)
plt.legend()

plt.show()