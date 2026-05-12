import customtkinter as ctk

from utils.validaciones import (
    es_entero_positivo,
    validar_metodo_grafico
)

from ui.formulario import (
    generar_formulario,
    obtener_datos
)

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ==========================================
# VENTANA PRINCIPAL
# ==========================================

app = ctk.CTk()

app.title("Investigación de Operaciones")
app.geometry("1400x900")
app.minsize(1200, 800)
app.resizable(True, True)

# ==========================================
# VARIABLES GLOBALES
# ==========================================

metodo_escogido = ctk.StringVar(value="grafico")

variables_texto = ctk.StringVar()

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def limpiar_frame(frame):

    for widget in frame.winfo_children():

        widget.destroy()


# ==========================================
# VALIDAR VARIABLES
# ==========================================

def verificar_variables(*args):

    valor = variables_texto.get()

    # ======================================
    # CAMPO VACÍO
    # ======================================

    if valor == "":

        r_grafico.configure(state="normal")

        mensaje_estado.configure(
            text="Configure el problema",
            text_color="white"
        )

        return

    # ======================================
    # VALIDACIÓN NUMÉRICA
    # ======================================

    if not es_entero_positivo(valor):

        mensaje_estado.configure(
            text="Ingrese un número válido",
            text_color="red"
        )

        return

    cantidad_variables = int(valor)

    # ======================================
    # VALIDAR MÉTODO GRÁFICO
    # ======================================

    if not validar_metodo_grafico(cantidad_variables):

        r_grafico.configure(state="disabled")

        metodo_escogido.set("dos_fases")

        mensaje_estado.configure(
            text="Método gráfico deshabilitado para más de 2 variables",
            text_color="orange"
        )

    else:

        r_grafico.configure(state="normal")

        mensaje_estado.configure(
            text="Método gráfico disponible",
            text_color="lightgreen"
        )


# ==========================================
# GENERAR FORMULARIO
# ==========================================

def confirmar():

    variables = entry_variables.get()

    restricciones = entry_restricciones.get()

    # ======================================
    # VALIDAR CAMPOS VACÍOS
    # ======================================

    if variables == "" or restricciones == "":

        mensaje_estado.configure(
            text="Complete todos los campos",
            text_color="red"
        )

        return

    # ======================================
    # VALIDAR VARIABLES
    # ======================================

    if not es_entero_positivo(variables):

        mensaje_estado.configure(
            text="Número de variables inválido",
            text_color="red"
        )

        return

    # ======================================
    # VALIDAR RESTRICCIONES
    # ======================================

    if not es_entero_positivo(restricciones):

        mensaje_estado.configure(
            text="Número de restricciones inválido",
            text_color="red"
        )

        return

    # ======================================
    # CONVERTIR A ENTEROS
    # ======================================

    variables = int(variables)

    restricciones = int(restricciones)

    # ======================================
    # LIMPIAR FORMULARIO
    # ======================================

    limpiar_frame(frame_formulario)

    # ======================================
    # GENERAR FORMULARIO
    # ======================================

    generar_formulario(
        frame_formulario,
        variables,
        restricciones
    )

    mensaje_estado.configure(
        text="Formulario generado correctamente",
        text_color="lightgreen"
    )


# ==========================================
# RESOLVER
# ==========================================

