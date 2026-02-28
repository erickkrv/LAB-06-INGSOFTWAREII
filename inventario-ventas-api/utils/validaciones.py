def es_email_valido(email: str) -> bool:
    return "@" in email and "." in email

def tiene_stock_suficiente(stock_actual, cantidad_req):
    return stock_actual >= cantidad_req
