# ======================================================================
# MÉTODO DOS FASES - VISUAL DARK MODE CON WIDGETS CTK
# ======================================================================

import customtkinter as ctk
from fractions import Fraction
from tkinter import ttk
from ui.estilo import (
    BG_MAIN, BG_CARD, BG_TABLE_HEAD, BG_TABLE_ROW, BG_TABLE_ALT,
    BG_PIVOT_COL, BG_PIVOT_CELL, BG_W_ROW, BG_RESULT,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_ACCENT, TEXT_GOLD,
    TEXT_GREEN, TEXT_RED, TEXT_BLUE, TEXT_PURPLE, TEXT_HEAD,
    BORDER_COLOR, BORDER_ACCENT,
    FONT_TITLE, FONT_HEAD, FONT_BODY, FONT_SMALL, FONT_LABEL, FONT_RESULT
)


# ── Helpers de fracción ───────────────────────────────────────────────
def fmt(valor):
    if isinstance(valor, float):
        valor = Fraction(valor).limit_denominator()
    if valor.numerator == 0:
        return "0"
    if valor.denominator == 1:
        return str(valor.numerator)
    return f"{valor.numerator}/{valor.denominator}"

# ── Helpers visuales ──────────────────────────────────────────────────
def seccion_titulo(parent, texto, color=TEXT_ACCENT):
    """Línea separadora con texto centrado, sin contenedor propio."""
    # Espacio superior
    ctk.CTkFrame(parent, fg_color="transparent", height=10).pack()
    # Línea hr superior
    ctk.CTkFrame(parent, fg_color=BORDER_ACCENT, height=1,
                 corner_radius=0).pack(fill="x", padx=18)
    # Texto centrado
    ctk.CTkLabel(parent, text=texto, font=FONT_TITLE, text_color=color,
                 anchor="center").pack(pady=4)
    # Línea hr inferior
    ctk.CTkFrame(parent, fg_color=BORDER_ACCENT, height=1,
                 corner_radius=0).pack(fill="x", padx=18)
    # Espacio inferior
    ctk.CTkFrame(parent, fg_color="transparent", height=6).pack()


def advertencia(parent, titulo, detalle):
    """Tarjeta de advertencia roja para errores críticos (sin solución, no acotado)."""
    card = ctk.CTkFrame(parent, fg_color="#2a0a0a", corner_radius=10,
                        border_width=2, border_color=TEXT_RED)
    card.pack(fill="x", padx=18, pady=12)
    ctk.CTkLabel(card, text=titulo,
                 font=("JetBrains Mono", 15, "bold"),
                 text_color=TEXT_RED).pack(pady=(12, 4))
    ctk.CTkLabel(card, text=detalle,
                 font=FONT_SMALL, text_color=TEXT_SECONDARY).pack(pady=(0, 12))


def linea_info(parent, texto, color=TEXT_SECONDARY):
    ctk.CTkLabel(parent, text=texto, font=FONT_SMALL, text_color=color,
                 anchor="w").pack(anchor="w", padx=28, pady=1)


def badge(parent, texto, color_bg, color_fg):
    """Pequeña pastilla de color para resaltar datos clave."""
    f = ctk.CTkFrame(parent, fg_color=color_bg, corner_radius=6)
    f.pack(side="left", padx=4, pady=4)
    ctk.CTkLabel(f, text=texto, font=FONT_SMALL, text_color=color_fg,
                 padx=8, pady=2).pack()


def separador(parent):
    ctk.CTkFrame(parent, fg_color=BORDER_COLOR, height=1,
                 corner_radius=0).pack(fill="x", padx=18, pady=6)