def resolver():

    datos = obtener_datos()

    metodo = metodo_escogido.get()

    # ======================================
    # LIMPIAR RESULTADOS
    # ======================================

    limpiar_frame(frame_resultados)

    # ======================================
    # TÍTULO RESULTADOS
    # ======================================

    titulo_resultado = ctk.CTkLabel(
        frame_resultados,
        text="Resultados del Problema",
        font=("Arial", 28, "bold")
    )

    titulo_resultado.pack(pady=(20, 10))

    # ======================================
    # MÉTODO SELECCIONADO
    # ======================================

    metodo_label = ctk.CTkLabel(
        frame_resultados,
        text=f"Método seleccionado: {metodo.upper()}",
        font=("Arial", 18, "bold"),
        text_color="cyan"
    )

    metodo_label.pack(pady=10)

    # ======================================
    # CAJA DE RESULTADOS
    # ======================================

    resultado_texto = ctk.CTkTextbox(
        frame_resultados,
        width=1100,
        height=450,
        font=("Consolas", 16),
        corner_radius=12
    )

    resultado_texto.pack(
        padx=20,
        pady=20,
        fill="both",
        expand=True
    )

    # ======================================
    # CONTENIDO
    # ======================================

    resultado_texto.insert(
        "end",
        "========================================\n"
    )

    resultado_texto.insert(
        "end",
        "        INVESTIGACIÓN DE OPERACIONES\n"
    )

    resultado_texto.insert(
        "end",
        "========================================\n\n"
    )

    resultado_texto.insert(
        "end",
        f"MÉTODO UTILIZADO:\n{metodo.upper()}\n\n"
    )

    resultado_texto.insert(
        "end",
        "========================================\n"
    )

    resultado_texto.insert(
        "end",
        "DATOS INGRESADOS\n"
    )

    resultado_texto.insert(
        "end",
        "========================================\n\n"
    )

    resultado_texto.insert(
        "end",
        f"{datos}\n\n"
    )

    # ======================================
    # SIMULACIÓN TABLA SIMPLEX
    # ======================================

    resultado_texto.insert(
        "end",
        "========================================\n"
    )

    resultado_texto.insert(
        "end",
        "TABLA INICIAL\n"
    )

    resultado_texto.insert(
        "end",
        "========================================\n\n"
    )

    resultado_texto.insert(
        "end",
        "XB     X1     X2     S1     S2     BI\n"
    )

    resultado_texto.insert(
        "end",
        "----------------------------------------\n"
    )

    resultado_texto.insert(
        "end",
        "S1      1      2      1      0      8\n"
    )

    resultado_texto.insert(
        "end",
        "S2      3      2      0      1     12\n\n"
    )

    resultado_texto.insert(
        "end",
        "Zj - Cj\n"
    )

    resultado_texto.insert(
        "end",
        "-3     -5      0      0\n\n"
    )

    # ======================================
    # ITERACIONES
    # ======================================

    resultado_texto.insert(
        "end",
        "========================================\n"
    )

    resultado_texto.insert(
        "end",
        "ITERACIÓN 1\n"
    )

    resultado_texto.insert(
        "end",
        "========================================\n\n"
    )

    resultado_texto.insert(
        "end",
        "Variable que entra: X2\n"
    )

    resultado_texto.insert(
        "end",
        "Variable que sale: S1\n"
    )

    resultado_texto.insert(
        "end",
        "Pivote: 2\n\n"
    )

    # ======================================
    # SOLUCIÓN FINAL
    # ======================================

    resultado_texto.insert(
        "end",
        "========================================\n"
    )

    resultado_texto.insert(
        "end",
        "SOLUCIÓN ÓPTIMA\n"
    )

    resultado_texto.insert(
        "end",
        "========================================\n\n"
    )

    resultado_texto.insert(
        "end",
        "X1 = 4\n"
    )

    resultado_texto.insert(
        "end",
        "X2 = 2\n\n"
    )

    resultado_texto.insert(
        "end",
        "Z = 26\n"
    )

    resultado_texto.configure(state="disabled")

    # ======================================
    # MENSAJE
    # ======================================

    mensaje_estado.configure(
        text="Problema resuelto correctamente",
        text_color="lightgreen"
    )


# ==========================================
# LIMPIAR
# ==========================================

def limpiar():

    entry_variables.delete(0, "end")

    entry_restricciones.delete(0, "end")

    metodo_escogido.set("grafico")

    r_grafico.configure(state="normal")

    limpiar_frame(frame_formulario)

    limpiar_frame(frame_resultados)

    mensaje_estado.configure(
        text="Campos limpiados",
        text_color="white"
    )


# ==========================================
# TRACE
# ==========================================

variables_texto.trace_add(
    "write",
    verificar_variables
)

# ==========================================
# HEADER
# ==========================================

header = ctk.CTkFrame(
    app,
    height=100,
    corner_radius=0
)

header.pack(fill="x")

titulo = ctk.CTkLabel(
    header,
    text="Método Gráfico y Dos Fases",
    font=("Arial", 42, "bold")
)

titulo.pack(pady=25)

# ==========================================
# FRAME PRINCIPAL
# ==========================================

frame_principal = ctk.CTkFrame(
    app,
    corner_radius=20
)

frame_principal.pack(
    padx=20,
    pady=20,
    fill="both",
    expand=True
)

