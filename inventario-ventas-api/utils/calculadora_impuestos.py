"""
Módulo para el cálculo de impuestos y totales de facturación.
"""

def calcular_total(subtotal: float, descuento: float = 0.0) -> float:
    """
    Calcula el total a pagar aplicando un descuento al subtotal y sumando el IVA (12%).
    """
    tasa_iva = 0.12
    subtotal_con_descuento = subtotal - descuento
    iva = subtotal_con_descuento * tasa_iva
    total = subtotal_con_descuento + iva
    return total
