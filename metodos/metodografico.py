# ======================================
# MÉTODO GRAFICO
# ======================================

from itertools import combinations

import customtkinter as ctk
import numpy as np

def es_factible(A, B, S, punto):

    resultados = np.dot(A, punto)
    for i in range(len(B)):
        if S[i] == "<=":
            if resultados[i] > B[i] + 1e-9:
                return False
        elif S[i] == ">=":
            if resultados[i] < B[i] - 1e-9:
                return False
        elif S[i] == "=":
            if abs(resultados[i] - B[i]) > 1e-9:
                return False
    return all(punto >= 0)

def metodo_grafico(contenedor, datos):
    c = datos.get("funcion_objetivo")
    r = datos.get("restricciones")

    coheficientes = []
    resultado = []
    signos = []
    for restricciones in r:
        coheficientes.append(restricciones['coeficientes'])
        resultado.append(restricciones['resultado'])
        signos.append(restricciones['simbolo'])

    A = np.array(coheficientes)
    B = np.array(resultado)
    S = np.array(signos)
    print(S)

    # Guardar Vertices
    vertices = []
    n_restricciones = len(A)
    parejas = combinations(range(n_restricciones), 2)

    # Intersección de cada par de restricciones
    for i, j in parejas:
        A_temp = np.array([A[i], A[j]])
        B_temp = np.array([B[i], B[j]])
        try:
            punto = np.linalg.solve(A_temp, B_temp)
            if es_factible(A, B, S, punto):
                vertices.append(punto)
        except np.linalg.LinAlgError:
            continue

    # Intersecciones con los ejes
    for i in range(n_restricciones):
        # X1 = 0, despeja X2
        if A[i][1] != 0:
            punto = np.array([0, B[i] / A[i][1]])
            if es_factible(A, B, S, punto):
                vertices.append(punto)

        # X2 = 0, despeja X1
        if A[i][0] != 0:
            punto = np.array([B[i] / A[i][0], 0])
            if es_factible(A, B, S, punto):
                vertices.append(punto)

        # Impresion de operaciones
        print('Restriccion', i+1, ':',
            A[i][0], 'X1 +',
            A[i][1], 'X2',
            S[i], B[i])

        # Intersección con X1 = 0
        if A[i][1] != 0:
            print('Interseccion con X1=0 ->',
                A[i][1], 'X2 =', B[i], '->', 'X2 =', B[i] / A[i][1])

        # Intersección con X2 = 0
        if A[i][0] != 0:
            print('Interseccion con X2=0 ->',
                A[i][0], 'X1 =', B[i], '->', 'X1 =', B[i] / A[i][0])

        print()

    # El origen
    origen = np.array([0, 0])

    if es_factible(A, B, S, origen):
        vertices.append(origen)

    for i in range(len(vertices)):
        print('Vértices de la región factible:', 'V', i+1, ':', vertices[i])

    # Evaluar la función objetivo en cada vértice
    resultados = []

    for punto in vertices:

        z = np.dot(c, punto)

        resultados.append((punto, z))

        print('Evaluando función objetivo en el vértice:', punto, '->', z)
    
    if datos.get("tipo_optimizacion") == "max":
        punto_optimo, valor_optimo = max(resultados, key=lambda x: x[1])
    else:
        punto_optimo, valor_optimo = min(resultados, key=lambda x: x[1])
    print("Punto óptimo:", punto_optimo)
    print("Valor óptimo:", valor_optimo)