# ======================================
# MÉTODO GRÁFICO - VISUAL DARK MODE
# ======================================

from itertools import combinations

import customtkinter as ctk
import numpy as np
from scipy.spatial import ConvexHull
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches

# ── Paleta de colores (igual que dos fases) ───────────────────────────
BG_MAIN       = "#0f1117"
BG_CARD       = "#1a1d27"
BG_TABLE_HEAD = "#1e2235"
BG_TABLE_ROW  = "#151825"
BG_TABLE_ALT  = "#191c2a"
BG_RESULT     = "#0d1f0d"

TEXT_PRIMARY   = "#e8eaf0"
TEXT_SECONDARY = "#8b92a8"
TEXT_ACCENT    = "#64d8cb"
TEXT_GOLD      = "#ffd166"
TEXT_GREEN     = "#6fcf97"
TEXT_RED       = "#eb5757"
TEXT_BLUE      = "#7eb8f7"
TEXT_HEAD      = "#a8b4cc"

BORDER_COLOR  = "#2a2f45"
BORDER_ACCENT = "#3d4a6b"

FONT_TITLE  = ("JetBrains Mono", 15, "bold")
FONT_HEAD   = ("JetBrains Mono", 12, "bold")
FONT_BODY   = ("JetBrains Mono", 12)
FONT_SMALL  = ("JetBrains Mono", 11)
FONT_LABEL  = ("JetBrains Mono", 13, "bold")
FONT_RESULT = ("JetBrains Mono", 14, "bold")

# Colores de matplotlib para la gráfica (dark mode)
MPL_BG        = "#0f1117"
MPL_AX_BG     = "#1a1d27"
MPL_GRID      = "#2a2f45"
MPL_TEXT      = "#a8b4cc"
MPL_OPTIMO    = "#ffd166"
MPL_REGION    = "#64d8cb"
MPL_COLORES   = ["#7eb8f7", "#6fcf97", "#c084fc", "#eb5757",
                 "#ffd166", "#64d8cb", "#f97316", "#a78bfa"]


# ── Helpers visuales (mismos que dos fases) ───────────────────────────
def seccion_titulo(parent, texto, color=TEXT_ACCENT):
    """Línea separadora con texto centrado, sin contenedor propio."""
    ctk.CTkFrame(parent, fg_color="transparent", height=10).pack()
    ctk.CTkFrame(parent, fg_color=BORDER_ACCENT, height=1,
                 corner_radius=0).pack(fill="x", padx=18)
    ctk.CTkLabel(parent, text=texto, font=FONT_TITLE, text_color=color,
                 anchor="center").pack(pady=4)
    ctk.CTkFrame(parent, fg_color=BORDER_ACCENT, height=1,
                 corner_radius=0).pack(fill="x", padx=18)
    ctk.CTkFrame(parent, fg_color="transparent", height=6).pack()


def separador(parent):
    ctk.CTkFrame(parent, fg_color=BORDER_COLOR, height=1,
                 corner_radius=0).pack(fill="x", padx=18, pady=6)


def badge(parent, texto, color_bg, color_fg):
    """Pastilla de color para resaltar datos clave."""
    f = ctk.CTkFrame(parent, fg_color=color_bg, corner_radius=6)
    f.pack(side="left", padx=4, pady=4)
    ctk.CTkLabel(f, text=texto, font=FONT_SMALL, text_color=color_fg,
                 padx=8, pady=2).pack()


def tarjeta(parent, fill="x", pady=4):
    """Frame con estilo de tarjeta oscura."""
    f = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=8,
                     border_width=1, border_color=BORDER_COLOR)
    f.pack(fill=fill, padx=18, pady=pady)
    return f