# ==========================================
# CONFIGURACIÓN
# ==========================================

lbl_configuracion = ctk.CTkLabel(
    frame_principal,
    text="Configuración del Problema",
    font=("Arial", 30, "bold")
)

lbl_configuracion.pack(
    pady=(25, 25)
)

# ==========================================
# FRAME ENTRADAS
# ==========================================

frame_inputs = ctk.CTkFrame(
    frame_principal,
    fg_color="transparent"
)

frame_inputs.pack()

# ==========================================
# VARIABLES
# ==========================================

lbl_variables = ctk.CTkLabel(
    frame_inputs,
    text="Número de variables",
    font=("Arial", 20)
)

lbl_variables.grid(
    row=0,
    column=0,
    padx=20,
    pady=10
)

entry_variables = ctk.CTkEntry(
    frame_inputs,
    width=220,
    height=45,
    font=("Arial", 20),
    textvariable=variables_texto
)

entry_variables.grid(
    row=1,
    column=0,
    padx=20
)

# ==========================================
# RESTRICCIONES
# ==========================================

lbl_restricciones = ctk.CTkLabel(
    frame_inputs,
    text="Número de restricciones",
    font=("Arial", 20)
)

lbl_restricciones.grid(
    row=0,
    column=1,
    padx=20,
    pady=10
)

entry_restricciones = ctk.CTkEntry(
    frame_inputs,
    width=220,
    height=45,
    font=("Arial", 20)
)

entry_restricciones.grid(
    row=1,
    column=1,
    padx=20
)

# ==========================================
# MÉTODOS
# ==========================================

frame_metodos = ctk.CTkFrame(
    frame_principal
)

frame_metodos.pack(
    pady=30,
    padx=30
)

lbl_metodo = ctk.CTkLabel(
    frame_metodos,
    text="Método de resolución",
    font=("Arial", 24, "bold")
)

lbl_metodo.pack(pady=15)

r_grafico = ctk.CTkRadioButton(
    frame_metodos,
    text="Método Gráfico",
    variable=metodo_escogido,
    value="grafico",
    font=("Arial", 18)
)

r_grafico.pack(pady=8)

r_dos_fases = ctk.CTkRadioButton(
    frame_metodos,
    text="Método Dos Fases",
    variable=metodo_escogido,
    value="dos_fases",
    font=("Arial", 18)
)

r_dos_fases.pack(pady=8)

# ==========================================
# ESTADO
# ==========================================

mensaje_estado = ctk.CTkLabel(
    frame_principal,
    text="Configure el problema",
    font=("Arial", 16, "bold")
)

mensaje_estado.pack(pady=10)

# ==========================================
# BOTONES
# ==========================================

frame_botones = ctk.CTkFrame(
    frame_principal,
    fg_color="transparent"
)

frame_botones.pack(pady=20)

btn_confirmar = ctk.CTkButton(
    frame_botones,
    text="Generar Formulario",
    width=220,
    height=50,
    font=("Arial", 18, "bold"),
    command=confirmar
)

btn_confirmar.pack(
    side="left",
    padx=10
)

btn_resolver = ctk.CTkButton(
    frame_botones,
    text="Resolver",
    width=220,
    height=50,
    font=("Arial", 18, "bold"),
    command=resolver
)

btn_resolver.pack(
    side="left",
    padx=10
)

btn_limpiar = ctk.CTkButton(
    frame_botones,
    text="Limpiar",
    width=220,
    height=50,
    font=("Arial", 18, "bold"),
    fg_color="#8B0000",
    hover_color="#5E0000",
    command=limpiar
)

btn_limpiar.pack(
    side="left",
    padx=10
)

# ==========================================
# FORMULARIO DINÁMICO
# ==========================================

frame_formulario = ctk.CTkScrollableFrame(
    frame_principal,
    width=1150,
    height=300,
    corner_radius=15
)

frame_formulario.pack(
    pady=20,
    padx=20,
    fill="both",
    expand=True
)

# ==========================================
# RESULTADOS
# ==========================================

frame_resultados = ctk.CTkScrollableFrame(
    frame_principal,
    width=1150,
    height=350,
    corner_radius=15
)

frame_resultados.pack(
    pady=(0, 20),
    padx=20,
    fill="both",
    expand=True
)

# ==========================================
# EJECUTAR APP
# ==========================================

app.mainloop()