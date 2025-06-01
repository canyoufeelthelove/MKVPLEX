import subprocess
import sys
import time
from pathlib import Path
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TimeElapsedColumn
import argparse
import signal

# Rutas compatibles con ejecutable y script
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
    WORK_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent
    WORK_DIR = BASE_DIR

FFMPEG = BASE_DIR / "ffmpeg.exe"
FFPROBE = BASE_DIR / "ffprobe.exe"
OUTPUT_DIR = WORK_DIR / "output"

# Lista completa de extensiones soportadas
ALL_EXTS = [".mp4", ".mov", ".avi", ".m4v", ".ts", ".flv", ".webm", ".wmv", ".mpg", ".mpeg", ".mkv"]

def handle_interrupt(signum, frame):
    print("\n⚠️ Proceso interrumpido. Saliendo...")
    sys.exit(1)

signal.signal(signal.SIGINT, handle_interrupt)

def get_duration(file_path):
    try:
        result = subprocess.run([
            str(FFPROBE), "-v", "error", "-show_entries",
            "format=duration", "-of",
            "default=noprint_wrappers=1:nokey=1", str(file_path)
        ], capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except Exception:
        return 0

def remux(file_path, output_path, total_duration, progress, task_id):
    process = subprocess.Popen(
        [str(FFMPEG), "-i", str(file_path), "-c", "copy", str(output_path)],
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    try:
        while True:
            line = process.stderr.readline()
            if not line:
                break
            if "time=" in line:
                try:
                    time_str = line.strip().split("time=")[-1].split(" ")[0]
                    h, m, s = time_str.split(":")
                    seconds = int(h) * 3600 + int(m) * 60 + float(s)
                    if total_duration > 0:
                        progress.update(task_id, completed=seconds)
                except Exception:
                    pass
        process.wait()
    finally:
        if process.stderr:
            process.stderr.close()
        process.terminate()
        process.wait()

def main():
    parser = argparse.ArgumentParser(description="Remuxador de videos")
    parser.add_argument("-i", "--input_format", help="Formato(s) de entrada (mp4, mov, avi, webm, etc.)")
    parser.add_argument("-o", "--output_format", help="Formato de salida (mkv, mp4, mov, webm, ts, avi)")
    args = parser.parse_args()

    # Selección interactiva si no se especifican argumentos
    if not args.input_format:
        print("📥 Formatos de entrada disponibles:", ", ".join(ext.strip(".") for ext in ALL_EXTS))
        chosen_input = input("👉 Ingresa formato(s) de entrada separados por coma (ej: mp4, mov): ").strip().lower()
        input_exts = [f".{ext.strip()}" for ext in chosen_input.split(",") if f".{ext.strip()}" in ALL_EXTS]
        if not input_exts:
            print("❌ Formatos de entrada inválidos. Usando todos los formatos disponibles.")
            input_exts = ALL_EXTS
    else:
        input_exts = [f".{ext.strip()}" for ext in args.input_format.split(",") if f".{ext.strip()}" in ALL_EXTS]
        if not input_exts:
            input_exts = ALL_EXTS

    if not args.output_format:
        print("📤 Formatos de salida disponibles: mkv, mp4, mov, webm, ts, avi")
        chosen_output = input("👉 Ingresa el formato de salida: ").strip().lower()
        if chosen_output not in ["mkv", "mp4", "mov", "webm", "ts", "avi"]:
            print("❌ Formato de salida inválido. Usando mkv por defecto.")
            chosen_output = "mkv"
    else:
        chosen_output = args.output_format.lower()

    output_ext = f".{chosen_output}"

    if not FFMPEG.exists() or not FFPROBE.exists():
        print("❌ No se encontraron ffmpeg.exe y/o ffprobe.exe.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(exist_ok=True)
    files = [f for f in WORK_DIR.iterdir() if f.suffix.lower() in input_exts and f.is_file()]
    total_files = len(files)

    if not total_files:
        print(f"⚠️ No se encontraron archivos con extensiones: {', '.join(input_exts)}")
        return

    try:
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            transient=True
        ) as progress:
            main_task = progress.add_task("📦 Progreso total", total=total_files)

            for file in files:
                output_file = OUTPUT_DIR / (file.stem + output_ext)
                duration = get_duration(file)
                file_task = progress.add_task(f"🎥 {file.name}", total=duration)
                try:
                    remux(file, output_file, duration, progress, file_task)
                except Exception as e:
                    print(f"❌ Error con {file.name}: {e}")
                progress.update(main_task, advance=1)

        print(f"✅ Todos los archivos han sido remuxeados a *{chosen_output}*.")

    except KeyboardInterrupt:
        print("\n⚠️ Proceso interrumpido manualmente.")
    finally:
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()

# scrip para compilar [ pyinstaller --onefile --add-binary "ffmpeg.exe;." --add-binary "ffprobe.exe;." --icon=ICO.ico MKVPLEX_1_00.py]
