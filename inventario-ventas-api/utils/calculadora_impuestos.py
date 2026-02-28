# DEFECTO: Nombres de variables poco descriptivos (Mantenibilidad)
def calc_imp(s, d=0):
    t = 0.12
    x = s - (s * d)
    z = x * t
    r = x + z
    return r, z, x

# DEFECTO: Dead code
def calc_desc_esp(m):
    if m > 1000:
        return 0.10
    return 0.05
