# ======================================
# MÉTODO DOS FASES
# ======================================

import customtkinter as ctk


# --------------------------------------
# Formatear números
# --------------------------------------
def fmt(valor):
    if float(valor).is_integer():
        return str(int(valor))
    return f"{valor:.2f}"


# --------------------------------------
# Método principal
# --------------------------------------
def metodo_dos_fases(contenedor, datos):

    # ----------------------------------
    # Limpiar resultados anteriores
    # ----------------------------------
    for widget in contenedor.winfo_children():
        widget.destroy()

    # ----------------------------------
    # Obtener datos
    # ----------------------------------
    funcion_objetivo = datos["funcion_objetivo"]
    restricciones = datos["restricciones"]
    tipo = datos["tipo_optimizacion"]

    texto = ""

    texto += "═" * 60 + "\n"
    texto += "MÉTODO DE DOS FASES\n"
    texto += "═" * 60 + "\n\n"

    # ==================================
    # FUNCIÓN OBJETIVO
    # ==================================
    texto += "FUNCIÓN OBJETIVO\n"
    texto += "─" * 60 + "\n"

    if tipo == "max":
        texto += "Max Z = "
    else:
        texto += "Min Z = "

    partes = []

    for i, coef in enumerate(funcion_objetivo):
        partes.append(f"{fmt(coef)}X{i+1}")

    texto += " + ".join(partes)
    texto += "\n\n"

    # ==================================
    # RESTRICCIONES
    # ==================================
    texto += "RESTRICCIONES\n"
    texto += "─" * 60 + "\n"

    for i, restriccion in enumerate(restricciones):

        expresion = []

        for j, coef in enumerate(restriccion["coeficientes"]):
            expresion.append(
                f"{fmt(coef)}X{j+1}"
            )

        texto += f"R{i+1}: "

        for k, termino in enumerate(expresion):

            if k > 0:
                texto += " + "

            texto += termino

        texto += (
            f" {restriccion['simbolo']} "
            f"{fmt(restriccion['resultado'])}\n"
        )

    texto += "\n"

    # ==================================
    # NO NEGATIVIDAD
    # ==================================
    texto += "CONDICIÓN DE NO NEGATIVIDAD\n"
    texto += "─" * 60 + "\n"

    variables = [
        f"X{i+1}"
        for i in range(len(funcion_objetivo))
    ]

    texto += ", ".join(variables)
    texto += " ≥ 0\n\n"

    texto += "MODELO RECIBIDO CORRECTAMENTE\n\n"

    # ==================================
    # FORMA ESTÁNDAR
    # ==================================
    texto += "═" * 60 + "\n"
    texto += "FORMA ESTÁNDAR\n"
    texto += "═" * 60 + "\n\n"

    contador_h = 1
    contador_e = 1
    contador_a = 1

    for i, restriccion in enumerate(restricciones):

        expresion = []

        for j, coef in enumerate(
            restriccion["coeficientes"]
        ):

            if coef != 0:

                expresion.append(
                    f"{fmt(coef)}X{j+1}"
                )

        simbolo = restriccion["simbolo"]

        # <=
        if simbolo == "<=":

            expresion.append(
                f"+ S{contador_h}"
            )

            contador_h += 1

        # >=
        elif simbolo == ">=":

            expresion.append(
                f"- E{contador_e}"
            )

            expresion.append(
                f"+ A{contador_a}"
            )

            contador_e += 1
            contador_a += 1

        # =
        elif simbolo == "=":

            expresion.append(
                f"+ A{contador_a}"
            )

            contador_a += 1

        texto += f"R{i+1}: "

        for k, termino in enumerate(expresion):

            if (
                k > 0
                and not termino.startswith("+")
                and not termino.startswith("-")
            ):
                texto += " + "

            texto += termino

        texto += (
            f" = {fmt(restriccion['resultado'])}\n"
        )

    texto += "\n"

    texto += (
        f"Variables de holgura creadas: "
        f"{contador_h - 1}\n"
    )

    texto += (
        f"Variables de exceso creadas: "
        f"{contador_e - 1}\n"
    )

    texto += (
        f"Variables artificiales creadas: "
        f"{contador_a - 1}\n"
    ) 
    # ==================================
    # COLUMNAS DEL TABLEAU
    # ==================================

    texto += "\n"
    texto += "═" * 60 + "\n"
    texto += "COLUMNAS DEL TABLEAU\n"
    texto += "═" * 60 + "\n\n"

    columnas = []

    # Variables originales
    for i in range(len(funcion_objetivo)):
        columnas.append(f"X{i+1}")

    # Holguras
    for i in range(contador_h - 1):
        columnas.append(f"S{i+1}")

    # Excesos
    for i in range(contador_e - 1):
        columnas.append(f"E{i+1}")

    # Artificiales
    for i in range(contador_a - 1):
        columnas.append(f"A{i+1}")

    columnas.append("RHS")

    texto += " | ".join(columnas)
    texto += "\n\n"

    # ==================================
    # VARIABLES BÁSICAS INICIALES
    # ==================================

    texto += "═" * 60 + "\n"
    texto += "VARIABLES BÁSICAS INICIALES\n"
    texto += "═" * 60 + "\n\n"

    variables_basicas = []

    contador_h_temp = 1
    contador_a_temp = 1

    for restriccion in restricciones:

        simbolo = restriccion["simbolo"]

        if simbolo == "<=":

            variables_basicas.append(
                f"S{contador_h_temp}"
            )

            contador_h_temp += 1

        else:

            variables_basicas.append(
                f"A{contador_a_temp}"
            )

            contador_a_temp += 1
    for i, vb in enumerate(variables_basicas):

        texto += (
            f"Fila {i+1} → {vb}\n"
        )

    texto += "\n"

    # ==================================
    # MATRIZ INICIAL FASE I
    # ==================================

    texto += "═" * 60 + "\n"
    texto += "MATRIZ INICIAL FASE I\n"
    texto += "═" * 60 + "\n\n"

    # Encabezado
    texto += "BV".ljust(8)

    for col in columnas:
        texto += col.ljust(8)

    texto += "\n"
    texto += "-" * 100 + "\n"

    # Filas de la matriz
    for fila, restriccion in enumerate(restricciones):

        texto += variables_basicas[fila].ljust(8)

        # Variables originales
        for coef in restriccion["coeficientes"]:
            texto += fmt(coef).ljust(8)

        simbolo = restriccion["simbolo"]

        # Holguras
        indice_holgura = 0

        for r in restricciones[:fila]:
            if r["simbolo"] == "<=":
                indice_holgura += 1

        for i in range(contador_h - 1):

            valor = 0

            if simbolo == "<=" and i == indice_holgura:
                valor = 1

            texto += str(valor).ljust(8)

        # Excesos
        indice_exceso = 0

        for r in restricciones[:fila]:
            if r["simbolo"] == ">=":
                indice_exceso += 1

        for i in range(contador_e - 1):

            valor = 0

            if simbolo == ">=" and i == indice_exceso:
                valor = -1

            texto += str(valor).ljust(8)

        # Artificiales
        indice_artificial = 0

        for r in restricciones[:fila]:
            if r["simbolo"] in [">=", "="]:
                indice_artificial += 1

        for i in range(contador_a - 1):

            valor = 0

            if simbolo in [">=", "="] and i == indice_artificial:
                valor = 1

            texto += str(valor).ljust(8)

        texto += (
            fmt(restriccion["resultado"])
            .ljust(8)
        )

        texto += "\n"

    texto += "\n"

    # ==================================
    # FILA W FASE I
    # ==================================

    texto += "═" * 60 + "\n"
    texto += "FILA W - FASE I\n"
    texto += "═" * 60 + "\n\n"

    texto += (
        "La función objetivo de la Fase I "
        "minimiza la suma de variables artificiales.\n\n"
    )

    artificiales = []

    for i in range(contador_a - 1):
        artificiales.append(f"A{i+1}")

    texto += "W = "

    for i, a in enumerate(artificiales):

        if i > 0:
            texto += " + "

        texto += a

    texto += "\n\n"

    texto += (
        "Variables artificiales presentes: "
        + ", ".join(artificiales)
        + "\n\n"
    )

    # ==================================
    # RESULTADO EN INTERFAZ
    # ==================================

    caja = ctk.CTkTextbox(
        contenedor,
        width=1100,
        height=600,
        font=("Consolas", 14)
    )

    caja.pack(
        padx=20,
        pady=20,
        fill="both",
        expand=True
    )

    caja.insert("end", texto)
    caja.configure(state="disabled")