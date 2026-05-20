import customtkinter as ctk

# ======================================
# VARIABLES GLOBALES
# ======================================

entradas_funcion = []

entradas_restricciones = []

simbolos_restricciones = []


# ======================================
# GENERAR FORMULARIO
# ======================================

def generar_formulario(
    contenedor,
    variables,
    restricciones,
    tipo_problema
):

    global entradas_funcion
    global entradas_restricciones
    global simbolos_restricciones

    # ======================================
    # LIMPIAR VARIABLES
    # ======================================
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

    frame_funcion = ctk.CTkFrame(
        contenedor,
        corner_radius=15
    )

    frame_funcion.pack(
        pady=20,
        padx=20,
        fill="x"
    )

    lbl_funcion = ctk.CTkLabel(
        frame_funcion,
        text="Función Objetivo",
        font=("Arial", 22, "bold")
    )

    lbl_funcion.pack(pady=15)

    frame_variables = ctk.CTkFrame(
        frame_funcion,
        fg_color="transparent"
    )

    frame_variables.pack(pady=15)

    def tipo():
        if tipo_problema == "min":
            return "MinZ ="
        else:
            return "MaxZ ="

    texto_z = ctk.CTkLabel(
        frame_variables,
        text=tipo(),
        font=("Arial", 22, "bold")
    )

    texto_z.pack(side="left", padx=10)

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

        texto_variable = ctk.CTkLabel(
            frame_variables,
            text=f"X{i+1}",
            font=("Arial", 18, "bold")
        )

        texto_variable.pack(side="left", padx=5)

        if i < variables - 1:

            signo = ctk.CTkLabel(
                frame_variables,
                text="+",
                font=("Arial", 20, "bold")
            )

            signo.pack(side="left", padx=5)

    # ======================================
    # RESTRICCIONES
    # ======================================

    frame_restricciones = ctk.CTkFrame(
        contenedor,
        corner_radius=15
    )

    frame_restricciones.pack(
        pady=20,
        padx=20,
        fill="x"
    )

    lbl_restricciones = ctk.CTkLabel(
        frame_restricciones,
        text="Restricciones",
        font=("Arial", 22, "bold")
    )

    lbl_restricciones.pack(pady=15)

    for fila in range(restricciones):

        frame_fila = ctk.CTkFrame(
            frame_restricciones,
            fg_color="transparent"
        )

        frame_fila.pack(pady=10)

        fila_actual = []

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

            texto_variable = ctk.CTkLabel(
                frame_fila,
                text=f"X{columna+1}",
                font=("Arial", 18)
            )

            texto_variable.pack(side="left", padx=5)

            if columna < variables - 1:

                signo = ctk.CTkLabel(
                    frame_fila,
                    text="+",
                    font=("Arial", 18)
                )

                signo.pack(side="left", padx=5)

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

    # ======================================
    # NO NEGATIVIDAD
    # ======================================

    texto_final = " , ".join(
        [f"X{i+1}" for i in range(variables)]
    )

    lbl_no_negatividad = ctk.CTkLabel(
        contenedor,
        text=f"{texto_final} ≥ 0",
        font=("Arial", 18, "bold"),
        text_color="lightgreen"
    )

    lbl_no_negatividad.pack(
        pady=(20, 40)
    )

# ======================================
# OBTENER DATOS
# ======================================

def obtener_datos(tipo_problema):

    datos = {}

    # ======================================
    # FUNCIÓN OBJETIVO
    # ======================================

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

    # ======================================
    # RESTRICCIONES
    # ======================================

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