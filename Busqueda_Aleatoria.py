import matplotlib.pyplot as plt
import base as b
import statistics

real_pc = [26, 26, 25, 24, 23, 24, 25, 27, 30, 29, 34, 32, 31, 31, 25, 24, 25, 26, 34, 36, 39, 40, 38, 29]
real_pv = [24, 23, 22, 23, 22, 22, 20, 20, 20, 19, 19, 20, 19, 20, 22, 23, 22, 23, 26, 28, 34, 35, 34, 24]
real_r = [0, 0, 0, 0, 0, 0, 0, 0, 100, 313, 500, 661, 786, 419, 865, 230, 239, 715, 634, 468, 285, 96, 0, 0]

random_pc = [7, 7, 50, 25, 11, 26, 48, 45, 10, 14, 42, 14, 42, 22, 40, 34, 21, 31, 29, 34, 11, 37, 8, 50]
random_pv = [1, 3, 21, 1, 10, 7, 44, 35, 4, 1, 23, 12, 30, 7, 30, 4, 9, 10, 6, 9, 8, 27, 7, 10]
random_r = [274, 345, 605, 810, 252, 56, 964, 98, 77, 816, 68, 261, 841, 897, 75, 489, 833, 96, 117, 956, 970, 255, 74,
            926]

extension = 1000
capacidad_bateria = 300
rendimiento = 0.2

semillas = [123456, 678901, 9876538, 4920083, 763682]

num_iteraciones = 100

horas = range(0, 24)


# Búsqueda aleatoria
def busqueda_aleatoria(pv, pc, r):
    resultados = []
    BeneficiosTotales = []
    EvaluacionesTotales = []
    for i in range(len(semillas)):
        solucion_inicial = b.generar_solucion_inicial(semillas[i])
        solucion_actual = solucion_inicial
        mejor_solucion = solucion_actual
        evaluaciones = 0
        for j in range(num_iteraciones):
            solucion_actual = b.generar_solucion_aleatoria()
            beneficio, lista_bat, lista_ben = b.funcion_evaluacion(solucion_actual, r, pv, pc)
            beneficio2, lista_bat2, lista_ben2 = b.funcion_evaluacion(mejor_solucion, r, pv, pc)
            evaluaciones += 2
            # Si el beneficio de la solucion generada aleatoriamente es mejor que el
            # de la mejor solucion, la mejor solucion pasa a ser esa aleatoria
            if beneficio > beneficio2:
                mejor_solucion = solucion_actual
        resultados.append(mejor_solucion)
        EvaluacionesTotales.append(evaluaciones)

    for i in range(len(resultados)):
        print(f"Solucion {i}: ", resultados[i])
        beneficio, lista_bat, lista_ben = b.funcion_evaluacion(resultados[i], r, pv, pc)
        BeneficiosTotales.append(beneficio)

        print("El beneficio ha sido de ", beneficio, " €")
        fig, axes = plt.subplots()
        axes.plot(horas, lista_ben, "k", label="Beneficio")
        axes.set_xlabel("Horas")
        axes.set_ylabel("Beneficio(€)")
        axes.legend()

        twin_axes = axes.twinx()
        twin_axes.plot(horas, lista_bat, "r", label="Bateria")
        twin_axes.set_ylabel("Batería(kWh)")
        twin_axes.legend()

        axes.set_ylim([-100, max(max(lista_ben), max(lista_bat))])
        twin_axes.set_ylim([-100, max(max(lista_ben), max(lista_bat))])
        plt.title(f"Búsqueda Aleatoria: Semilla {semillas[i]}")
        plt.xticks(range(0, 24, 1))
        plt.show()

    print()
    print("EVMEDIAS: ", statistics.mean(EvaluacionesTotales))
    print("EVMEJOR: ", min(EvaluacionesTotales))
    print("EVDESV: ", round(statistics.stdev(EvaluacionesTotales), 2))
    print("MEDIA: ", round(statistics.mean(BeneficiosTotales), 2))
    print("DESVIACIÓN TÍPICA: ", round(statistics.stdev(BeneficiosTotales), 2))
    print("MEJOR RESULTADO: ", max(BeneficiosTotales))
    print()


