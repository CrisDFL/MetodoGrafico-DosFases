# ======================================
# MÉTODO GRAFICO
# ======================================

from itertools import combinations

import customtkinter as ctk
import numpy as np
from scipy.spatial import ConvexHull
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#----------------------------------
# Función para verificar si un punto es factible
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
    texto = ""

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

    # Guardar Vertices
    vertices = []
    n_restricciones = len(A)
    parejas = combinations(range(n_restricciones), 2)
    #------------------------------------------------------------------------
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
    #------------------------------------------------------------------
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
        texto += f"Restricción {i+1}: {A[i][0]}X1 + {A[i][1]}X2 {S[i]} {B[i]}\n"

        # Intersección con X1 = 0
        if A[i][1] != 0:
            texto += f"Intersección con X1=0 -> {A[i][1]}X2 = {B[i]} -> X2 = {B[i] / A[i][1]}\n"

        # Intersección con X2 = 0
        if A[i][0] != 0:
            texto += f"Intersección con X2=0 -> {A[i][0]}X1 = {B[i]} -> X1 = {B[i] / A[i][0]}\n"


    # El origen
    origen = np.array([0, 0])
    if es_factible(A, B, S, origen):
        vertices.append(origen)

    for i in range(len(vertices)):
        texto += f"Vértices de la región factible V{i+1}: {vertices[i]}\n"
    #------------------------------------------------------------------------------------------------
    # Evaluar la función objetivo en cada vértice
    resultados = []

    for punto in vertices:
        z = np.dot(c, punto)
        resultados.append((punto, z))
        texto += f"Evaluando función objetivo en el vértice {punto} -> Z = {z}\n"
    
    if datos.get("tipo_optimizacion") == "max":
        punto_optimo, valor_optimo = max(resultados, key=lambda x: x[1])
    else:
        punto_optimo, valor_optimo = min(resultados, key=lambda x: x[1])
    
    texto += f"Punto óptimo: {punto_optimo} con valor óptimo: {valor_optimo}\n"

    caja = ctk.CTkTextbox(contenedor, width=1100, height=400, font=("Consolas", 14))
    #------------------------------------------------------------------------------------
    # Grafica
    figura = Figure(figsize=(6, 5))
    ax = figura.add_subplot(111)

    # Dibujar lineas
    for i in range(n_restricciones):
    # caso normal: ambos coeficientes distintos de 0
        if A[i][0] != 0 and A[i][1] != 0:
            x1 = B[i] / A[i][0]
            x2 = B[i] / A[i][1]
            ax.plot([0, x1], [x2, 0], label=f"R{i+1}")

        # caso horizontal: X1 no aparece, solo X2
        elif A[i][0] == 0 and A[i][1] != 0:
            x2 = B[i] / A[i][1]
            ax.axhline(y=x2, label=f"R{i+1}")

        # caso vertical: X2 no aparece, solo X1
        elif A[i][1] == 0 and A[i][0] != 0:
            x1 = B[i] / A[i][0]
            ax.axvline(x=x1, label=f"R{i+1}")

    # Dibujar región factible
    puntos = np.array(vertices)
    hull = ConvexHull(puntos)
    ax.fill(puntos[hull.vertices, 0], puntos[hull.vertices, 1], alpha=0.3, color="blue")

    # Marcar los vertices
    for punto in vertices:
        ax.plot(punto[0], punto[1], "bo", markersize=6)
        ax.annotate(
            f"({round(punto[0], 2)}, {round(punto[1], 2)})",
            xy=(punto[0], punto[1]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8
        )
        # Marcar el punto óptimo
        ax.plot(punto_optimo[0], punto_optimo[1], "r*", markersize=15)
        ax.annotate(
            f"ÓPTIMO\n({round(punto_optimo[0], 2)}, {round(punto_optimo[1], 2)})\nZ={round(valor_optimo, 2)}",
            xy=(punto_optimo[0], punto_optimo[1]),
            xytext=(10, 10),
            textcoords="offset points",
            fontsize=9,
            color="red"
        )

    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(figura, master=contenedor)
    canvas.draw()
    canvas.get_tk_widget().pack(padx=20, pady=20)


    caja.pack(padx=20, pady=20, fill="both", expand=True)
    caja.insert("end", texto)
    caja.configure(state="disabled")

    