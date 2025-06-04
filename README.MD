# Remuxador de Videos con ffmpeg y Python

Este script permite remuxear (cambiar contenedor sin recodificar) archivos de video desde múltiples formatos de entrada a un formato de salida especificado, utilizando `ffmpeg` y `ffprobe` integrados. Además, muestra barras de progreso interactivas para cada archivo y para el proceso total.

-------------------------------------------------------------------------------------------------------------

## Características

- Soporta múltiples formatos de video como entrada: `.mp4`, `.mov`, `.avi`, `.m4v`, `.ts`, `.flv`, `.webm`, `.wmv`, `.mpg`, `.mpeg`, `.mkv`.
- Permite elegir formatos de entrada y salida desde la línea de comandos o vía selección interactiva.
- Muestra progreso individual por archivo y progreso total usando la librería [rich](https://github.com/Textualize/rich).
- Detecta duración de los videos con `ffprobe` para calcular el progreso real.
- Maneja interrupciones con Ctrl+C para salir limpiamente.
- Guarda los archivos remuxeados en una carpeta `output` dentro del directorio de trabajo.
- Compatible con ejecución directa en Python o como ejecutable generado con PyInstaller.

-------------------------------------------------------------------------------------------------------------

## Requisitos

- Python 3.6+
- `ffmpeg.exe` y `ffprobe.exe` deben estar en el mismo directorio que el script o el ejecutable.
- Librería `rich` (instalable con `pip install rich`).

-------------------------------------------------------------------------------------------------------------

## Uso

Ejecutar el script desde línea de comandos:

```bash
python MKVPLEX_1_00.py [-i formatos_de_entrada] [-o formato_salida]
````

Ejemplos:

* Remuxear todos los `.mp4` y `.mov` a `.mkv`:

```bash
python MKVPLEX_1_00.py -i mp4,mov -o mkv
```

* Ejecutar sin argumentos para usar selección interactiva:

```bash
python MKVPLEX_1_00.py
```

-------------------------------------------------------------------------------------------------------------

## Formatos soportados

### Entrada

`.mp4`, `.mov`, `.avi`, `.m4v`, `.ts`, `.flv`, `.webm`, `.wmv`, `.mpg`, `.mpeg`, `.mkv`

### Salida

`mkv`, `mp4`, `mov`, `webm`, `ts`, `avi`

-------------------------------------------------------------------------------------------------------------

## Directorios y archivos

* Los archivos a remuxear deben estar en el mismo directorio donde se ejecuta el script.
* Los archivos remuxeados se guardan en la carpeta `output`, que se crea automáticamente.

-------------------------------------------------------------------------------------------------------------

## Manejo de interrupciones

Presionar Ctrl+C detendrá el proceso limpiamente y cerrará los procesos `ffmpeg` en ejecución.

-------------------------------------------------------------------------------------------------------------

## Compilación con PyInstaller

Para generar un ejecutable independiente con `ffmpeg` y `ffprobe` embebidos, usar:

#----------------------------------------------------------------------------------------------------------------------------------------#
# scrip para compilar [ pyinstaller --onefile --add-binary "ffmpeg.exe;." --add-binary "ffprobe.exe;." --icon=ICO.ico MKVPLEX_1_00.py]   |
#----------------------------------------------------------------------------------------------------------------------------------------#