def fila_dato(parent, etiqueta, valor, color_val=TEXT_PRIMARY):
    """Fila con etiqueta y valor en la misma línea."""
    f = ctk.CTkFrame(parent, fg_color="transparent")
    f.pack(anchor="w", padx=16, pady=2)
    ctk.CTkLabel(f, text=etiqueta, font=FONT_SMALL,
                 text_color=TEXT_SECONDARY).pack(side="left")
    ctk.CTkLabel(f, text=valor, font=FONT_LABEL,
                 text_color=color_val).pack(side="left", padx=6)


# ── Helpers del método ────────────────────────────────────────────────
def fmt(valor):
    """Formatea entero o decimal a 2 cifras."""
    return f"{int(valor)}" if float(valor).is_integer() else f"{valor:.2f}"


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
            # Restricción de igualdad: el punto DEBE estar exactamente sobre la recta
            if abs(resultados[i] - B[i]) > 1e-9:
                return False
    return all(punto >= -1e-9)


# ── Función principal ─────────────────────────────────────────────────
def metodo_grafico(contenedor, datos):
    # ======================================
    # LIMPIAR CONTENEDOR
    # ======================================
    for widget in contenedor.winfo_children():
        widget.destroy()

    contenedor.configure(fg_color=BG_MAIN)

    c = datos.get("funcion_objetivo")
    r = datos.get("restricciones")
    tipo_opt = datos.get("tipo_optimizacion", "max")

    # ======================================
    # EXTRAER DATOS DE RESTRICCIONES
    # ======================================
    coheficientes = []
    resultado     = []
    signos        = []

    for restricciones in r:
        coheficientes.append(restricciones['coeficientes'])
        resultado.append(restricciones['resultado'])
        signos.append(restricciones['simbolo'])

    A = np.array(coheficientes)
    B = np.array(resultado)
    S = np.array(signos)
    n_restricciones = len(A)

    # ── Banner ────────────────────────────────────────────────────────
    banner = ctk.CTkFrame(contenedor, fg_color=BG_CARD, corner_radius=12,
                          border_width=1, border_color=BORDER_ACCENT)
    banner.pack(fill="x", padx=18, pady=(8, 4))
    ctk.CTkLabel(banner, text="MÉTODO GRÁFICO",
                 font=("JetBrains Mono", 18, "bold"),
                 text_color=TEXT_ACCENT).pack(pady=(8, 2))
    tipo_str = "MAXIMIZACIÓN" if tipo_opt == "max" else "MINIMIZACIÓN"
    ctk.CTkLabel(banner, text=tipo_str,
                 font=FONT_SMALL, text_color=TEXT_SECONDARY).pack(pady=(0, 8))

    # ── Modelo original ───────────────────────────────────────────────
    seccion_titulo(contenedor, "⬡  MODELO ORIGINAL", TEXT_ACCENT)

    fo_card = tarjeta(contenedor)
    obj_str = ("Min Z = " if tipo_opt == "min" else "Max Z = ") + \
              " + ".join([f"{fmt(c[i])}·X{i+1}" for i in range(len(c))])
    ctk.CTkLabel(fo_card, text=obj_str, font=FONT_LABEL,
                 text_color=TEXT_GOLD, anchor="w").pack(anchor="w", padx=16, pady=8)

    rest_card = tarjeta(contenedor)
    ctk.CTkLabel(rest_card, text="Restricciones:", font=FONT_HEAD,
                 text_color=TEXT_HEAD, anchor="w").pack(anchor="w", padx=16, pady=(8, 2))
    for i in range(n_restricciones):
        exp = " + ".join([f"{fmt(A[i][j])}·X{j+1}" for j in range(len(A[i]))])
        ctk.CTkLabel(rest_card,
                     text=f"  R{i+1}:  {exp}  {S[i]}  {fmt(B[i])}",
                     font=FONT_BODY, text_color=TEXT_PRIMARY, anchor="w"
                     ).pack(anchor="w", padx=16, pady=2)
    ctk.CTkLabel(rest_card, text="  No negatividad:  X1, X2 ≥ 0",
                 font=FONT_SMALL, text_color=TEXT_SECONDARY, anchor="w"
                 ).pack(anchor="w", padx=16, pady=(2, 8))

    # ======================================
    # GUARDAR VÉRTICES
    # ======================================
    vertices = []
    parejas = combinations(range(n_restricciones), 2)

    # ── Sección análisis de restricciones ─────────────────────────────
    seccion_titulo(contenedor, "⬡  ANÁLISIS DE RESTRICCIONES", TEXT_BLUE)

    #------------------------------------------------------------------------
    # Intersección de cada par de restricciones
    for i, j in combinations(range(n_restricciones), 2):
        A_temp = np.array([A[i], A[j]])
        B_temp = np.array([B[i], B[j]])
        try:
            punto = np.linalg.solve(A_temp, B_temp)
            if es_factible(A, B, S, punto):
                vertices.append(punto)
        except np.linalg.LinAlgError:
            continue

    #------------------------------------------------------------------
    # Intersecciones con los ejes y análisis por restricción
    for i in range(n_restricciones):
        r_card = tarjeta(contenedor, pady=3)

        # Encabezado de la restricción con badge de tipo
        enc = ctk.CTkFrame(r_card, fg_color="transparent")
        enc.pack(anchor="w", padx=16, pady=(8, 4))

        exp = " + ".join([f"{fmt(A[i][j])}·X{j+1}" for j in range(len(A[i]))])
        ctk.CTkLabel(enc, text=f"R{i+1}:  {exp}  {S[i]}  {fmt(B[i])}",
                     font=FONT_HEAD, text_color=TEXT_PRIMARY).pack(side="left")

        # Badge con tipo de restricción
        color_badge = {"<=": ("#1a2a1a", TEXT_GREEN),
                       ">=": ("#1a1a2e", TEXT_BLUE),
                       "=":  ("#2a1a1a", TEXT_GOLD)}.get(S[i], (BG_CARD, TEXT_PRIMARY))
        ctk.CTkFrame(enc, fg_color=color_badge[0], corner_radius=6,
                     width=2, height=2).pack(side="left", padx=8)
        ctk.CTkLabel(enc, text=S[i], font=FONT_SMALL,
                     text_color=color_badge[1]).pack(side="left")

        # X1 = 0, despeja X2
        if A[i][1] != 0:
            val = B[i] / A[i][1]
            punto = np.array([0.0, val])
            factible = es_factible(A, B, S, punto)
            icono = "✔" if factible else "✘"
            color_ic = TEXT_GREEN if factible else TEXT_RED
            ctk.CTkLabel(r_card,
                         text=f"  {icono}  X₁=0 → X₂={fmt(val)}   Punto: (0, {fmt(val)})",
                         font=FONT_SMALL, text_color=color_ic, anchor="w"
                         ).pack(anchor="w", padx=24, pady=1)
            if factible:
                vertices.append(punto)

        # X2 = 0, despeja X1
        if A[i][0] != 0:
            val = B[i] / A[i][0]
            punto = np.array([val, 0.0])
            factible = es_factible(A, B, S, punto)
            icono = "✔" if factible else "✘"
            color_ic = TEXT_GREEN if factible else TEXT_RED
            ctk.CTkLabel(r_card,
                         text=f"  {icono}  X₂=0 → X₁={fmt(val)}   Punto: ({fmt(val)}, 0)",
                         font=FONT_SMALL, text_color=color_ic, anchor="w"
                         ).pack(anchor="w", padx=24, pady=(1, 8))
            if factible:
                vertices.append(punto)

    # El origen
    origen = np.array([0.0, 0.0])
    orig_card = tarjeta(contenedor, pady=3)
    if es_factible(A, B, S, origen):
        vertices.append(origen)
        ctk.CTkLabel(orig_card,
                     text="  ✔  El origen (0, 0) es factible → agregado como vértice",
                     font=FONT_SMALL, text_color=TEXT_GREEN, anchor="w"
                     ).pack(anchor="w", padx=16, pady=8)
    else:
        ctk.CTkLabel(orig_card,
                     text="  ✘  El origen (0, 0) no es factible → descartado",
                     font=FONT_SMALL, text_color=TEXT_RED, anchor="w"
                     ).pack(anchor="w", padx=16, pady=8)

    # ======================================
    # VERIFICAR SI HAY SOLUCIÓN FACTIBLE
    # Advertencia cuando no hay vértices suficientes para formar región
    # ======================================
    puntos_unicos = []
    for p in vertices:
        es_duplicado = False
        for q in puntos_unicos:
            if np.linalg.norm(p - q) < 1e-6:
                es_duplicado = True
                break
        if not es_duplicado:
            puntos_unicos.append(p)

    if len(puntos_unicos) < 2:
        # No hay suficientes vértices → sin solución factible
        warn_card = ctk.CTkFrame(contenedor, fg_color="#2a0a0a", corner_radius=10,
                                 border_width=2, border_color=TEXT_RED)
        warn_card.pack(fill="x", padx=18, pady=12)
        ctk.CTkLabel(warn_card,
                     text="⚠  SIN SOLUCIÓN FACTIBLE",
                     font=("JetBrains Mono", 15, "bold"),
                     text_color=TEXT_RED).pack(pady=(12, 4))
        ctk.CTkLabel(warn_card,
                     text="No existe ningún punto que satisfaga simultáneamente\n"
                          "todas las restricciones y la condición de no negatividad.",
                     font=FONT_SMALL, text_color=TEXT_SECONDARY).pack(pady=(0, 12))
        return

    vertices = puntos_unicos

    # ======================================
    # EVALUACIÓN DE LA FUNCIÓN OBJETIVO
    # ======================================
    seccion_titulo(contenedor, "⬡  EVALUACIÓN DE LA FUNCIÓN OBJETIVO", TEXT_GOLD)

    resultados = []
    eval_card = tarjeta(contenedor)
    ctk.CTkLabel(eval_card, text="Vértices de la región factible:",
                 font=FONT_HEAD, text_color=TEXT_HEAD, anchor="w"
                 ).pack(anchor="w", padx=16, pady=(8, 4))

    for i, punto in enumerate(vertices):
        z = np.dot(c, punto)
        resultados.append((punto, z))
        fila = ctk.CTkFrame(eval_card, fg_color=BG_TABLE_ALT if i % 2 else BG_TABLE_ROW,
                            corner_radius=6)
        fila.pack(fill="x", padx=12, pady=2)
        ctk.CTkLabel(fila, text=f"  V{i+1}  ({fmt(punto[0])}, {fmt(punto[1])})",
                     font=FONT_BODY, text_color=TEXT_PRIMARY, anchor="w",
                     width=260).pack(side="left", padx=8, pady=6)
        ctk.CTkLabel(fila, text=f"Z  =  {fmt(z)}",
                     font=FONT_LABEL, text_color=TEXT_BLUE, anchor="w"
                     ).pack(side="left", padx=8)

    ctk.CTkFrame(eval_card, fg_color="transparent", height=6).pack()

    # ── Resultado óptimo ──────────────────────────────────────────────
    if tipo_opt == "max":
        punto_optimo, valor_optimo = max(resultados, key=lambda x: x[1])
    else:
        punto_optimo, valor_optimo = min(resultados, key=lambda x: x[1])

    seccion_titulo(contenedor, "★  SOLUCIÓN ÓPTIMA", TEXT_GOLD)

    res_frame = ctk.CTkFrame(contenedor, fg_color=BG_RESULT, corner_radius=12,
                             border_width=1, border_color="#2d4a1e")
    res_frame.pack(fill="x", padx=18, pady=8)

    vars_row = ctk.CTkFrame(res_frame, fg_color="transparent")
    vars_row.pack(pady=(14, 6), padx=16, anchor="w")

    for i in range(len(c)):
        vf = ctk.CTkFrame(vars_row, fg_color="#1a2a1a", corner_radius=8,
                          border_width=1, border_color="#2d4a1e")
        vf.pack(side="left", padx=6, pady=4)
        ctk.CTkLabel(vf, text=f"  X{i+1} = {fmt(punto_optimo[i])}  ",
                     font=FONT_RESULT, text_color=TEXT_GREEN, padx=4, pady=6).pack()

    separador(res_frame)

    z_row = ctk.CTkFrame(res_frame, fg_color="transparent")
    z_row.pack(pady=(4, 14), padx=16, anchor="w")
    ctk.CTkLabel(z_row, text="Valor óptimo  ",
                 font=FONT_HEAD, text_color=TEXT_SECONDARY).pack(side="left")
    ctk.CTkLabel(z_row, text=f"Z = {fmt(valor_optimo)}",
                 font=("JetBrains Mono", 16, "bold"),
                 text_color=TEXT_GOLD).pack(side="left")

    # ======================================
    # GRÁFICA — DARK MODE
    # ======================================
    seccion_titulo(contenedor, "⬡  GRÁFICA DE LA REGIÓN FACTIBLE", TEXT_ACCENT)

    grafica_card = ctk.CTkFrame(contenedor, fg_color=BG_CARD, corner_radius=10,
                                border_width=1, border_color=BORDER_COLOR)
    grafica_card.pack(fill="x", padx=18, pady=6)

    figura = Figure(figsize=(8, 5), facecolor=MPL_BG)
    ax = figura.add_subplot(111)
    ax.set_facecolor(MPL_AX_BG)

    # Estilo dark en todos los elementos del eje
    ax.tick_params(colors=MPL_TEXT)
    ax.xaxis.label.set_color(MPL_TEXT)
    ax.yaxis.label.set_color(MPL_TEXT)
    for spine in ax.spines.values():
        spine.set_edgecolor(MPL_GRID)
    ax.grid(True, color=MPL_GRID, linewidth=0.7, linestyle="--")
    ax.set_xlabel("X₁", color=MPL_TEXT, fontsize=11)
    ax.set_ylabel("X₂", color=MPL_TEXT, fontsize=11)

    # Calcular rango del gráfico con un margen generoso
    todos_x = [p[0] for p in vertices] + [0]
    todos_y = [p[1] for p in vertices] + [0]
    max_x = max(todos_x) * 1.35 + 1
    max_y = max(todos_y) * 1.35 + 1
    x_range = np.linspace(0, max_x, 400)

    #------------------------------------------------------------------------------------
    # Dibujar líneas de restricciones
    for i in range(n_restricciones):
        color = MPL_COLORES[i % len(MPL_COLORES)]

        # Caso normal: ambos coeficientes distintos de 0
        if A[i][0] != 0 and A[i][1] != 0:
            # Despejamos X2 en función de X1: X2 = (B - A0*X1) / A1
            y_vals = (B[i] - A[i][0] * x_range) / A[i][1]
            ax.plot(x_range, y_vals, color=color, linewidth=1.8,
                    label=f"R{i+1}: {fmt(A[i][0])}X₁ + {fmt(A[i][1])}X₂ {S[i]} {fmt(B[i])}")

        # Caso horizontal: solo X2 aparece (X1=0 en coeficiente)
        elif A[i][0] == 0 and A[i][1] != 0:
            x2_val = B[i] / A[i][1]
            ax.axhline(y=x2_val, color=color, linewidth=1.8,
                       label=f"R{i+1}: X₂ {S[i]} {fmt(x2_val)}")

        # Caso vertical: solo X1 aparece (X2=0 en coeficiente)
        elif A[i][1] == 0 and A[i][0] != 0:
            x1_val = B[i] / A[i][0]
            ax.axvline(x=x1_val, color=color, linewidth=1.8,
                       label=f"R{i+1}: X₁ {S[i]} {fmt(x1_val)}")

        # Restricción de igualdad: se resalta con línea punteada más gruesa
        # Es una recta que reduce drasticamente la región factible
        if S[i] == "=":
            # Re-dibujar encima con estilo especial para destacar que es igualdad
            if A[i][0] != 0 and A[i][1] != 0:
                y_vals = (B[i] - A[i][0] * x_range) / A[i][1]
                ax.plot(x_range, y_vals, color=TEXT_GOLD, linewidth=2.5,
                        linestyle="--", zorder=5)
            elif A[i][0] == 0 and A[i][1] != 0:
                ax.axhline(y=B[i]/A[i][1], color=TEXT_GOLD,
                           linewidth=2.5, linestyle="--", zorder=5)
            elif A[i][1] == 0 and A[i][0] != 0:
                ax.axvline(x=B[i]/A[i][0], color=TEXT_GOLD,
                           linewidth=2.5, linestyle="--", zorder=5)

    # Dibujar región factible (solo si hay suficientes puntos para ConvexHull)
    puntos_np = np.array(vertices)
    if len(puntos_np) >= 3:
        try:
            hull = ConvexHull(puntos_np)
            ax.fill(puntos_np[hull.vertices, 0], puntos_np[hull.vertices, 1],
                    alpha=0.18, color=MPL_REGION, zorder=1)
            # Borde de la región
            hull_pts = np.append(hull.vertices, hull.vertices[0])
            ax.plot(puntos_np[hull_pts, 0], puntos_np[hull_pts, 1],
                    color=MPL_REGION, linewidth=1, alpha=0.5, zorder=2)
        except Exception:
            pass
    elif len(puntos_np) == 2:
        # Cuando la región es una línea (caso restricción de igualdad)
        ax.plot(puntos_np[:, 0], puntos_np[:, 1],
                color=MPL_REGION, linewidth=3, alpha=0.5, zorder=2)

    # Marcar los vértices
    for i, punto in enumerate(vertices):
        es_optimo = np.allclose(punto, punto_optimo, atol=1e-6)
        color_pt  = MPL_OPTIMO if es_optimo else "#ffffff"
        size_pt   = 10 if es_optimo else 6
        ax.plot(punto[0], punto[1], "o", color=color_pt,
                markersize=size_pt, zorder=6)
        ax.annotate(
            f"V{i+1}({fmt(punto[0])}, {fmt(punto[1])})",
            xy=(punto[0], punto[1]),
            xytext=(6, 6),
            textcoords="offset points",
            fontsize=8,
            color=MPL_OPTIMO if es_optimo else MPL_TEXT
        )

    # Marcar el punto óptimo con estrella destacada
    ax.plot(punto_optimo[0], punto_optimo[1], "*",
            color=MPL_OPTIMO, markersize=18, zorder=7,
            label=f"Óptimo: Z={fmt(valor_optimo)}")
    ax.annotate(
        f"ÓPTIMO\nZ = {fmt(valor_optimo)}",
        xy=(punto_optimo[0], punto_optimo[1]),
        xytext=(12, 12),
        textcoords="offset points",
        fontsize=9,
        color=MPL_OPTIMO,
        fontweight="bold"
    )

    ax.set_xlim(left=0, right=max_x)
    ax.set_ylim(bottom=0, top=max_y)

    leg = ax.legend(loc="upper right", facecolor=BG_CARD,
                    edgecolor=BORDER_ACCENT, labelcolor=MPL_TEXT,
                    fontsize=8)

    figura.tight_layout()

    canvas = FigureCanvasTkAgg(figura, master=grafica_card)
    canvas.draw()
    canvas.get_tk_widget().configure(bg=MPL_BG)
    canvas.get_tk_widget().pack(padx=12, pady=12, fill="x")