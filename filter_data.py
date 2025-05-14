import numpy as np
from scipy.signal import sos2tf

# Para leer archivos que vienen de MatLab
def leer_fcf(path):
    sos = []
    scale_values = []

    with open(path, 'r') as file:
        lines = file.readlines()

    is_sos = False
    is_scale = False

    for line in lines:
        line = line.strip()
        if not line or line.startswith('%'):
            continue

        if "SOS Matrix" in line:
            is_sos = True
            continue
        elif "Scale Values" in line:
            is_sos = False
            is_scale = True
            continue

        if is_sos:
            values = list(map(float, line.split()))
            sos.append(values)
        elif is_scale:
            values = list(map(float, line.split()))
            scale_values.extend(values)

    sos_matrix = np.array(sos)
    scale_values = np.array(scale_values)

    return sos_matrix, scale_values

def getFilterData(filter_path):
    sos_matrix, scale_values = leer_fcf(filter_path)
    # Obtener los coeficientes del sistema
    total_gain = np.prod(scale_values)
    b, a = sos2tf(sos_matrix)

    # Aplicar la ganancia global
    b *= total_gain

    # Obteer el orden del filtro
    n = len(b) - 1

    print(b)
    print(a)
    print(n)

    return b, a, n
