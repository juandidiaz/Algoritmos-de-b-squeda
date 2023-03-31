import copy

import matplotlib.pyplot as plt
import base as b
import statistics
import numpy as np

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

num_iteraciones_max = 200
max_vecinos = 40
horas = range(0, 24)

valoresColumnas = list((range(-100, 101, 10)))


def tabu(pv, pc, r):
    BeneficiosTotales = []
    EvaluacionesTotales = []
    for i in range(len(semillas)):
        iteraciones = 0
        tenencia = 4
        solucion_inicial = b.generar_solucion_inicial(semillas[i])
        solucion_actual = copy.copy(solucion_inicial)
        mejor_solucion = copy.copy(solucion_actual)
        mejor_vecino = solucion_actual
        lista_tabu = [None] * tenencia
        posicion = 0
        MLP = np.ones([23, 21])
        evaluaciones = 0
        while iteraciones < num_iteraciones_max:
            vecinos_generados = 0
            beneficioActual, lista_batActual, lista_benActual = b.funcion_evaluacion(solucion_actual, r, pv, pc)
            evaluaciones += 1
            while vecinos_generados < max_vecinos:
                vecino, pos, valor = b.generar_vecino_aleatorio_tabu(solucion_actual)
                vecinos_generados += 1
                beneficioMejorVecino, lista_batMejVecino, lista_benMejVecino = b.funcion_evaluacion(mejor_vecino, r, pv,
                                                                                                    pc)
                beneficioVecino, lista_batVecino, lista_benVecino = b.funcion_evaluacion(vecino, r, pv, pc)
                evaluaciones += 2
                if beneficioVecino > beneficioMejorVecino:
                    mejor_vecino = vecino
                    tupla = (pos, valor)
                    beneficioMejorVecino, lista_batMejVecino, lista_benMejVecino = b.funcion_evaluacion(mejor_vecino, r,
                                                                                                        pv,
                                                                                                        pc)
                    evaluaciones+=1
            if not (esta_en_tabu(lista_tabu, tupla)) or beneficioMejorVecino > beneficioActual:
                actualizar_lista_tabu(lista_tabu, tupla, posicion, tenencia)
                posicion += 1
                solucion_actual = mejor_vecino
                mejor_solucion = solucion_actual
                actualizar_memoria_largo_plazo(MLP, tupla)
            iteraciones += 1

            if iteraciones % (int(num_iteraciones_max / 4)) == 0:
                n = np.random.rand(1)

                if n < 0.25:
                    solucion_actual = b.generar_solucion_aleatoria()
                elif n < 0.75:
                    solucion_actual = greedy(MLP)
                else:
                    solucion_actual = mejor_vecino

                lista_tabu = [None] * tenencia
                dado = np.random.uniform(0, 1)
                if dado <= 0.5:
                    tenencia = (int(tenencia / 2))
                    lista_tabu = [None] * tenencia
                else:
                    tenencia *= 2
                    lista_tabu = [None] * tenencia

            beneficioMejor, lista_batMejor, lista_benMejor = b.funcion_evaluacion(mejor_vecino, r, pv, pc)
            beneficioActual, lista_batActual, lista_benActual = b.funcion_evaluacion(solucion_actual, r, pv, pc)
            evaluaciones += 2

            if beneficioActual > beneficioMejor:
                mejor_solucion = solucion_actual

        EvaluacionesTotales.append(evaluaciones)
        print(f"Solucion {i}: ", mejor_solucion)
        beneficio, lista_bat, lista_ben = b.funcion_evaluacion(mejor_solucion, r, pv, pc)
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
        plt.title(f"Tabú: Semilla {semillas[i]}")

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


def esta_en_tabu(lista_tabu, tupla):
    if tupla in lista_tabu:
        return True
    else:
        return False


def actualizar_lista_tabu(lista_tabu, movimiento, pos, tenencia):
    if pos < tenencia:
        lista_tabu[pos] = movimiento
    else:
        posicion = pos % tenencia
        lista_tabu[posicion] = movimiento


def actualizar_memoria_largo_plazo(memoria, movimiento):
    columna = valoresColumnas.index(movimiento[1])
    memoria[movimiento[0]][columna] += 1


def greedy(memoria):
    solucionGreedy = []
    matrizProbabilidades = np.copy(memoria)

    matrizInversa = np.reciprocal(matrizProbabilidades)
    matrizProbabilidadesNormal = np.divide(matrizInversa, np.sum(matrizInversa, axis=1, keepdims=True))

    for i in range(len(matrizProbabilidadesNormal)):
        numRandom = np.random.uniform(0, 1)
        suma = 0
        for j in range(len(valoresColumnas)):
            suma += matrizProbabilidadesNormal[i][j]
            if numRandom < suma:
                solucionGreedy.append(valoresColumnas[j])
                break
    return solucionGreedy

tabu(real_pv,real_pc,real_r)