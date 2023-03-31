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

kMaxima = 6


def busqueda_local_mejorK(solucion_actual, pv, pc, r, k,granularidad):
    iteraciones = 0
    while (iteraciones < 3000):  # Fijar numero de iteraciones
        mejor_vecino = solucion_actual
        beneficioMejor, lista_batMejor, lista_benMejor = b.funcion_evaluacion(mejor_vecino, r, pv, pc)
        pos = 0
        sumar = True
        for j in range(48):
            vecino = b.generar_vecinosk(solucion_actual,pos, sumar, k,granularidad)
            pos += 1
            if (pos == 23):
                pos = 0
                sumar = False
            beneficioPrimo, lista_batPrimo, lista_benPrimo = b.funcion_evaluacion(vecino, r, pv, pc)
            if beneficioPrimo > beneficioMejor:
                mejor_vecino = vecino
                beneficioMejor, lista_batMejor, lista_benMejor = b.funcion_evaluacion(mejor_vecino, r, pv, pc)
        beneficioActual, lista_batActual, lista_benActual = b.funcion_evaluacion(solucion_actual, r, pv, pc)
        iteraciones += 1
        # Si el beneficio del mejor vecino es mejor que el de la solucion actual,
        # la solucion actual pasa a ser ese vecino
        if beneficioMejor > beneficioActual:
            solucion_actual = mejor_vecino
        # Si el beneficio del mejor vecino es peor que el de la actual, salgo del while
        if beneficioMejor <= beneficioActual:
            break
    return solucion_actual


def VND(pv, pc, r,granularidad):
    EvaluacionesTotales = []
    BeneficiosTotales = []
    for i in range(len(semillas)):
        evaluaciones = 0
        k = 1
        solucion_actual = b.generar_solucion_inicial(semillas[i])
        beneficioActual, lista_batActual, lista_benActual = b.funcion_evaluacion(solucion_actual, r, pv, pc)
        evaluaciones += 1
        while k < kMaxima:
            solucionLocal = busqueda_local_mejorK(solucion_actual, pv, pc, r, k,granularidad)
            beneficioLocal, lista_batLocal, lista_benLocal = b.funcion_evaluacion(solucionLocal, r, pv, pc)
            evaluaciones += 1
            if beneficioLocal > beneficioActual:
                solucion_actual = solucionLocal
                beneficioActual, lista_batActual, lista_benActual = b.funcion_evaluacion(solucion_actual, r, pv, pc)
                evaluaciones += 1
            else:
                k += 1
        EvaluacionesTotales.append(evaluaciones)
        print(f"Solucion {i}:", solucion_actual)
        beneficioActual, lista_batActual, lista_benActual = b.funcion_evaluacion(solucion_actual, r, pv, pc)
        BeneficiosTotales.append(beneficioActual)

        print("El beneficio es de ", beneficioActual)
        fig, axes = plt.subplots()
        axes.plot(horas, lista_benActual, "k", label="Beneficio")
        axes.set_xlabel("Horas")
        axes.set_ylabel("Beneficio(€)")
        axes.legend()

        twin_axes = axes.twinx()
        twin_axes.plot(horas, lista_batActual, "r", label="Bateria")
        twin_axes.set_ylabel("Batería(kWh)")
        twin_axes.legend()

        axes.set_ylim([-100, max(max(lista_benActual), max(lista_batActual))])
        twin_axes.set_ylim([-100, max(max(lista_benActual), max(lista_batActual))])
        plt.title(f"VND: Semilla {semillas[i]} y granularidad {granularidad}")

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



