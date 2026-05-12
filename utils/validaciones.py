# ======================================
# VALIDACIONES
# ======================================

def es_entero_positivo(valor):

    """
    Verifica si el valor es un entero positivo.
    """

    return valor.isdigit() and int(valor) > 0


def validar_metodo_grafico(cantidad_variables):

    """
    El método gráfico solo permite máximo 2 variables.
    """

    return cantidad_variables <= 2