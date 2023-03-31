import numpy as np
import matplotlib.pyplot as plt
import copy

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


# Generar un array aleatorio de tamaño 24. En cada posición habrá
# un numero entre -100 y 100
def generar_solucion_inicial(semilla):
    np.random.seed(semilla)
    init_solution = np.random.randint(-10, 11, size=24)*10
    return init_solution


def generar_solucion_aleatoria():
    init_solution = np.random.randint(-10, 11, size=24)*10
    return init_solution


def funcion_evaluacion(solucion, radiacion, pv, pc):
    beneficio = 0
    bateria = 0
    lista_bateria = []
    lista_beneficio = []
    for i in range(len(solucion)):
        # Caso vender
        if solucion[i] >= 0:
            # Calcular la energia disponible
            energia_disponible = bateria + radiacion[i] * rendimiento

            # Calculo cuanto voy a vender y el beneficio que obtengo
            vender = solucion[i] / 100 * energia_disponible
            beneficio += vender * pv[i]

            # Si lo que quiero vender está en la batería completamente
            if vender >= bateria:
                energia_disponible -= bateria
                vender -= bateria
                bateria = 0
                # Si aun me queda por vender, sigo con la energia generada
                if vender > 0:
                    energia_disponible -= vender
                    # Si me queda energia, la meto en la bateria
                    if energia_disponible > 0:
                        bateria += energia_disponible

            # Si lo que quiero vender es menor a lo que hay en la bateria
            elif bateria > vender:
                bateria -= vender
                # La energia disponible pierde algo de la bateria, ya que es lo que he vendido
                energia_disponible -= bateria
        # Caso comprar
        else:
            # Calculo la energia disponible
            energia_disponible = bateria + radiacion[i] * rendimiento
            # Si la energia disponible cabe entera en la bateria
            if energia_disponible <= capacidad_bateria - bateria:
                bateria += energia_disponible
            # Si la energia disponible cabe parcialmente en la bateria y la bateria no esta llena
            elif energia_disponible > capacidad_bateria - bateria and bateria < capacidad_bateria:
                energia_disponible -= capacidad_bateria - bateria
                bateria = capacidad_bateria
                # Vendo lo que sobra
                beneficio += energia_disponible * pv[i]

            # Comprar porcentaje del hueco disponible de la bateria
            comprar = solucion[i] / 100 * (capacidad_bateria - bateria)
            beneficio += comprar * pc[i]
            bateria += -comprar
            # Si no compro nada, vendo(no obtendré nada)
            if comprar == 0:
                beneficio += comprar * pv[i]

        if i < 23:
            lista_bateria.append(round(bateria, 2))
            lista_beneficio.append(round(beneficio / 100, 2))

    beneficio += bateria * pv[23]
    bateria = 0
    beneficio = round(beneficio / 100, 2)
    lista_bateria.append(bateria)
    lista_beneficio.append(beneficio)

    return beneficio, lista_bateria, lista_beneficio


def generar_vecino(solucion, pos, sumar,granularidad):
    vecino = copy.copy(solucion)

    if (sumar):

        if (vecino[pos] + granularidad <= 100):
            vecino[pos] += granularidad
        else:
            vecino[pos] = 100
    else:

        if (vecino[pos] - granularidad >= -100):
            vecino[pos] -= granularidad
        else:
            vecino[pos] = -100
    return vecino

def generar_vecino_aleatorio(solucion,granularidad):
    vecino=copy.copy(solucion)
    pos=np.random.randint(0,len(solucion))
    sumar_restar=np.random.randint(0,2)
    if(sumar_restar==0):
        if(vecino[pos]+granularidad<=100):
            vecino[pos]+=granularidad
        else:
            vecino[pos]=100
    else:
        if(vecino[pos]-granularidad>=-100):
            vecino[pos]-=granularidad
        else:
            vecino[pos]=-100
    return vecino

def generar_vecino_aleatorio_tabu(solucion):
    granularidad=10
    vecino=copy.copy(solucion)
    pos=np.random.randint(0,len(solucion))
    sumar_restar=np.random.randint(0,2)
    if(sumar_restar==0):
        if(vecino[pos]+granularidad<=100):
            vecino[pos]+=granularidad
        else:
            vecino[pos]=100
    else:
        if(vecino[pos]-granularidad>=-100):
            vecino[pos]-=granularidad
        else:
            vecino[pos]=-100
    return vecino,pos,vecino[pos]


def generar_vecinosk(solucion,pos, sumar, k,granularidad):
    gran = granularidad*k
    vecino = copy.copy(solucion)

    if (sumar):
        if (vecino[pos] + granularidad <= 100):
            vecino[pos] += granularidad
        else:
            vecino[pos] = 100
    else:

        if (vecino[pos] - granularidad >= -100):
            vecino[pos] -= granularidad
        else:
            vecino[pos] = -100
    return vecino
