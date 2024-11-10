# Optimización de Ganancias en Compra/Venta de Energía en una Planta Solar

Este repositorio contiene la implementación de varios algoritmos de optimización para maximizar las ganancias en la compra y venta de energía en una planta solar. Cada algoritmo está diseñado para encontrar una solución eficiente al problema de optimización de ingresos, evaluando múltiples estrategias y soluciones en el proceso.

## Algoritmos Implementados

Se han desarrollado e implementado los siguientes algoritmos de optimización:

- **Búsqueda Local Mejor Vecino**: Explora la vecindad de la solución actual, eligiendo el mejor vecino como la nueva solución en cada iteración.
- **Búsqueda Local Primer Mejor**: Selecciona el primer vecino que mejora la solución actual, buscando eficientemente hasta encontrar un aumento en la ganancia.
- **Búsqueda Aleatoria**: Genera soluciones aleatorias dentro del espacio de búsqueda, siendo útil para evitar caer en mínimos locales.
- **Enfriamiento Simulado**: Basado en un proceso de enfriamiento termodinámico, este algoritmo permite aceptar soluciones peores con cierta probabilidad, disminuyendo dicha probabilidad con el tiempo.
- **Búsqueda Tabú**: Mantiene una lista de soluciones recientemente visitadas (tabú) para evitar que el algoritmo explore las mismas regiones del espacio de búsqueda repetidamente.
- **VND (Variable Neighborhood Descent)**: Cambia dinámicamente la estructura de la vecindad, explorando diferentes vecindades en busca de una mejora.
- **Greedy**: Selecciona iterativamente las mejores opciones locales sin considerar el impacto futuro, proporcionando una solución rápida aunque no necesariamente óptima.

## Objetivo del Proyecto

El objetivo principal de este proyecto es desarrollar e implementar algoritmos que maximicen las ganancias de una planta solar mediante la optimización de sus decisiones de compra y venta de energía. Cada algoritmo ofrece un enfoque diferente al problema, permitiendo una comparación entre estrategias de optimización.

## Requisitos

- **Python 3** y las bibliotecas necesarias para ejecutar cada algoritmo.

## Cómo Empezar

1. Clona el repositorio en tu máquina local:

   ```bash
   git clone https://github.com/juandidiaz/Algoritmos-de-busqueda.git
