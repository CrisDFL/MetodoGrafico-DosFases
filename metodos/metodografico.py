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

# Funcion para identificar si es entero o decimal
def fmt(valor):
    return f"{int(valor)}" if float(valor).is_integer() else f"{valor:.2f}"

# Funcion principal
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
    texto += "\n" + "═" * 40 + "\n"
    texto += "ANÁLISIS DE RESTRICCIONES\n"
    texto += "═" * 40 + "\n\n"

    for i in range(n_restricciones):
        texto += f"  ▸ Restricción {i+1}:  {A[i][0]}X₁ + {A[i][1]}X₂  {S[i]}  {B[i]}\n"
        texto += "  " + "─" * 45 + "\n"

        # X1 = 0, despeja X2
        if A[i][1] != 0:
            val = B[i] / A[i][1]
            punto = np.array([0, val])
            texto += f"    • Intersección con X₁ = 0:\n"
            texto += f"      {A[i][1]}X₂ = {B[i]}  →  X₂ = {fmt(val)}\n"
            texto += f"      Punto: (0, {fmt(val)})\n"
            if es_factible(A, B, S, punto):
                vertices.append(punto)
                texto += f"      ✔ Factible → se agrega como vértice\n"
            else:
                texto += f"      ✘ No factible → descartado\n"

        # X2 = 0, despeja X1
        if A[i][0] != 0:
            val = B[i] / A[i][0]
            punto = np.array([val, 0])
            texto += f"    • Intersección con X₂ = 0:\n"
            texto += f"      {A[i][0]}X₁ = {B[i]}  →  X₁ = {fmt(val)}\n"
            texto += f"      Punto: ({fmt(val)}, 0)\n"
            if es_factible(A, B, S, punto):
                vertices.append(punto)
                texto += f"      ✔ Factible → se agrega como vértice\n"
            else:
                texto += f"      ✘ No factible → descartado\n"

        texto += "\n"

    # El origen
    texto += "═" * 40 + "\n"
    texto += "VERIFICACIÓN DEL ORIGEN\n"
    texto += "═" * 40 + "\n\n"

    origen = np.array([0, 0])
    if es_factible(A, B, S, origen):
        vertices.append(origen)
        texto += "  ✔ El origen (0, 0) es factible → se agrega como vértice\n\n"
    else:
        texto += "  ✘ El origen (0, 0) no es factible → descartado\n\n"


    #-----------------------------------------------------
    # EVALUACIÓN DE LA FUNCIÓN OBJETIVO
    texto += "═" * 40 + "\n"
    texto += "EVALUACIÓN DE LA FUNCIÓN OBJETIVO\n"
    texto += "═" * 40 + "\n\n"

    resultados = []
    for i, punto in enumerate(vertices):
        z = np.dot(c, punto)
        resultados.append((punto, z))
        texto += f"  V{i+1}  ({fmt(punto[0])}, {fmt(punto[1])})  →  Z = {fmt(z)}\n"

    texto += "\n"
    
    # ----------------------------------------------------
    # RESULTADO ÓPTIMO
    texto += "═" * 40 + "\n"

    if datos.get("tipo_optimizacion") == "max":
        punto_optimo, valor_optimo = max(resultados, key=lambda x: x[1])
        texto += "SOLUCIÓN ÓPTIMA  (MAXIMIZACIÓN)\n"
    else:
        punto_optimo, valor_optimo = min(resultados, key=lambda x: x[1])
        texto += "SOLUCIÓN ÓPTIMA  (MINIMIZACIÓN)\n"

    texto += "═" * 40 + "\n\n"
    texto += f"  X₁ = {fmt(punto_optimo[0])}\n"
    texto += f"  X₂ = {fmt(punto_optimo[1])}\n"
    texto += f"  Z  = {fmt(valor_optimo)}\n\n"
    texto += "═" * 40 + "\n"

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
            f"({fmt(punto[0])}, {fmt(punto[1])})",
            xy=(punto[0], punto[1]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8
        )
        # Marcar el punto óptimo
        ax.plot(punto_optimo[0], punto_optimo[1], "r*", markersize=15)
        ax.annotate(
            f"ÓPTIMO\n({fmt(punto_optimo[0])}, {fmt(punto_optimo[1])})\nZ={fmt(valor_optimo)}",
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

    