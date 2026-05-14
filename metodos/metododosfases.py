# ======================================
# MÉTODO DOS FASES
# ======================================
import customtkinter as ctk

def metodo_dos_fases(contenedor, datos):

    """
    Recibe:
        datos -> diccionario con:
            funcion_objetivo
            restricciones
            metodo

    Retorna:
        pasos y solución
    """


    titulo = ctk.CTkLabel(
        contenedor,
        text="no",
        font=("Arial", 28, "bold")
    )

    titulo.pack(pady=20)