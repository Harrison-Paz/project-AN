mapeo_CONDUCTA_INAPROPIADA = {
  'BAJA': 0,
  'MEDIA': 1,
  'ALTA': 2,
}

mapeo_NOTA = {
    'D': 0,
    'C': 1,
    'B': 2,
    'A': 3,
}

mapeo_RETIRO = {
    'NO': 0,
    'SI': 1,
}

def categorizar_conducta(valor):
    if valor <= 5:
        return 'BAJA'
    elif valor < 10:
        return 'MEDIA'
    else:
        return 'ALTA'

def categorizar_nota(valor):
    valor = float(valor)

    if valor <= 5:
        return 'D'
    elif valor <= 11:
        return 'C'
    elif valor <= 16:
        return 'B'
    else:
        return 'A'