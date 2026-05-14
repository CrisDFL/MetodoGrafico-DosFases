# ======================================
# MÉTODO DOS FASES
# ======================================

import customtkinter as ctk
import numpy as np


def metodo_grafico(contenedor, datos):
    c = datos.get("funcion_objetivo")
    r = datos.get("restricciones")
    
    j = []
    z = []
    for restricciones in r:
        j.append(restricciones['coeficientes'])
        z.append(restricciones['resultado'])

    
    A= np.array(j)

    B = np.array(z)

    print("Matriz A:", A)
    print("Vector b:", B)