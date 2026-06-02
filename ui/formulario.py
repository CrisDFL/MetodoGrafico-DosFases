import tkinter as tk
import customtkinter as ctk

# ======================================
# VARIABLES GLOBALES
# ======================================

entradas_funcion = []
entradas_restricciones = []
simbolos_restricciones = []


# ======================================
# HELPER: FILA CON SCROLL HORIZONTAL
# ======================================

def fila_scrollable(contenedor, height=60):
    outer = ctk.CTkFrame(contenedor, fg_color="transparent")
    outer.pack(fill="x", pady=5, padx=10)

    canvas = tk.Canvas(outer, bg="#2b2b2b", highlightthickness=0, height=height)
    canvas.pack(side="top", fill="both", expand=True)

    scrollbar = tk.Scrollbar(
        outer,
        orient="horizontal",
        command=canvas.xview,
        bg="#2a2f45",
        troughcolor="#1a1d27",
        activebackground="#4a5170",
        relief="flat",
        bd=0,
        width=8
    )

    inner = ctk.CTkFrame(canvas, fg_color="transparent")
    window_id = canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)

    def actualizar_scroll(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.configure(height=inner.winfo_reqheight() + 4)

        contenido_ancho = inner.winfo_reqwidth()
        canvas_ancho = canvas.winfo_width()

        if contenido_ancho > canvas_ancho:
            # Contenido no cabe: alinear a la izquierda y mostrar scrollbar
            canvas.coords(window_id, 0, 0)
            canvas.itemconfig(window_id, anchor="nw")
            scrollbar.pack(side="bottom", fill="x")
        else:
            # Contenido cabe: centrar y ocultar scrollbar
            canvas.coords(window_id, canvas_ancho // 2, 0)
            canvas.itemconfig(window_id, anchor="n")
            scrollbar.pack_forget()

    inner.bind("<Configure>", actualizar_scroll)
    canvas.bind("<Configure>", actualizar_scroll)

    return inner


# ======================================
# GENERAR FORMULARIO
# ======================================

def generar_formulario(contenedor, variables, restricciones, tipo_problema):

    global entradas_funcion
    global entradas_restricciones
    global simbolos_restricciones

    entradas_funcion = []
    entradas_restricciones = []
    simbolos_restricciones = []

    # ======================================
    # TÍTULO
    # ======================================

    titulo = ctk.CTkLabel(
        contenedor,
        text="Ingreso del Modelo Matemático",
        font=("Arial", 28, "bold")
    )
    titulo.pack(pady=(20, 30))

    # ======================================
    # FUNCIÓN OBJETIVO
    # ======================================

    frame_funcion = ctk.CTkFrame(contenedor, corner_radius=15)
    frame_funcion.pack(pady=20, padx=20, fill="x")

    lbl_funcion = ctk.CTkLabel(
        frame_funcion,
        text="Función Objetivo",
        font=("Arial", 22, "bold")
    )
    lbl_funcion.pack(pady=15)

    # Fila con scroll horizontal
    frame_variables = fila_scrollable(frame_funcion, height=60)

    tipo_texto = "MinZ =" if tipo_problema == "min" else "MaxZ ="
    ctk.CTkLabel(
        frame_variables,
        text=tipo_texto,
        font=("Arial", 22, "bold")
    ).pack(side="left", padx=10)

    for i in range(variables):
        entrada = ctk.CTkEntry(
            frame_variables,
            width=80,
            height=40,
            font=("Arial", 18),
            justify="center"
        )
        entrada.pack(side="left", padx=5)
        entradas_funcion.append(entrada)

        ctk.CTkLabel(
            frame_variables,
            text=f"X{i+1}",
            font=("Arial", 18, "bold")
        ).pack(side="left", padx=5)

        if i < variables - 1:
            ctk.CTkLabel(
                frame_variables,
                text="+",
                font=("Arial", 20, "bold")
            ).pack(side="left", padx=5)

    ctk.CTkFrame(frame_funcion, fg_color="transparent", height=10).pack()

    # ======================================
    # RESTRICCIONES
    # ======================================

    frame_restricciones = ctk.CTkFrame(contenedor, corner_radius=15)
    frame_restricciones.pack(pady=20, padx=20, fill="x")

    ctk.CTkLabel(
        frame_restricciones,
        text="Restricciones",
        font=("Arial", 22, "bold")
    ).pack(pady=15)

    for fila in range(restricciones):

        fila_actual = []

        # Cada fila de restricción tiene su propio scroll horizontal
        frame_fila = fila_scrollable(frame_restricciones, height=55)

        for columna in range(variables):
            entrada = ctk.CTkEntry(
                frame_fila,
                width=80,
                height=40,
                font=("Arial", 18),
                justify="center"
            )
            entrada.pack(side="left", padx=5)
            fila_actual.append(entrada)

            ctk.CTkLabel(
                frame_fila,
                text=f"X{columna+1}",
                font=("Arial", 18)
            ).pack(side="left", padx=5)

            if columna < variables - 1:
                ctk.CTkLabel(
                    frame_fila,
                    text="+",
                    font=("Arial", 18)
                ).pack(side="left", padx=5)

        simbolo = ctk.CTkComboBox(
            frame_fila,
            values=["<=", ">=", "="],
            width=90,
            height=40,
            font=("Arial", 16),
            state="readonly"
        )
        simbolo.set("<=")
        simbolo.pack(side="left", padx=10)
        simbolos_restricciones.append(simbolo)

        resultado = ctk.CTkEntry(
            frame_fila,
            width=100,
            height=40,
            font=("Arial", 18),
            justify="center"
        )
        resultado.pack(side="left", padx=10)
        fila_actual.append(resultado)
        entradas_restricciones.append(fila_actual)

    ctk.CTkFrame(frame_restricciones, fg_color="transparent", height=10).pack()

    # ======================================
    # NO NEGATIVIDAD
    # ======================================

    texto_final = " , ".join([f"X{i+1}" for i in range(variables)])

    ctk.CTkLabel(
        contenedor,
        text=f"{texto_final} ≥ 0",
        font=("Arial", 18, "bold"),
        text_color="lightgreen"
    ).pack(pady=(20, 40))


# ======================================
# OBTENER DATOS
# ======================================

def obtener_datos(tipo_problema):

    datos = {}

    funcion_objetivo = []
    for entrada in entradas_funcion:
        try:
            valor = entrada.get()
            if valor == "":
                valor = 0
            funcion_objetivo.append(float(valor))
        except:
            funcion_objetivo.append(0)

    datos["funcion_objetivo"] = funcion_objetivo
    datos["tipo_optimizacion"] = tipo_problema

    restricciones = []
    for i, fila in enumerate(entradas_restricciones):
        restriccion = {}
        coeficientes = []

        for entrada in fila[:-1]:
            try:
                valor = entrada.get()
                if valor == "":
                    valor = 0
                coeficientes.append(float(valor))
            except:
                coeficientes.append(0)

        try:
            resultado = fila[-1].get()
            if resultado == "":
                resultado = 0
            resultado = float(resultado)
        except:
            resultado = 0

        restriccion["coeficientes"] = coeficientes
        restriccion["simbolo"] = simbolos_restricciones[i].get()
        restriccion["resultado"] = resultado
        restricciones.append(restriccion)

    datos["restricciones"] = restricciones
    return datos