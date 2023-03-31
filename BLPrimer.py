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

horas = range(0, 24)


# Busqueda Local Mejor
def busqueda_local_primer_mejor(pv, pc, r,granularidad):
    BeneficiosTotales = []
    EvaluacionesTotales = []
    for i in range(len(semillas)):
        evaluaciones = 0
        solucion_actual = b.generar_solucion_inicial(semillas[i])
        mejor_vecino = solucion_actual
        iteraciones = 0

        while (iteraciones < 7000):  # Fijar numero de iteraciones
            beneficioVecino = 0
            beneficioMejor = 0
            pos = 0
            numVecinos = 0
            intentosSinMejora = 0
            sumar_restar = True
            contador = 0
            while (beneficioVecino <= beneficioMejor and numVecinos < 48 and intentosSinMejora < 28):
                vecino = b.generar_vecino(solucion_actual, pos, sumar_restar,granularidad)
                numVecinos += 1
                pos += 1
                pos %= len(solucion_actual)
                if (pos == 0 and contador == 0):
                    sumar_restar = False
                    contador += 1
                elif (pos == 0 and contador == 1):
                    sumar_restar = True
                    contador = 0
                beneficioMejor, lista_batMejor, lista_benMejor = b.funcion_evaluacion(mejor_vecino, r, pv, pc)
                beneficioVecino, lista_batVecino, lista_benVecino = b.funcion_evaluacion(vecino, r, pv, pc)
                evaluaciones += 2

                if (beneficioVecino > beneficioMejor):
                    mejor_vecino = vecino
                    break
                else:
                    intentosSinMejora += 1

            beneficioActual, lista_batActual, lista_benActual = b.funcion_evaluacion(solucion_actual, r, pv, pc)
            beneficioMejor, lista_batMejor, lista_benMejor = b.funcion_evaluacion(mejor_vecino, r, pv, pc)
            evaluaciones += 2
            iteraciones += 1
            if beneficioMejor > beneficioActual:
                solucion_actual = mejor_vecino
            if beneficioMejor <= beneficioActual:
                break

        EvaluacionesTotales.append(evaluaciones)

        print(f"Solucion {i}: ", solucion_actual)
        beneficio, lista_bat, lista_ben = b.funcion_evaluacion(solucion_actual, r, pv, pc)
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
        plt.title(f"Búsqueda Local Primer Mejor: Semilla {semillas[i]} y granularidad {granularidad}")

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






