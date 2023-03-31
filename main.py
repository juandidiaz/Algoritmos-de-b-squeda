import greedy as g
import BLMejor as BL
import BLPrimer as BP
import Enfriamiento as E
import Tabu as T
import VND as V
import Busqueda_Aleatoria as BA
import matplotlib.pyplot as plt

real_pc = [26, 26, 25, 24, 23, 24, 25, 27, 30, 29, 34, 32, 31, 31, 25, 24, 25, 26, 34, 36, 39, 40, 38, 29]
real_pv = [24, 23, 22, 23, 22, 22, 20, 20, 20, 19, 19, 20, 19, 20, 22, 23, 22, 23, 26, 28, 34, 35, 34, 24]
real_r = [0, 0, 0, 0, 0, 0, 0, 0, 100, 313, 500, 661, 786, 419, 865, 230, 239, 715, 634, 468, 285, 96, 0, 0]

random_pc = [7, 7, 50, 25, 11, 26, 48, 45, 10, 14, 42, 14, 42, 22, 40, 34, 21, 31, 29, 34, 11, 37, 8, 50]
random_pv = [1, 3, 21, 1, 10, 7, 44, 35, 4, 1, 23, 12, 30, 7, 30, 4, 9, 10, 6, 9, 8, 27, 7, 10]
random_r = [274, 345, 605, 810, 252, 56, 964, 98, 77, 816, 68, 261, 841, 897, 75, 489, 833, 96, 117, 956, 970, 255, 74,
            926]

mu = 0.07
phi = 0.06
granularidades=[1,5,8]
horas = range(0, 24)

print("DATOS REALES")
print("---------------------------------------")
print("GREEDY: ")
solucionReal, beneficio_real, lista_bateria_real, lista_beneficio_real, hora_venta_real = g.greedy_real()
print(f"Solucion{solucionReal}")
print(beneficio_real, "Euros")
fig, axes = plt.subplots()
axes.plot(horas, lista_beneficio_real, "k", label="Beneficio")
axes.set_xlabel("Horas")
axes.set_ylabel("Beneficio(€)")
axes.legend()

twin_axes = axes.twinx()
twin_axes.plot(horas, lista_bateria_real, "r", label="Bateria")
twin_axes.set_ylabel("Batería(kWh)")
twin_axes.legend()

axes.set_ylim([-100, max(max(lista_beneficio_real), max(lista_bateria_real))])
twin_axes.set_ylim([-100, max(max(lista_beneficio_real), max(lista_bateria_real))])
plt.xticks(range(0, 24, 1))
plt.title("Greedy con datos reales")
plt.show()
print()
print("Búsqueda Aleatoria: ")
BA.busqueda_aleatoria(real_pv, real_pc, real_r)
print()
for gran in granularidades:
    print("Búsqueda Local Mejor: ")
    BL.busqueda_local_mejor(real_pv, real_pc, real_r,gran)
    print()
    print("Búsqueda Local Primer Mejor: ")
    BP.busqueda_local_primer_mejor(real_pv, real_pc, real_r,gran)
    print()
    print("Búsqueda Enfriamiento Simulado: ")
    E.enfriamientoSimulado(real_pv, real_pc, real_r, mu, phi, beneficio_real,gran)
    print()
    print("Búsqueda VND: ")
    V.VND(real_pv, real_pc, real_r,gran)
    print()
print("Búsqueda Tabú:")
T.tabu(real_pv, real_pc, real_r)
print()

print("DATOS ALEATORIOS")
print("---------------------------------------")
print("GREEDY: ")
solucionAleatoria, beneficio_Aleatorio, lista_bateria_Aleatoria, lista_beneficio_Aleatoria, hora_venta_Aleatoria = g.greedy_aleatorio()
print(f"Solucion{solucionAleatoria}")
print(beneficio_Aleatorio, "Euros")
fig, axes = plt.subplots()
axes.plot(horas, lista_beneficio_Aleatoria, "k", label="Beneficio")
axes.set_xlabel("Horas")
axes.set_ylabel("Beneficio(€)")
axes.legend()

twin_axes = axes.twinx()
twin_axes.plot(horas, lista_bateria_Aleatoria, "r", label="Bateria")
twin_axes.set_ylabel("Batería(kWh)")
twin_axes.legend()

axes.set_ylim([-100, max(max(lista_beneficio_Aleatoria), max(lista_bateria_Aleatoria))])
twin_axes.set_ylim([-100, max(max(lista_beneficio_Aleatoria), max(lista_bateria_Aleatoria))])
plt.xticks(range(0, 24, 1))
plt.title("Greedy con datos aleatorios")
plt.show()
print()
print("Búsqueda Aleatoria: ")
BA.busqueda_aleatoria(random_pv, random_pc, random_r)
print()
for gran in granularidades:
    print("Búsqueda Local Mejor: ")
    BL.busqueda_local_mejor(random_pv, random_pc, random_r,gran)
    print()
    print("Búsqueda Local Primer Mejor: ")
    BP.busqueda_local_primer_mejor(random_pv, random_pc, random_r,gran)
    print()
    print("Búsqueda Enfriamiento Simulado: ")
    E.enfriamientoSimulado(random_pv, random_pc, random_r, mu, phi, beneficio_Aleatorio,gran)
    print()
    print("Búsqueda VND: ")
    V.VND(random_pv, random_pc, random_r,gran)
    print()

print("Búsqueda Tabú:")
T.tabu(random_pv, random_pc, random_r)
