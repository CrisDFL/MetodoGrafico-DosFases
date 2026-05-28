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

def obtener_columna_pivote(fila_w, columnas):

    menor = 0
    indice = None

    for i in range(len(fila_w) - 1):

        nombre_columna = columnas[i]

        # NO permitir artificiales
        if nombre_columna.startswith("A"):
            continue

        if fila_w[i] < menor:

            menor = fila_w[i]
            indice = i

    return indice, menor

def obtener_fila_pivote(matriz, indice_pivote):

    razones = []

    for fila in range(len(matriz)):

        coef = matriz[fila][indice_pivote]

        rhs = matriz[fila][-1]

        if coef > 0:

            razones.append(
                (rhs / coef, fila)
            )

    return min(razones)


def normalizar_fila(fila, pivote):

    return [
        valor / pivote
        for valor in fila
    ]


def hacer_ceros(
    matriz,
    fila_pivote,
    indice_pivote
):

    nueva_fila = matriz[fila_pivote]

    for fila in range(len(matriz)):

        if fila != fila_pivote:

            factor = matriz[fila][indice_pivote]

            matriz[fila] = [

                matriz[fila][j]
                - factor * nueva_fila[j]

                for j in range(len(matriz[fila]))
            ]

    return matriz


def recalcular_w(
    matriz,
    variables_basicas,
    columnas
):

    fila_w = [0] * len(columnas)

    for fila in range(len(matriz)):

        vb = variables_basicas[fila]

        if vb.startswith("A"):

            for j in range(len(columnas)):

                fila_w[j] -= matriz[fila][j]

    return fila_w


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
    # FILA W NUMÉRICA REAL
    # ==================================

    texto += "Fila W corregida:\n\n"

    # Crear fila W inicial
    fila_w = [0] * len(columnas)

    # Buscar filas con artificiales básicas
    for fila, vb in enumerate(variables_basicas):

        if vb.startswith("A"):

            restriccion = restricciones[fila]

            # Variables originales
            for i, coef in enumerate(
                restriccion["coeficientes"]
            ):
                fila_w[i] -= coef

            indice_columna = len(funcion_objetivo)

            # Holguras
            contador_temp = 0

            for r in restricciones:

                if r["simbolo"] == "<=":

                    if contador_temp == (
                        sum(
                            1
                            for rr in restricciones[:fila]
                            if rr["simbolo"] == "<="
                        )
                    ):
                        fila_w[indice_columna] -= 1

                    contador_temp += 1

                    indice_columna += 1

            # Excesos
            contador_temp = 0

            for r in restricciones:

                if r["simbolo"] == ">=":

                    if contador_temp == (
                        sum(
                            1
                            for rr in restricciones[:fila]
                            if rr["simbolo"] == ">="
                        )
                    ):
                        fila_w[indice_columna] += 1

                    contador_temp += 1

                    indice_columna += 1

            # Artificiales
            contador_temp = 0

            for r in restricciones:

                if r["simbolo"] in [">=", "="]:

                    if contador_temp == (
                        sum(
                            1
                            for rr in restricciones[:fila]
                            if rr["simbolo"] in [">=", "="]
                        )
                    ):
                        fila_w[indice_columna] -= 1

                    contador_temp += 1

                    indice_columna += 1

            # RHS
            fila_w[-1] -= restriccion["resultado"]

    # Mostrar fila W
    texto += "W".ljust(8)

    for valor in fila_w:
        texto += fmt(valor).ljust(8)

    texto += "\n\n"
    
        # ==================================
    # COLUMNA PIVOTE
    # ==================================

    texto += "═" * 60 + "\n"
    texto += "COLUMNA PIVOTE\n"
    texto += "═" * 60 + "\n\n"
    indice_pivote, menor = (
        obtener_columna_pivote(
            fila_w,
            columnas
        )
    )

    columna_pivote = columnas[
        indice_pivote
    ]

    texto += (
        f"Valor más negativo en W: "
        f"{fmt(menor)}\n"
    )

    texto += (
        f"Columna pivote seleccionada: "
        f"{columna_pivote}\n\n"
    )
    

    # ==================================
    # FILA PIVOTE
    # ==================================

    texto += "═" * 60 + "\n"
    texto += "FILA PIVOTE\n"
    texto += "═" * 60 + "\n\n"

    texto += (
        "Cálculo de razón mínima:\n\n"
    )

    razones = []

    for fila, restriccion in enumerate(restricciones):

        coef_pivote = restriccion["coeficientes"][
            indice_pivote
        ]

        rhs = restriccion["resultado"]

        if coef_pivote > 0:

            razon = rhs / coef_pivote

            razones.append(
                (razon, fila)
            )

            texto += (
                f"Fila {fila+1}: "
                f"{fmt(rhs)} / "
                f"{fmt(coef_pivote)} "
                f"= {fmt(razon)}\n"
            )

        else:

            texto += (
                f"Fila {fila+1}: "
                "No válida\n"
            )

    texto += "\n"

    # Buscar menor positivo
    menor_razon, fila_pivote = min(razones)

    texto += (
        f"Menor razón positiva: "
        f"{fmt(menor_razon)}\n"
    )

    texto += (
        f"Fila pivote seleccionada: "
        f"Fila {fila_pivote + 1}\n"
    )

    elemento_pivote = restricciones[
        fila_pivote
    ]["coeficientes"][indice_pivote]

    texto += (
        f"Elemento pivote: "
        f"{fmt(elemento_pivote)}\n\n"
    )
    
        # ==================================
    # NORMALIZAR FILA PIVOTE
    # ==================================

    texto += "═" * 60 + "\n"
    texto += "NORMALIZACIÓN FILA PIVOTE\n"
    texto += "═" * 60 + "\n\n"

    texto += (
        f"Fila pivote seleccionada: "
        f"Fila {fila_pivote + 1}\n"
    )

    texto += (
        f"Elemento pivote: "
        f"{fmt(elemento_pivote)}\n\n"
    )

    # Construir fila completa
    fila_completa = []

    restriccion_pivote = restricciones[
        fila_pivote
    ]

    # Variables originales
    for coef in restriccion_pivote[
        "coeficientes"
    ]:
        fila_completa.append(coef)

    simbolo = restriccion_pivote["simbolo"]

    # Holguras
    indice_h = 0

    for i in range(contador_h - 1):

        valor = 0

        if simbolo == "<=" and i == (
            sum(
                1
                for r in restricciones[:fila_pivote]
                if r["simbolo"] == "<="
            )
        ):
            valor = 1

        fila_completa.append(valor)

    # Excesos
    for i in range(contador_e - 1):

        valor = 0

        if simbolo == ">=" and i == (
            sum(
                1
                for r in restricciones[:fila_pivote]
                if r["simbolo"] == ">="
            )
        ):
            valor = -1

        fila_completa.append(valor)

    # Artificiales
    for i in range(contador_a - 1):

        valor = 0

        if simbolo in [">=", "="] and i == (
            sum(
                1
                for r in restricciones[:fila_pivote]
                if r["simbolo"] in [">=", "="]
            )
        ):
            valor = 1

        fila_completa.append(valor)

    # RHS
    fila_completa.append(
        restriccion_pivote["resultado"]
    )

    # Dividir entre pivote
    nueva_fila = []

    for valor in fila_completa:
        nueva_fila.append(
            valor / elemento_pivote
        )

    texto += (
        "Nueva fila pivote:\n\n"
    )

    texto += " ".ljust(8)

    for valor in nueva_fila:
        texto += fmt(valor).ljust(8)

    texto += "\n\n"
    
        # ==================================
    # NUEVO TABLEAU
    # ==================================

    texto += "═" * 60 + "\n"
    texto += "PRIMERA ITERACIÓN SIMPLEX\n"
    texto += "═" * 60 + "\n\n"

    texto += (
        "Se realizan operaciones fila "
        "para hacer cero toda la columna pivote.\n\n"
    )

    # Construir matriz completa original
    matriz = []

    for fila, restriccion in enumerate(restricciones):

        fila_actual = []

        # Variables originales
        for coef in restriccion["coeficientes"]:
            fila_actual.append(coef)

        simbolo = restriccion["simbolo"]

        # Holguras
        for i in range(contador_h - 1):

            valor = 0

            if simbolo == "<=" and i == (
                sum(
                    1
                    for r in restricciones[:fila]
                    if r["simbolo"] == "<="
                )
            ):
                valor = 1

            fila_actual.append(valor)

        # Excesos
        for i in range(contador_e - 1):

            valor = 0

            if simbolo == ">=" and i == (
                sum(
                    1
                    for r in restricciones[:fila]
                    if r["simbolo"] == ">="
                )
            ):
                valor = -1

            fila_actual.append(valor)

        # Artificiales
        for i in range(contador_a - 1):

            valor = 0

            if simbolo in [">=", "="] and i == (
                sum(
                    1
                    for r in restricciones[:fila]
                    if r["simbolo"] in [">=", "="]
                )
            ):
                valor = 1

            fila_actual.append(valor)

        # RHS
        fila_actual.append(
            restriccion["resultado"]
        )

        matriz.append(fila_actual)

    # Reemplazar fila pivote normalizada
    matriz[fila_pivote] = nueva_fila

    # Hacer ceros
    for fila in range(len(matriz)):

        if fila != fila_pivote:

            factor = matriz[fila][indice_pivote]

            nueva = []

            for j in range(len(matriz[fila])):

                valor = (
                    matriz[fila][j]
                    - factor * nueva_fila[j]
                )

                nueva.append(valor)

            matriz[fila] = nueva

    # Cambiar variable básica
    variables_basicas[fila_pivote] = columna_pivote

    # Mostrar nuevo tableau

    texto += "BV".ljust(8)

    for col in columnas:
        texto += col.ljust(8)

    texto += "\n"
    texto += "-" * 120 + "\n"

    for fila in range(len(matriz)):

        texto += (
            variables_basicas[fila]
            .ljust(8)
        )

        for valor in matriz[fila]:

            texto += (
                fmt(valor)
                .ljust(8)
            )

        texto += "\n"

    texto += "\n"
    
    
    
        # ==================================
    # NUEVA FILA W
    # ==================================

    texto += "═" * 60 + "\n"
    texto += "NUEVA FILA W\n"
    
    
    texto += "═" * 60 + "\n\n"

    nueva_w = [0] * len(columnas)

    # Restar filas artificiales básicas
    for fila in range(len(matriz)):

        vb = variables_basicas[fila]

        if vb.startswith("A"):

            for j in range(len(columnas)):

                nueva_w[j] -= matriz[fila][j]

    texto += "W".ljust(8)

    for valor in nueva_w:
        texto += fmt(valor).ljust(8)

    texto += "\n\n"

       # ==================================
    # ITERACIONES AUTOMÁTICAS
    # ==================================

    iteracion = 2
    max_iteraciones = 20

    while (
        min(nueva_w[:-1]) < 0
        and iteracion <= max_iteraciones
    ):

        texto += "═" * 60 + "\n"
        texto += "═" * 60 + "\n"
        texto += f"ITERACIÓN {iteracion}\n"
        texto += "═" * 60 + "\n\n"

        indice_pivote, menor = (
    obtener_columna_pivote(
        nueva_w,
        columnas
    )
)

        columna_pivote = columnas[
            indice_pivote
        ]

        texto += (
            f"Columna pivote: "
            f"{columna_pivote}\n"
        )

        texto += (
            f"Valor más negativo: "
            f"{fmt(menor)}\n\n"
        )

        menor_razon, fila_pivote = (
            obtener_fila_pivote(
                matriz,
                indice_pivote
            )
        )

        pivote = matriz[fila_pivote][
            indice_pivote
        ]

        texto += (
            f"Fila pivote: "
            f"{fila_pivote + 1}\n"
        )

        texto += (
            f"Pivote: "
            f"{fmt(pivote)}\n\n"
        )

        matriz[fila_pivote] = (
            normalizar_fila(
                matriz[fila_pivote],
                pivote
            )
        )

        matriz = hacer_ceros(
            matriz,
            fila_pivote,
            indice_pivote
        )

        sale = variables_basicas[
            fila_pivote
        ]

        variables_basicas[fila_pivote] = (
            columna_pivote
        )

        texto += (
            f"Sale de la base: "
            f"{sale}\n"
        )

        texto += (
            f"Entra a la base: "
            f"{columna_pivote}\n\n"
        )

        texto += "BV".ljust(8)

        for col in columnas:
            texto += col.ljust(8)

        texto += "\n"
        texto += "-" * 120 + "\n"

        for fila in range(len(matriz)):

            texto += (
                variables_basicas[fila]
                .ljust(8)
            )

            for valor in matriz[fila]:

                texto += (
                    fmt(valor)
                    .ljust(8)
                )

            texto += "\n"

        texto += "\n"

        nueva_w = recalcular_w(
            matriz,
            variables_basicas,
            columnas
        )

        texto += "W".ljust(8)

        for valor in nueva_w:

            texto += (
                fmt(valor)
                .ljust(8)
            )

        texto += "\n\n"

        iteracion += 1

        if iteracion > max_iteraciones:

            texto += "Se alcanzó el límite "
            texto += "máximo de iteraciones.\n\n"

            break
    
    texto += "═" * 60 + "\n"
    texto += "FIN FASE I\n"
    texto += "═" * 60 + "\n\n"

    texto += (
        "Ya no existen valores negativos "
        "en la fila W.\n"
    )

    texto += (
        "La solución básica factible "
        "ha sido encontrada.\n\n"
    )
   
   
       # ==================================
    # VALIDACIÓN FASE I
    # ==================================

    texto += "═" * 60 + "\n"
    texto += "VALIDACIÓN FASE I\n"
    texto += "═" * 60 + "\n\n"

    valor_w = nueva_w[-1]

    texto += (
        f"Valor final de W: "
        f"{fmt(valor_w)}\n\n"
    )

    artificiales_en_base = []

    for vb in variables_basicas:

        if vb.startswith("A"):

            artificiales_en_base.append(vb)

    if valor_w == 0 and len(artificiales_en_base) == 0:

        texto += (
            "La Fase I terminó correctamente.\n"
        )

        texto += (
            "Existe solución básica factible.\n\n"
        )
        

    else:

        texto += (
            "El problema NO tiene "
            "solución factible.\n\n"
        )

        texto += (
            "Existen variables artificiales "
            "en la base o W ≠ 0.\n\n"
        )
   
   
       # ==================================
    # INICIO FASE II
    # ==================================

    texto += "═" * 60 + "\n"
    texto += "INICIO FASE II\n"
    texto += "═" * 60 + "\n\n"

    texto += (
        "Se eliminan las columnas "
        "artificiales.\n\n"
    )

    # ----------------------------------
    # Eliminar artificiales
    # ----------------------------------

    indices_eliminar = []

    for i, col in enumerate(columnas):

        if col.startswith("A"):

            indices_eliminar.append(i)

    # Eliminar columnas de derecha a izquierda
    for indice in reversed(indices_eliminar):

        columnas.pop(indice)

        for fila in matriz:

            fila.pop(indice)

    texto += "Columnas restantes:\n\n"

    texto += " | ".join(columnas)
    texto += "\n\n"
   
   
       # ==================================
    # TABLEAU INICIAL FASE II
    # ==================================

    texto += "Tableau inicial Fase II:\n\n"

    texto += "BV".ljust(8)

    for col in columnas:
        texto += col.ljust(8)

    texto += "\n"

    texto += "-" * 120 + "\n"

    for fila in range(len(matriz)):

        texto += (
            variables_basicas[fila]
            .ljust(8)
        )

        for valor in matriz[fila]:

            texto += (
                fmt(valor)
                .ljust(8)
            )

        texto += "\n"

    texto += "\n"
    
    
        # ==================================
    # FILA Z ORIGINAL
    # ==================================

    texto += "═" * 60 + "\n"
    texto += "FILA Z ORIGINAL\n"
    texto += "═" * 60 + "\n\n"

    # Crear fila Z
    fila_z = [0] * len(columnas)

    # Coeficientes originales
    for i, coef in enumerate(funcion_objetivo):

        if tipo == "max":
            fila_z[i] = -coef
        else:
            fila_z[i] = coef

    # Ajustar según variables básicas
    for fila, vb in enumerate(variables_basicas):

        if vb.startswith("X"):

            indice_variable = int(
                vb.replace("X", "")
            ) - 1

            coef_objetivo = funcion_objetivo[
                indice_variable
            ]

            for j in range(len(columnas)):

                fila_z[j] += (
                    coef_objetivo
                    * matriz[fila][j]
                )

    texto += "Z".ljust(8)

    for valor in fila_z:

        texto += (
            fmt(valor)
            .ljust(8)
        )

    texto += "\n\n"
    
    
    
        # ==================================
    # SIMPLEX FASE II
    # ==================================

    texto += "═" * 60 + "\n"
    texto += "OPTIMIZACIÓN FASE II\n"
    texto += "═" * 60 + "\n\n"

    iteracion_fase2 = 1

    while min(fila_z[:-1]) < 0:

        texto += (
            f"ITERACIÓN FASE II "
            f"{iteracion_fase2}\n"
        )

        texto += "-" * 60 + "\n\n"

        # -----------------------------
        # Columna pivote
        # -----------------------------

        menor = min(fila_z[:-1])

        indice_pivote = fila_z.index(menor)

        columna_pivote = columnas[
            indice_pivote
        ]

        texto += (
            f"Columna pivote: "
            f"{columna_pivote}\n"
        )

        # -----------------------------
        # Fila pivote
        # -----------------------------

        razones = []

        for fila in range(len(matriz)):

            coef = matriz[fila][
                indice_pivote
            ]

            rhs = matriz[fila][-1]

            if coef > 0:

                razon = rhs / coef

                razones.append(
                    (razon, fila)
                )

        menor_razon, fila_pivote = (
            min(razones)
        )

        pivote = matriz[fila_pivote][
            indice_pivote
        ]

        texto += (
            f"Fila pivote: "
            f"{fila_pivote + 1}\n"
        )

        texto += (
            f"Pivote: "
            f"{fmt(pivote)}\n\n"
        )

        # -----------------------------
        # Normalizar
        # -----------------------------

        matriz[fila_pivote] = [

            valor / pivote

            for valor in matriz[
                fila_pivote
            ]
        ]

        # -----------------------------
        # Hacer ceros
        # -----------------------------

        for fila in range(len(matriz)):

            if fila != fila_pivote:

                factor = matriz[fila][
                    indice_pivote
                ]

                matriz[fila] = [

                    matriz[fila][j]
                    - factor *
                    matriz[fila_pivote][j]

                    for j in range(
                        len(matriz[fila])
                    )
                ]

        # -----------------------------
        # Actualizar básicas
        # -----------------------------

        sale = variables_basicas[
            fila_pivote
        ]

        variables_basicas[fila_pivote] = (
            columna_pivote
        )

        texto += (
            f"Sale: {sale}\n"
        )

        texto += (
            f"Entra: {columna_pivote}\n\n"
        )

        # -----------------------------
        # Recalcular Z
        # -----------------------------

        fila_z = [0] * len(columnas)

        for i, coef in enumerate(
            funcion_objetivo
        ):

            fila_z[i] = -coef

        for fila, vb in enumerate(
            variables_basicas
        ):

            if vb.startswith("X"):

                indice_variable = int(
                    vb.replace("X", "")
                ) - 1

                coef_obj = funcion_objetivo[
                    indice_variable
                ]

                for j in range(
                    len(columnas)
                ):

                    fila_z[j] += (
                        coef_obj
                        * matriz[fila][j]
                    )

        # -----------------------------
        # Mostrar tableau
        # -----------------------------

        texto += "BV".ljust(8)

        for col in columnas:
            texto += col.ljust(8)

        texto += "\n"

        texto += "-" * 120 + "\n"

        for fila in range(len(matriz)):

            texto += (
                variables_basicas[fila]
                .ljust(8)
            )

            for valor in matriz[fila]:

                texto += (
                    fmt(valor)
                    .ljust(8)
                )

            texto += "\n"

        texto += "\n"

        texto += "Z".ljust(8)

        for valor in fila_z:

            texto += (
                fmt(valor)
                .ljust(8)
            )

        texto += "\n\n"

        iteracion_fase2 += 1
        # ==================================
    # SOLUCIÓN ÓPTIMA
    # ==================================

    texto += "═" * 60 + "\n"
    texto += "SOLUCIÓN ÓPTIMA\n"
    texto += "═" * 60 + "\n\n"

    solucion = {}

    # Variables originales
    for i in range(len(funcion_objetivo)):

        nombre = f"X{i+1}"

        solucion[nombre] = 0

    # Buscar variables básicas
    for fila, vb in enumerate(variables_basicas):

        if vb.startswith("X"):

            solucion[vb] = matriz[fila][-1]

    # Mostrar solución
    for variable, valor in solucion.items():

        texto += (
            f"{variable} = "
            f"{fmt(valor)}\n"
        )

    texto += "\n"

    texto += (
        f"Valor óptimo de Z = "
        f"{fmt(fila_z[-1])}\n\n"
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