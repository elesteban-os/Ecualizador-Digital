# Ecualizador Digital

Este proyecto es un Ecualizador Digital desarrollado en Python utilizando bibliotecas como PyQt5, PyAudio, NumPy, y PyQtGraph. La aplicación permite visualizar y manipular señales de audio en tiempo real mediante filtros digitales, como pasa bajas, pasa altas, pasa bandas, y supresores de bandas. Además, incluye un control deslizante para ajustar dinámicamente la frecuencia de corte de un filtro pasa bajas ajustable.

## Características

- **Visualización en tiempo real**:
    - Forma de onda (Waveform).
    - Espectro de frecuencia (Spectrum).
- **Filtros digitales**:
    - Pasa bajas.
    - Pasa altas.
    - Pasa bandas.
    - Supresor de bandas.
    - Filtro pasa bajas ajustable con control deslizante.
- **Interfaz gráfica interactiva**:
    - Checkboxes para activar/desactivar filtros.
    - Control deslizante para ajustar la frecuencia de corte del filtro pasa bajas ajustable.
- **Procesamiento de audio en tiempo real**:
    - Captura, filtrado y reproducción de audio.

## Requisitos del Sistema

- **Lenguaje**: Python 3.9 o superior.
- **Dependencias**:
    - PyQt5
    - PyQtGraph
    - PyAudio
    - NumPy
    - SciPy
- **Sistema Operativo**: Compatible con Windows, macOS y Linux.
- Asegúrate de que tu sistema tenga configurado correctamente el acceso a dispositivos de audio.

## Instalación

1. Clona este repositorio:
        ```bash
        git clone https://github.com/elesteban-os/Ecualizador-Digital.git
        ```
2. Navega al directorio del proyecto:
        ```bash
        cd Ecualizador-Digital
        ```
3. Instala las dependencias necesarias:
        ```bash
        pip install PyQt5 PyQtGraph PyAudio NumPy SciPy
        ```

## Uso

1. Ejecuta el archivo principal:
        ```bash
        python main.py
        ```
2. La interfaz gráfica mostrará:
     - Checkboxes para activar/desactivar filtros.
     - Un control deslizante para ajustar la frecuencia de corte del filtro pasa bajas ajustable.
     - Gráficos en tiempo real de la forma de onda y el espectro de frecuencia.
3. Interactúa con los controles:
     - Marca/desmarca los checkboxes para activar/desactivar filtros.
     - Ajusta el control deslizante para cambiar la frecuencia de corte del filtro pasa bajas ajustable.
