import customtkinter as ctk

# FUNCIONES

#Verificar el numero de variables
def Verificar(*args):
    valor = validacion.get()
    if valor.isdigit() and int(valor) > 2:
        r_grafico.configure(state="disabled")
        metodo_escogido.set("fases")
        print("Metodo de dos fases seleccionado")
    else:
        r_grafico.configure(state="normal")

def Confirmar():
    print("Confirmar")

def Limpiar():
    print("Limpiar")


app = ctk.CTk()

app.title("Investigacion de Operaciones")
app.geometry("780x500")

#Variables de control
validacion = ctk.StringVar()
validacion.trace_add("write", Verificar)
metodo_escogido = ctk.StringVar(value="grafico")

#Encabezado
titulo = ctk.CTkLabel(app, text="prueba", font=("Arial", 24, "bold"), text_color="#a8d8ea")
titulo.pack(pady=20)


#Bloque de selectores
selectores_frame = ctk.CTkFrame(app)
selectores_frame.pack(pady=20)

##Selector de número de variables
lbl_variables = ctk.CTkLabel(selectores_frame, text="Número de variables:", font=("Arial", 16))
lbl_variables.pack(pady=10)
selector_variable = ctk.CTkEntry(selectores_frame, font=("Arial", 16), textvariable=validacion)
selector_variable.pack(pady=10)

##Selector de número de restricciones
lbl_restricciones = ctk.CTkLabel(selectores_frame, text="Número de restricciones:", font=("Arial", 16))
lbl_restricciones.pack(pady=10)
selector_restricciones = ctk.CTkEntry(selectores_frame, font=("Arial", 16))
selector_restricciones.pack(pady=10)


##Selector de tipo de metodo
lbl_metodo = ctk.CTkLabel(selectores_frame, text="Tipo de método:", font=("Arial", 16))
lbl_metodo.pack(pady=10)


r_grafico = ctk.CTkRadioButton(selectores_frame, text="Gráfico (Máx 2 Variables)", value="grafico", variable=metodo_escogido, font=("Arial", 16))
r_grafico.pack(pady=10)
r_fases = ctk.CTkRadioButton(selectores_frame, text="Dos Fases", value="fases", variable=metodo_escogido, font=("Arial", 16))
r_fases.pack(pady=10)


##Botones
btn_confirmar = ctk.CTkButton(selectores_frame, text="Confirmar", font=("Arial", 16), command=Confirmar)
btn_confirmar.pack(side="left", pady=10, padx=10)

btn_limpiar = ctk.CTkButton(selectores_frame, text="Limpiar", font=("Arial", 16), command=Limpiar)
btn_limpiar.pack(side="left", pady=10, padx=10)

app.mainloop()