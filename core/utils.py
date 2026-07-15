import bleach

def sanitize_text(value: str) -> str:
    """
    Sanitiza una cadena de texto eliminando cualquier etiqueta HTML o script.
    Si el valor no es un string o es None, lo retorna tal cual.
    """
    if not isinstance(value, str):
        return value
    
    # tags=[] y strip=True remueven todas las etiquetas HTML (como <script>, <html>, etc.)
    # devolviendo solo texto plano limpio.
    return bleach.clean(value, tags=[], strip=True)
