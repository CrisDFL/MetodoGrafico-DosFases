import customtkinter as ctk

from utils.validaciones import (
    es_entero_positivo,
    validar_metodo_grafico
)

from ui.formulario import (
    generar_formulario,
    obtener_datos
)
from metodos.metodografico import (
    metodo_grafico
)
from metodos.metododosfases import (
    metodo_dos_fases
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
app.minsize(900, 600)
app.resizable(True, True)

# ==========================================
# VARIABLES GLOBALES
# ==========================================

metodo_escogido = ctk.StringVar(value="grafico")
tipo_problema = ctk.StringVar(value="max")
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

    if valor == "":
        r_grafico.configure(state="normal")
        mensaje_estado.configure(
            text="Configure el problema",
            text_color="white"
        )
        return

    if not es_entero_positivo(valor):
        mensaje_estado.configure(
            text="Ingrese un número válido",
            text_color="red"
        )
        return

    cantidad_variables = int(valor)

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

    if variables == "" or restricciones == "":
        mensaje_estado.configure(
            text="Complete todos los campos",
            text_color="red"
        )
        return

    if not es_entero_positivo(variables):
        mensaje_estado.configure(
            text="Número de variables inválido",
            text_color="red"
        )
        return

    if not es_entero_positivo(restricciones):
        mensaje_estado.configure(
            text="Número de restricciones inválido",
            text_color="red"
        )
        return

    variables = int(variables)
    restricciones = int(restricciones)

    limpiar_frame(frame_formulario)

    generar_formulario(
        frame_formulario,
        variables,
        restricciones,
        tipo_problema.get()
    )

    mensaje_estado.configure(
        text="Formulario generado correctamente",
        text_color="lightgreen"
    )

    btn_resolver = ctk.CTkButton(
        frame_formulario,
        text="Resolver",
        width=220,
        height=50,
        font=("Arial", 18, "bold"),
        command=resolver
    )
    btn_resolver.pack(padx=10, pady=20)


# ==========================================
# RESOLVER
# ==========================================

def resolver():
    datos = obtener_datos(tipo_problema.get())
    metodo = metodo_escogido.get()
    if metodo == "grafico":
        mensaje_estado.configure(
            text="Resolviendo con método gráfico...",
            text_color="lightblue"
        )
        metodo_grafico(frame_formulario, datos)
    elif metodo == "dos_fases":
        mensaje_estado.configure(
            text="Resolviendo con método dos fases...",
            text_color="lightblue"
        )
        metodo_dos_fases(frame_formulario, datos)


# ==========================================
# LIMPIAR
# ==========================================

def limpiar():
    entry_variables.delete(0, "end")
    entry_restricciones.delete(0, "end")
    metodo_escogido.set("grafico")
    r_grafico.configure(state="normal")
    limpiar_frame(frame_formulario)
    mensaje_estado.configure(
        text="Campos limpiados",
        text_color="white"
    )


# ==========================================
# TRACE
# ==========================================

variables_texto.trace_add("write", verificar_variables)

# ==========================================
# HEADER
# ==========================================

header = ctk.CTkFrame(app, height=100, corner_radius=0)
header.pack(fill="x")

titulo = ctk.CTkLabel(
    header,
    text="Método Gráfico y Dos Fases",
    font=("Arial", 42, "bold")
)
titulo.pack(pady=25)

# ==========================================
# CONTENEDOR PRINCIPAL (grid de 2 columnas)
# ==========================================

frame_contenedor = ctk.CTkFrame(app, fg_color="transparent")
frame_contenedor.pack(fill="both", expand=True, padx=20, pady=20)

# Columna 0: panel izquierdo fijo, columna 1: formulario se expande
frame_contenedor.grid_columnconfigure(0, weight=0, minsize=340)
frame_contenedor.grid_columnconfigure(1, weight=1)
frame_contenedor.grid_rowconfigure(0, weight=1)

# ==========================================
# PANEL IZQUIERDO con scroll
# ==========================================

scroll_izq = ctk.CTkScrollableFrame(
    frame_contenedor,
    corner_radius=20,
    width=420
)
scroll_izq.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

frame_principal = scroll_izq  # todos los widgets van directo aquí

# ==========================================
# CONFIGURACIÓN
# ==========================================

lbl_configuracion = ctk.CTkLabel(
    frame_principal,
    text="Configuración del Problema",
    font=("Arial", 26, "bold")
)
lbl_configuracion.pack(pady=(25, 20))

# ==========================================
# FRAME ENTRADAS (en columna vertical)
# ==========================================

frame_inputs = ctk.CTkFrame(frame_principal, fg_color="transparent")
frame_inputs.pack(fill="x", padx=20)

lbl_variables = ctk.CTkLabel(
    frame_inputs,
    text="Número de variables",
    font=("Arial", 18)
)
lbl_variables.pack(pady=(5, 2))

entry_variables = ctk.CTkEntry(
    frame_inputs,
    height=45,
    font=("Arial", 18),
    textvariable=variables_texto
)
entry_variables.pack(fill="x")

lbl_restricciones = ctk.CTkLabel(
    frame_inputs,
    text="Número de restricciones",
    font=("Arial", 18)
)
lbl_restricciones.pack(pady=(12, 2))

entry_restricciones = ctk.CTkEntry(
    frame_inputs,
    height=45,
    font=("Arial", 18)
)
entry_restricciones.pack(fill="x")

# ==========================================
# MÉTODOS
# ==========================================

frame_metodos = ctk.CTkFrame(frame_principal)
frame_metodos.pack(pady=20, padx=20, fill="x")

lbl_metodo = ctk.CTkLabel(
    frame_metodos,
    text="Método de resolución",
    font=("Arial", 20, "bold")
)
lbl_metodo.pack(pady=12)

r_grafico = ctk.CTkRadioButton(
    frame_metodos,
    text="Método Gráfico",
    variable=metodo_escogido,
    value="grafico",
    font=("Arial", 16)
)
r_grafico.pack(pady=6)

r_dos_fases = ctk.CTkRadioButton(
    frame_metodos,
    text="Método Dos Fases",
    variable=metodo_escogido,
    value="dos_fases",
    font=("Arial", 16)
)
r_dos_fases.pack(pady=6)

# ==========================================
# TIPO DE PROBLEMA
# ==========================================

frame_tipo = ctk.CTkFrame(frame_principal)
frame_tipo.pack(pady=20, padx=20, fill="x")

lbl_tipo = ctk.CTkLabel(
    frame_tipo,
    text="Tipo de problema",
    font=("Arial", 20, "bold")
)
lbl_tipo.pack(pady=12)

frame_tipo_botones = ctk.CTkFrame(frame_tipo, fg_color="transparent")
frame_tipo_botones.pack(pady=5)

t_max = ctk.CTkRadioButton(
    frame_tipo_botones,
    text="Maximización",
    variable=tipo_problema,
    value="max",
    font=("Arial", 16)
)
t_max.pack(side="left", padx=15)

t_min = ctk.CTkRadioButton(
    frame_tipo_botones,
    text="Minimización",
    variable=tipo_problema,
    value="min",
    font=("Arial", 16)
)
t_min.pack(side="left", padx=15)

# ==========================================
# ESTADO
# ==========================================

mensaje_estado = ctk.CTkLabel(
    frame_principal,
    text="Configure el problema",
    font=("Arial", 15, "bold")
)
mensaje_estado.pack(pady=10)

# ==========================================
# BOTONES
# ==========================================

frame_botones = ctk.CTkFrame(frame_principal, fg_color="transparent")
frame_botones.pack(pady=15, padx=20, fill="x")

btn_confirmar = ctk.CTkButton(
    frame_botones,
    text="Generar Formulario",
    height=50,
    font=("Arial", 16, "bold"),
    command=confirmar
)
btn_confirmar.pack(fill="x", pady=(0, 8))

btn_limpiar = ctk.CTkButton(
    frame_botones,
    text="Limpiar",
    height=50,
    font=("Arial", 16, "bold"),
    fg_color="#8B0000",
    hover_color="#5E0000",
    command=limpiar
)
btn_limpiar.pack(fill="x")

# ==========================================
# FORMULARIO DINÁMICO (panel derecho)
# ==========================================

frame_formulario = ctk.CTkScrollableFrame(
    frame_contenedor,
    corner_radius=15
)
frame_formulario.grid(row=0, column=1, sticky="nsew")


# ==========================================
# EJECUTAR APP
# ==========================================

app.mainloop()