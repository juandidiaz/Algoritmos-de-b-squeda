import matplotlib.pyplot as plt

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


def greedy_real():
    solucion = []
    bateria = 0
    beneficio = 0
    lista_bateria = []
    lista_beneficio = []
    precio_maximo = max(real_pv)
    # Obtengo la hora a la que vendo
    hora_venta = real_pv.index(precio_maximo)
    for i in range(24):
        # Si la hora es menor a la de venta
        if i < hora_venta:
            producido = real_r[i] * rendimiento
            # No está la batería llena y lo que genero cabe
            if producido <= capacidad_bateria - bateria and bateria < capacidad_bateria:
                bateria += producido
                producido = 0
            # No esta la bateria llena y no cabe toda la energia generada
            elif producido > capacidad_bateria - bateria and bateria < capacidad_bateria:
                # Calculamos cuanta energia cabe en la bateria hasta que consiga llenarse
                producido -= capacidad_bateria - bateria
                # La bateria esta completamente llena
                bateria = capacidad_bateria
            # Vendemos lo que sobre
            beneficio += producido * real_pv[i]
            solucion.append(0)
        else:
            disponible = bateria + real_r[i] * rendimiento
            beneficio += disponible * real_pv[i]
            # La bateria se vacia
            bateria = 0
            solucion.append(100)

        lista_bateria.append(round(bateria, 2))
        lista_beneficio.append(round(beneficio / 100, 2))
    beneficio = round(beneficio / 100, 2)
    return solucion, beneficio, lista_bateria, lista_beneficio, hora_venta


def greedy_aleatorio():
    solucion = []
    bateria = 0
    beneficio = 0
    lista_bateria = []
    lista_beneficio = []
    precio_maximo = max(random_pv)
    hora_venta = random_pv.index(precio_maximo)
    for i in range(24):
        # Si la hora es menor a la de venta
        if i < hora_venta:
            producido = random_r[i] * rendimiento
            # No está la batería llena y lo que genero cabe
            if producido <= capacidad_bateria - bateria and bateria < capacidad_bateria:
                bateria += producido
                producido = 0
            # No esta la bateria llena y no cabe toda la energia generada
            elif producido > capacidad_bateria - bateria and bateria < capacidad_bateria:
                # Calculamos cuanta energia cabe en la bateria hasta que consiga llenarse
                producido -= capacidad_bateria - bateria
                # La bateria esta completamente llena
                bateria = capacidad_bateria
            # Vendemos lo que sobre
            beneficio += producido * random_pv[i]
            solucion.append(0)
        else:
            disponible = bateria + random_r[i] * rendimiento
            beneficio += disponible * random_pv[i]
            bateria = 0
            solucion.append(100)

        lista_bateria.append(round(bateria, 2))
        lista_beneficio.append(round(beneficio / 100, 2))
    beneficio = round(beneficio / 100, 2)
    return solucion, beneficio, lista_bateria, lista_beneficio, hora_venta








