import matplotlib.pyplot as plt
import base as b
import statistics
import greedy as g
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

# Se usa el esquema de Cauchy
# Tk=T0/(1+k)

# Se enfria cuando se haya generado un numero maximo de vecinos

# Se para cuando el algoritmo haga un numero maximo de iteraciones
# El numero de soluciones iniciales no aceptadas debe ser un 20%




mu = 0.07
phi = 0.06
solucionReal, beneficio_real, lista_bateria_real, lista_beneficio_real, hora_venta_real = g.greedy_real()
solucionAleatoria, beneficio_Aleatoria, lista_bateria_Aleatoria, lista_beneficio_Aleatoria, hora_venta_Aleatoria = g.greedy_aleatorio()
horas = range(0, 24)


def enfriamientoSimulado(pv, pc, r,mu,phi,beneficio,granularidad):
    BeneficiosTotales = []
    ListaRechazo = []
    Temperatura = []
    EvaluacionesTotales = []
    T0 = (mu / (-(np.log(phi)))) * beneficio
    LT = 15

    for i in range(len(semillas)):
        numIteraciones = 0
        T = T0
        solucion_actual = b.generar_solucion_inicial(semillas[i])
        mejor = solucion_actual
        aceptadas = 0
        rechazadas = 0
        evaluaciones = 0
        Temperatura.clear()
        while numIteraciones < 100:
            for j in range(LT):  # Velocidad de enfriamiento( max de vecinos)
                # Seleccionar una solucion candidata, en este caso sera aleatoria
                solucion_candidata = b.generar_vecino_aleatorio(solucion_actual,granularidad)
                beneficioCand, lista_batCand, lista_benCand = b.funcion_evaluacion(solucion_candidata, r, pv, pc)
                beneficioMejor, lista_batMej, lista_benMej = b.funcion_evaluacion(mejor, r, pv, pc)
                evaluaciones += 2
                # Calculamos la diferencia de beneficio entre la candidada y la actual
                delta = beneficioMejor - beneficioCand
                U = np.random.uniform(0, 1)
                E = np.exp(-delta / T)
                if U < E or delta < 0:
                    solucion_actual = solucion_candidata
                    aceptadas += 1
                    # Si el beneficio de la actual es mejor que el beneficio de la mejor visitada, la mejor
                    # visitada pasa a ser la actual
                    beneficioAct, lista_batAct, lista_benAct = b.funcion_evaluacion(solucion_actual, r, pv, pc)
                    evaluaciones += 1
                    if beneficioAct > beneficioMejor:
                        mejor = solucion_actual
                else:
                    rechazadas+=1

            T = T0 / (1 + numIteraciones)  # Mecanismo de enfriamiento (Cauchy)
            if (numIteraciones == 0):
                porcentaje = (rechazadas * 100) / (rechazadas + aceptadas)
                ListaRechazo.append(porcentaje)
            Temperatura.append(T)
            numIteraciones += 1

        beneficioMejor, lista_batMej, lista_benMej = b.funcion_evaluacion(mejor, r, pv, pc)
        BeneficiosTotales.append(beneficioMejor)
        EvaluacionesTotales.append(evaluaciones)
        print(f"Solucion {i}: ", mejor)
        print("El beneficio ha sido de ", beneficioMejor, "€")

        fig, axes = plt.subplots()
        axes.plot(horas, lista_benMej, "k", label="Beneficio")
        axes.set_xlabel("Horas")
        axes.set_ylabel("Beneficio(€)")
        axes.legend()

        twin_axes = axes.twinx()
        twin_axes.plot(horas, lista_batMej, "r", label="Bateria")
        twin_axes.set_ylabel("Batería(kWh)")
        twin_axes.legend()

        axes.set_ylim([-100, max(max(lista_benMej), max(lista_batMej))])
        twin_axes.set_ylim([-100, max(max(lista_benMej), max(lista_batMej))])
        plt.title(f"Enfriamiento Simulado: Semilla {semillas[i]} y granularidad {granularidad}")

        plt.xticks(range(0, 24, 1))
        plt.show()

    rango = range(numIteraciones)
    plt.title("TEMPERATURA")
    plt.xlabel("Número de iteraciones")
    plt.ylabel("Valor de la temperatura")
    plt.plot(rango, Temperatura)
    plt.show()

    print()
    print("EVMEDIAS: ", statistics.mean(EvaluacionesTotales))
    print("EVMEJOR: ", min(EvaluacionesTotales))
    print("EVDESV: ", round(statistics.stdev(EvaluacionesTotales), 2))
    print("MEDIA: ", round(statistics.mean(BeneficiosTotales), 2))
    print("DESVIACIÓN TÍPICA: ", round(statistics.stdev(BeneficiosTotales), 2))
    print("MEJOR RESULTADO: ", max(BeneficiosTotales))
    print("MEDIA DE RECHAZO: ", statistics.mean(ListaRechazo))
    print()



