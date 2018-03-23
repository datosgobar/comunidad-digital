#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

# Colores para los nodos
COLORS = ['#ff0000', '#e6acac', '#d97400', '#4c4700', '#20f200',
          '#8fbfaf', '#002233', '#7989f2', '#281d73', '#e200f2',
          '#d90057', '#f20000', '#806460', '#8c5e00', '#e6f23d',
          '#283326', '#79eaf2', '#003059', '#0000f2', '#0e0033',
          '#912699', '#bf6086', '#731d1d', '#7f4620', '#ffbf40',
          '#f2ffbf', '#005924', '#396773', '#a3bfd9', '#0000cc',
          '#bbace6', '#e673cf', '#331a24', '#f27979', '#331c0d',
          '#b3aa86', '#739926', '#6cd998', '#0077b3', '#0047b3',
          '#0000bf', '#44394d', '#59003c']


def main():
    nodos = []

    def add_to_nodos(column_value):
        new_column_value = []
        for nodo in column_value:
            nodo = nodo.strip()
            nodos.append(nodo)
            new_column_value.append(nodo)
        return new_column_value

    inscriptos = pd.read_csv("../data/inscriptos.csv",
                             usecols=[6, 9, 11], encoding='utf-8')
    inscriptos.columns = ['trabaja',
                          'colabora', 'quiere_colaborar']

    inscriptos['colabora'] = inscriptos[
        'colabora'].str.split(",")
    inscriptos['quiere_colaborar'] = inscriptos[
        'quiere_colaborar'].str.split(",")
    trabaja_unique = inscriptos[
        'trabaja'].dropna().unique().tolist()

    inscriptos['colabora'].dropna().apply(add_to_nodos)

    nodos = list(set(nodos + trabaja_unique))

    colores = COLORS[0:len(nodos)]

    # Crear csv para los nodos y los colores
    pd.DataFrame({
        'name': nodos,
        'color': colores
    }).to_csv("../data/nodos-colabora.csv", encoding='utf-8', index=False)

    # Crear matriz entre todos los nodos
    matriz = []
    for nodo_destino in nodos:
        matriz_nodo = []

        for nodo_origen in nodos:
            count = 0
            # Calcular cuantas instancias hay de origen-destino
            for index, row in inscriptos.iterrows():
                if (row['trabaja'] == nodo_origen and
                        type(row['colabora']) == list and
                        nodo_destino in row['colabora']):
                    count += 1
            matriz_nodo.append(count)

        matriz.append(matriz_nodo)

    print matriz

    # Hacer lo mismo pero para quiere colaborar
    nodos = []
    inscriptos['quiere_colaborar'].dropna().apply(add_to_nodos)
    nodos = list(set(nodos + trabaja_unique))
    colores = COLORS[0:len(nodos)]

    # Crear csv para los nodos y los colores
    pd.DataFrame({
        'name': nodos,
        'color': colores
    }).to_csv("../data/nodos-quiere-colaborar.csv",
              encoding='utf-8', index=False)

    # Crear matriz entre todos los nodos
    matriz = []
    for nodo_destino in nodos:
        matriz_nodo = []

        for nodo_origen in nodos:
            count = 0
            # Calcular cuantas instancias hay de origen-destino
            for index, row in inscriptos.iterrows():
                if (row['trabaja'] == nodo_origen and
                        type(row['quiere_colaborar']) == list and
                        nodo_destino in row['quiere_colaborar']):
                    count += 1
            matriz_nodo.append(count)

        matriz.append(matriz_nodo)

    print matriz


if __name__ == "__main__":
    main()