# ── Tabla del Tableau ─────────────────────────────────────────────────
def dibujar_tabla(parent, columnas, variables_basicas, matriz,
                  fila_extra, label_extra,
                  col_pivote_idx=None, fila_pivote_idx=None):
    import tkinter as tk

    COL_W = 82
    n_cols = len(columnas) + 1

    # Contenedor externo
    outer = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=10,
                         border_width=1, border_color=BORDER_COLOR)
    outer.pack(fill="x", padx=18, pady=6)

    # Canvas con scrollbar horizontal
    canvas = tk.Canvas(outer, bg=BG_MAIN, highlightthickness=0)
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Custom.Horizontal.TScrollbar",
        background="#2a2f45",
        troughcolor="#1e2233",
        bordercolor="#1e2233",
        lightcolor="#2a2f45",
        darkcolor="#2a2f45",
        arrowcolor="#aaaaaa",
        gripcount=0,
        relief="flat",
        borderwidth=0
    )

    style.map(
        "Custom.Horizontal.TScrollbar",
        background=[
            ("active", "#4a5170"),
            ("!active", "#2a2f45")
        ]
    )

    scrollbar = ttk.Scrollbar(
        outer,
        orient="horizontal",
        command=canvas.xview,
        style="Custom.Horizontal.TScrollbar"
    )
    scrollbar.pack(side="bottom", fill="x")
    canvas.pack(side="top", fill="both", expand=True, padx=8, pady=(8, 0))
    canvas.configure(xscrollcommand=scrollbar.set)

    # Frame interno dentro del canvas
    grid_frame = ctk.CTkFrame(canvas, fg_color=BG_MAIN, corner_radius=8)
    canvas.create_window((0, 0), window=grid_frame, anchor="nw")

    def celda(frame, texto, bg, fg, font=FONT_BODY, row=0, col=0):
        f = ctk.CTkFrame(frame, fg_color=bg, corner_radius=0, border_width=0)
        f.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
        f.grid_columnconfigure(0, minsize=COL_W)
        ctk.CTkLabel(f, text=texto, font=font,
                     text_color=fg, anchor="center",
                     padx=6, pady=6).pack(fill="both", expand=True)

    total_filas = len(variables_basicas) + 2

    for r in range(total_filas):
        grid_frame.grid_rowconfigure(r, weight=1, minsize=36)
    for c in range(n_cols):
        grid_frame.grid_columnconfigure(c, weight=1, minsize=COL_W)

    # Cabecera
    celda(grid_frame, "Xb", BG_TABLE_HEAD, TEXT_HEAD, FONT_HEAD, row=0, col=0)
    for j, col in enumerate(columnas):
        bg = BG_PIVOT_COL if col_pivote_idx is not None and j == col_pivote_idx else BG_TABLE_HEAD
        fg = TEXT_GOLD if col_pivote_idx is not None and j == col_pivote_idx else TEXT_HEAD
        celda(grid_frame, col, bg, fg, FONT_HEAD, row=0, col=j + 1)

    # Filas de la matriz
    for f, vb in enumerate(variables_basicas):
        bg_row = BG_TABLE_ALT if f % 2 else BG_TABLE_ROW
        celda(grid_frame, vb, bg_row, TEXT_PURPLE, FONT_BODY, row=f + 1, col=0)
        for j in range(len(columnas)):
            es_pivot_col = col_pivote_idx is not None and j == col_pivote_idx
            es_pivot_cel = es_pivot_col and fila_pivote_idx is not None and f == fila_pivote_idx
            if es_pivot_cel:
                bg = BG_PIVOT_CELL; fg = TEXT_GOLD
            elif es_pivot_col:
                bg = BG_PIVOT_COL; fg = TEXT_PRIMARY
            else:
                bg = bg_row; fg = TEXT_PRIMARY
            celda(grid_frame, fmt(matriz[f][j]), bg, fg, FONT_BODY, row=f + 1, col=j + 1)

    # Fila W / Z
    celda(grid_frame, label_extra, BG_W_ROW, TEXT_BLUE, FONT_HEAD, row=total_filas - 1, col=0)
    for j in range(len(columnas)):
        es_pivot_col = col_pivote_idx is not None and j == col_pivote_idx
        bg = BG_PIVOT_COL if es_pivot_col else BG_W_ROW
        fg = TEXT_GOLD if es_pivot_col else TEXT_BLUE
        celda(grid_frame, fmt(fila_extra[j]), bg, fg, FONT_BODY, row=total_filas - 1, col=j + 1)

    # Actualizar scroll region y alto del canvas
    def actualizar_scroll(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.configure(height=grid_frame.winfo_reqheight() + 4)

    grid_frame.bind("<Configure>", actualizar_scroll)

    outer.update_idletasks()
    return outer


def mostrar_pivote_info(parent, col_entra, fila_sale, pivote):
    f = ctk.CTkFrame(parent, fg_color="#1c1e2e", corner_radius=8,
                     border_width=1, border_color="#3a3f5c")
    f.pack(fill="x", padx=18, pady=(2, 8))
    inner = ctk.CTkFrame(f, fg_color="transparent")
    inner.pack(pady=6, padx=12, anchor="w")
    ctk.CTkLabel(inner, text="↳  Entra: ", font=FONT_SMALL,
                 text_color=TEXT_SECONDARY).pack(side="left")
    ctk.CTkLabel(inner, text=col_entra, font=FONT_LABEL,
                 text_color=TEXT_GREEN).pack(side="left")
    ctk.CTkLabel(inner, text="   Sale: ", font=FONT_SMALL,
                 text_color=TEXT_SECONDARY).pack(side="left")
    ctk.CTkLabel(inner, text=fila_sale, font=FONT_LABEL,
                 text_color=TEXT_RED).pack(side="left")
    ctk.CTkLabel(inner, text="   Pivote: ", font=FONT_SMALL,
                 text_color=TEXT_SECONDARY).pack(side="left")
    ctk.CTkLabel(inner, text=pivote, font=FONT_LABEL,
                 text_color=TEXT_GOLD).pack(side="left")


# ── Lógica del simplex ────────────────────────────────────────────────
def calcular_fila_costos_fase1(matriz, variables_basicas, columnas, tipo_optimizacion="min"):
    fila_w = [Fraction(0)] * len(columnas)
    costo_artificial = Fraction(1) if tipo_optimizacion == "min" else Fraction(-1)
    costos_fase1 = {col: costo_artificial if col.startswith("A") else Fraction(0) for col in columnas}

    for j in range(len(columnas)):
        suma_wj = Fraction(0)
        for f, vb in enumerate(variables_basicas):
            costo_vb = costos_fase1.get(vb, Fraction(0))
            suma_wj += costo_vb * matriz[f][j]
        costo_propio = costos_fase1.get(columnas[j], Fraction(0))
        if columnas[j] == "bi":
            fila_w[j] = suma_wj
        else:
            fila_w[j] = suma_wj - costo_propio
    return fila_w


def recalcular_fila_z_fase2(matriz, variables_basicas, columnas, funcion_objetivo_original):
    fila_z = [Fraction(0)] * len(columnas)
    costos_originales = {}
    for i, col in enumerate(columnas):
        if col.startswith("X"):
            idx = int(col[1:]) - 1
            costos_originales[col] = Fraction(funcion_objetivo_original[idx])
        else:
            costos_originales[col] = Fraction(0)

    for j in range(len(columnas)):
        suma_zj = Fraction(0)
        for f, vb in enumerate(variables_basicas):
            costo_vb = costos_originales.get(vb, Fraction(0))
            suma_zj += costo_vb * matriz[f][j]
        costo_propio_cj = costos_originales.get(columnas[j], Fraction(0))
        if columnas[j] == "bi":
            fila_z[j] = suma_zj
        else:
            fila_z[j] = suma_zj - costo_propio_cj
    return fila_z


def obtener_columna_pivote(fila_costos, columnas, fase, tipo_optimizacion="max"):
    indice = None
    if fase == 1:
        if tipo_optimizacion == "min":
            mayor = Fraction(0)
            for i in range(len(fila_costos) - 1):
                if columnas[i].startswith("A"):
                    continue
                if fila_costos[i] > mayor:
                    mayor = fila_costos[i]
                    indice = i
        else:
            menor = Fraction(0)
            for i in range(len(fila_costos) - 1):
                if columnas[i].startswith("A"):
                    continue
                if fila_costos[i] < menor:
                    menor = fila_costos[i]
                    indice = i
        return indice
    else:
        if tipo_optimizacion == "max":
            menor = Fraction(0)
            for i in range(len(fila_costos) - 1):
                if fila_costos[i] < menor:
                    menor = fila_costos[i]
                    indice = i
            return indice
        else:
            mayor = Fraction(0)
            for i in range(len(fila_costos) - 1):
                if fila_costos[i] > mayor:
                    mayor = fila_costos[i]
                    indice = i
            return indice


def obtener_fila_pivote(matriz, indice_pivote):
    razones = []
    for fila in range(len(matriz)):
        coef = matriz[fila][indice_pivote]
        rhs = matriz[fila][-1]
        if coef > 0:
            razones.append((rhs / coef, fila))
    if not razones:
        return None
    return min(razones, key=lambda x: x[0])[1]


# ── Función principal ─────────────────────────────────────────────────
def metodo_dos_fases(contenedor, datos):
    for widget in contenedor.winfo_children():
        widget.destroy()

    ctk.set_appearance_mode("dark")
    contenedor.configure(fg_color=BG_MAIN)

    # El contenedor ya es CTkScrollableFrame (frame_formulario en main.py)
    # No creamos otro scroll adentro, usamos el contenedor directamente
    scroll = contenedor

    funcion_objetivo = datos["funcion_objetivo"]
    restrictions     = datos["restricciones"]
    tipo             = datos["tipo_optimizacion"].lower()

    # ── Banner principal ──────────────────────────────────────────────
    banner = ctk.CTkFrame(scroll, fg_color=BG_CARD, corner_radius=12,
                          border_width=1, border_color=BORDER_ACCENT)
    banner.pack(fill="x", padx=18, pady=(8, 4))
    ctk.CTkLabel(banner, text="MÉTODO DE DOS FASES",
                 font=("JetBrains Mono", 18, "bold"),
                 text_color=TEXT_ACCENT).pack(pady=(8, 2))
    tipo_str = "MAXIMIZACIÓN" if tipo == "max" else "MINIMIZACIÓN"
    ctk.CTkLabel(banner, text=tipo_str,
                 font=FONT_SMALL, text_color=TEXT_SECONDARY).pack(pady=(0, 12))

    # ── Modelo Original ───────────────────────────────────────────────
    seccion_titulo(scroll, "⬡  MODELO ORIGINAL", TEXT_ACCENT)

    fo_frame = ctk.CTkFrame(scroll, fg_color=BG_CARD, corner_radius=8,
                            border_width=1, border_color=BORDER_COLOR)
    fo_frame.pack(fill="x", padx=18, pady=4)

    obj_str = ("Min Z = " if tipo == "min" else "Max Z = ") + \
              " + ".join([f"{fmt(Fraction(c))}·X{i+1}" for i, c in enumerate(funcion_objetivo)])
    ctk.CTkLabel(fo_frame, text=obj_str, font=FONT_LABEL,
                 text_color=TEXT_GOLD, anchor="w").pack(anchor="w", padx=16, pady=8)

    rest_frame = ctk.CTkFrame(scroll, fg_color=BG_CARD, corner_radius=8,
                              border_width=1, border_color=BORDER_COLOR)
    rest_frame.pack(fill="x", padx=18, pady=4)
    ctk.CTkLabel(rest_frame, text="Restricciones:", font=FONT_HEAD,
                 text_color=TEXT_HEAD, anchor="w").pack(anchor="w", padx=16, pady=(8, 2))
    for i, r in enumerate(restrictions):
        exp = " + ".join([f"{fmt(Fraction(c))}·X{j+1}" for j, c in enumerate(r["coeficientes"])])
        ctk.CTkLabel(rest_frame,
                     text=f"  R{i+1}:  {exp}  {r['simbolo']}  {fmt(Fraction(r['resultado']))}",
                     font=FONT_BODY, text_color=TEXT_PRIMARY, anchor="w"
                     ).pack(anchor="w", padx=16, pady=2)
    nn = ", ".join([f"X{i+1}" for i in range(len(funcion_objetivo))]) + " ≥ 0"
    ctk.CTkLabel(rest_frame, text=f"  No negatividad:  {nn}",
                 font=FONT_SMALL, text_color=TEXT_SECONDARY, anchor="w"
                 ).pack(anchor="w", padx=16, pady=(2, 8))

    # ── Forma Estándar ────────────────────────────────────────────────
    seccion_titulo(scroll, "⬡  FORMA ESTÁNDAR", "#7eb8f7")

    contador_a = 1
    variables_basicas = []
    holguras, excesos, artificiales = [], [], []

    est_frame = ctk.CTkFrame(scroll, fg_color=BG_CARD, corner_radius=8,
                             border_width=1, border_color=BORDER_COLOR)
    est_frame.pack(fill="x", padx=18, pady=4)

    for i, r in enumerate(restrictions):
        num = i + 1
        partes = [f"{fmt(Fraction(c))}·X{j+1}" for j, c in enumerate(r["coeficientes"]) if c != 0]
        if r["simbolo"] == "<=":
            nom = f"S{num}"; holguras.append(nom)
            partes.append(f"+ {nom}"); variables_basicas.append(nom)
        elif r["simbolo"] == ">=":
            nom_e = f"E{num}"; nom_a = f"A{contador_a}"
            excesos.append(nom_e); artificiales.append(nom_a)
            partes.append(f"- {nom_e}"); partes.append(f"+ {nom_a}")
            variables_basicas.append(nom_a); contador_a += 1
        elif r["simbolo"] == "=":
            nom_a = f"A{contador_a}"; artificiales.append(nom_a)
            partes.append(f"+ {nom_a}"); variables_basicas.append(nom_a); contador_a += 1
        expr = "  ".join(partes)
        ctk.CTkLabel(est_frame,
                     text=f"  R{num}:  {expr}  =  {fmt(Fraction(r['resultado']))}",
                     font=FONT_BODY, text_color=TEXT_PRIMARY, anchor="w"
                     ).pack(anchor="w", padx=16, pady=3)

    holguras.sort(key=lambda x: int(x[1:]))
    excesos.sort(key=lambda x: int(x[1:]))
    artificiales.sort(key=lambda x: int(x[1:]))

    badge_frame = ctk.CTkFrame(scroll, fg_color="transparent")
    badge_frame.pack(anchor="w", padx=18, pady=6)
    if holguras:
        badge(badge_frame, f"Holguras: {len(holguras)}", "#1a2a1a", TEXT_GREEN)
    if excesos:
        badge(badge_frame, f"Excesos: {len(excesos)}", "#1a1a2e", TEXT_BLUE)
    if artificiales:
        badge(badge_frame, f"Artificiales: {len(artificiales)}", "#2a1a1a", TEXT_RED)

    columnas = [f"X{i+1}" for i in range(len(funcion_objetivo))] + \
               holguras + excesos + artificiales + ["bi"]

    # Construcción de la matriz
    matriz = []
    for i, r in enumerate(restrictions):
        num = i + 1
        fila = [Fraction(0)] * len(columnas)
        for j, coef in enumerate(r["coeficientes"]):
            fila[j] = Fraction(coef)
        if r["simbolo"] == "<=":
            fila[columnas.index(f"S{num}")] = Fraction(1)
        elif r["simbolo"] == ">=":
            fila[columnas.index(f"E{num}")] = Fraction(-1)
        vb_fila = variables_basicas[i]
        fila[columnas.index(vb_fila)] = Fraction(1)
        fila[-1] = Fraction(r["resultado"])
        matriz.append(fila)

    # ── FASE I ────────────────────────────────────────────────────────
    seccion_titulo(scroll, "◈  FASE I — Minimizar variables artificiales", TEXT_RED)

    iteracion = 1
    max_iter  = 30

    while iteracion <= max_iter:
        fila_w = calcular_fila_costos_fase1(matriz, variables_basicas, columnas, tipo)
        indice_pivote = obtener_columna_pivote(fila_w, columnas, fase=1, tipo_optimizacion=tipo)

        # Determinar si hay pivote en esta iteración
        hay_pivote = indice_pivote is not None
        if hay_pivote and indice_pivote is not None:
            if tipo == "min" and fila_w[indice_pivote] <= 0:
                hay_pivote = False
            if tipo == "max" and fila_w[indice_pivote] >= 0:
                hay_pivote = False

        fila_pivote_idx = obtener_fila_pivote(matriz, indice_pivote) if hay_pivote else None

        # Etiqueta de iteración
        iter_label = ctk.CTkFrame(scroll, fg_color="transparent")
        iter_label.pack(anchor="w", padx=18, pady=(10, 2))
        ctk.CTkLabel(iter_label,
                     text=f"  Iteración {iteracion}  —  Fase I",
                     font=FONT_HEAD, text_color=TEXT_SECONDARY).pack(side="left")

        dibujar_tabla(scroll, columnas, variables_basicas, matriz,
                      fila_w, "Zj-Cj",
                      col_pivote_idx=indice_pivote if hay_pivote else None,
                      fila_pivote_idx=fila_pivote_idx)

        if not hay_pivote:
            break
        if indice_pivote is None:
            break
        columna_pivote = columnas[indice_pivote]
        if fila_pivote_idx is None:
            advertencia(scroll,
                        "⚠  SIN SOLUCIÓN FACTIBLE",
                        "No existe ningún punto que satisfaga simultáneamente\n"
                        "todas las restricciones y la condición de no negatividad.")
            return

        elem_pivote = matriz[fila_pivote_idx][indice_pivote]
        mostrar_pivote_info(scroll, columna_pivote,
                            variables_basicas[fila_pivote_idx], fmt(elem_pivote))

        # Pivotear
        matriz[fila_pivote_idx] = [v / elem_pivote for v in matriz[fila_pivote_idx]]
        for f in range(len(matriz)):
            if f != fila_pivote_idx:
                factor = matriz[f][indice_pivote]
                matriz[f] = [matriz[f][j] - factor * matriz[fila_pivote_idx][j]
                             for j in range(len(matriz[f]))]
        variables_basicas[fila_pivote_idx] = columna_pivote
        iteracion += 1

    # Verificar factibilidad
    fila_w = calcular_fila_costos_fase1(matriz, variables_basicas, columnas, tipo)
    infactible = (tipo == "min" and fila_w[-1] > Fraction(0)) or \
                 (tipo == "max" and fila_w[-1] < Fraction(0))
    if infactible:
        advertencia(scroll,
                    "⚠  SIN SOLUCIÓN FACTIBLE",
                    "No existe ningún punto que satisfaga simultáneamente\n"
                    "todas las restricciones y la condición de no negatividad.")
        return

    # ── FASE II ───────────────────────────────────────────────────────
    seccion_titulo(scroll, "◈  FASE II — Optimización", TEXT_GREEN)

    nota = ctk.CTkFrame(scroll, fg_color=BG_CARD, corner_radius=8,
                        border_width=1, border_color=BORDER_COLOR)
    nota.pack(fill="x", padx=18, pady=4)
    ctk.CTkLabel(nota, text="  Se eliminan las columnas artificiales del tableau.",
                 font=FONT_SMALL, text_color=TEXT_SECONDARY, anchor="w"
                 ).pack(anchor="w", padx=8, pady=8)

    indices_a = [i for i, col in enumerate(columnas) if col.startswith("A")]
    for idx in reversed(indices_a):
        columnas.pop(idx)
        for fila in matriz:
            fila.pop(idx)

    iteracion_f2 = 1
    fila_z = None

    while iteracion_f2 <= max_iter:
        fila_z = recalcular_fila_z_fase2(matriz, variables_basicas, columnas, funcion_objetivo)
        indice_pivote = obtener_columna_pivote(fila_z, columnas, fase=2, tipo_optimizacion=tipo)

        hay_pivote = indice_pivote is not None
        if hay_pivote and indice_pivote is not None:
            if tipo == "min" and fila_z[indice_pivote] <= 0:
                hay_pivote = False
            if tipo == "max" and fila_z[indice_pivote] >= 0:
                hay_pivote = False

        fila_pivote_idx = obtener_fila_pivote(matriz, indice_pivote) if hay_pivote else None

        iter_label = ctk.CTkFrame(scroll, fg_color="transparent")
        iter_label.pack(anchor="w", padx=18, pady=(10, 2))
        ctk.CTkLabel(iter_label,
                     text=f"  Iteración {iteracion_f2}  —  Fase II",
                     font=FONT_HEAD, text_color=TEXT_SECONDARY).pack(side="left")

        dibujar_tabla(scroll, columnas, variables_basicas, matriz,
                      fila_z, "Zj-Cj",
                      col_pivote_idx=indice_pivote if hay_pivote else None,
                      fila_pivote_idx=fila_pivote_idx)

        if not hay_pivote:
            optimo = ctk.CTkLabel(scroll,
                                  text="✓  Criterio de optimalidad alcanzado.",
                                  font=FONT_LABEL, text_color=TEXT_GREEN)
            optimo.pack(padx=18, pady=6, anchor="w")
            break

        if indice_pivote is None:
            break
        columna_pivote = columnas[indice_pivote]
        if fila_pivote_idx is None:
            advertencia(scroll,
                        "⚠  SOLUCIÓN NO ACOTADA",
                        "La región factible es ilimitada en la dirección de optimización.\n"
                        "El problema no tiene solución óptima finita.")
            return

        elem_pivote = matriz[fila_pivote_idx][indice_pivote]
        mostrar_pivote_info(scroll, columna_pivote,
                            variables_basicas[fila_pivote_idx], fmt(elem_pivote))

        matriz[fila_pivote_idx] = [v / elem_pivote for v in matriz[fila_pivote_idx]]
        for f in range(len(matriz)):
            if f != fila_pivote_idx:
                factor = matriz[f][indice_pivote]
                matriz[f] = [matriz[f][j] - factor * matriz[fila_pivote_idx][j]
                             for j in range(len(matriz[f]))]
        variables_basicas[fila_pivote_idx] = columna_pivote
        iteracion_f2 += 1

    # ── SOLUCIÓN ÓPTIMA ───────────────────────────────────────────────
    seccion_titulo(scroll, "★  SOLUCIÓN ÓPTIMA", TEXT_GOLD)

    res_frame = ctk.CTkFrame(scroll, fg_color=BG_RESULT, corner_radius=12,
                             border_width=1, border_color="#2d4a1e")
    res_frame.pack(fill="x", padx=18, pady=8)

    valores_finales = {f"X{i+1}": Fraction(0) for i in range(len(funcion_objetivo))}
    for f, vb in enumerate(variables_basicas):
        if vb in valores_finales:
            valores_finales[vb] = matriz[f][-1]

    vars_row = ctk.CTkFrame(res_frame, fg_color="transparent")
    vars_row.pack(pady=(14, 6), padx=16, anchor="w")
    for var, val in valores_finales.items():
        vf = ctk.CTkFrame(vars_row, fg_color="#1a2a1a", corner_radius=8,
                          border_width=1, border_color="#2d4a1e")
        vf.pack(side="left", padx=6, pady=4)
        ctk.CTkLabel(vf, text=f"  {var} = {fmt(val)}  ",
                     font=FONT_RESULT, text_color=TEXT_GREEN,
                     padx=4, pady=6).pack()

    separador(res_frame)

    z_val = fila_z[-1] if fila_z else Fraction(0)
    z_frame = ctk.CTkFrame(res_frame, fg_color="transparent")
    z_frame.pack(pady=(4, 14), padx=16, anchor="w")
    ctk.CTkLabel(z_frame, text="Valor óptimo  ",
                 font=FONT_HEAD, text_color=TEXT_SECONDARY).pack(side="left")
    ctk.CTkLabel(z_frame, text=f"Z = {fmt(z_val)}",
                 font=("JetBrains Mono", 16, "bold"),
                 text_color=TEXT_GOLD).pack(side="left")