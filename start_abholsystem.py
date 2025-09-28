import subprocess
import os

# Verzeichnis festlegen
verzeichnis = r"C:\Users\Cevi WIE\Abholsystem"

# Streamlit-Skripte festlegen
eingabe_script = os.path.join(verzeichnis, "eingabe.py")
resultate_script = os.path.join(verzeichnis, "resultate.py")

# Starte das Eingabe-Programm
subprocess.Popen(["streamlit", "run", eingabe_script])

# Starte das Resultate-Programm
subprocess.Popen(["streamlit", "run", resultate_script])

print("Beide Programme wurden gestartet.")
