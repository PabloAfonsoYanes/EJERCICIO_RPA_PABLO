import os
import time
import subprocess
import pyautogui
import pyperclip

def create_dummy_files():
    """
    Crea dos archivos dummy en el Escritorio para que aparezcan iconos con posiciones fijas.
    """
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    file1 = os.path.join(desktop, "dummy1.txt")
    file2 = os.path.join(desktop, "dummy2.txt")
    
    with open(file1, "w") as f:
        f.write("Dummy file 1")
    with open(file2, "w") as f:
        f.write("Dummy file 2")
    
    print("Archivos dummy creados en el Escritorio.")
    time.sleep(3)  # Esperar a que Finder actualice la vista de iconos

def simulate_drag_and_drop():
    """
    Activa el Finder y simula el movimiento (arrastrar y soltar) de los archivos dummy usando `dragTo()`.
    Ajusta las coordenadas según tu pantalla.
    """
    # Activar Finder para que se muestre el Escritorio
    subprocess.Popen(["osascript", "-e", 'tell application "Finder" to activate'])
    time.sleep(2)
    
    # Coordenadas iniciales (ejemplo) de los archivos dummy en el Escritorio
    x1, y1 = 200, 200   # Posición de dummy1.txt
    x2, y2 = 200, 350   # Posición de dummy2.txt
    
    # Coordenadas de destino (ejemplo)
    x1_dest, y1_dest = 400, 200
    x2_dest, y2_dest = 400, 350
    
    # Arrastrar dummy1.txt usando dragTo
    pyautogui.moveTo(x1, y1, duration=1)
    pyautogui.dragTo(x1_dest, y1_dest, duration=2, button='left')
    time.sleep(1)
    
    # Arrastrar dummy2.txt usando dragTo
    pyautogui.moveTo(x2, y2, duration=1)
    pyautogui.dragTo(x2_dest, y2_dest, duration=2, button='left')
    time.sleep(1)
    
    print("Archivos movidos mediante dragTo.")

def search_in_chrome():
    """
    Abre Google Chrome, posiciona el cursor en la barra de direcciones,
    escribe un término de búsqueda y toma una captura de pantalla.
    """
    # Abrir Google Chrome
    subprocess.Popen(["open", "-a", "Google Chrome"])
    time.sleep(5)  # Espera a que Chrome se abra completamente
    
    # Enfocar la barra de direcciones: ajusta las coordenadas (ejemplo: (300, 50))
    chrome_bar_x, chrome_bar_y = 650, 525
    pyautogui.moveTo(chrome_bar_x, chrome_bar_y, duration=1)
    pyautogui.click()
    time.sleep(1)
    
    # Escribir el término de búsqueda
    termino_busqueda = "Recetas de cocina saludables"
    pyautogui.write(termino_busqueda, interval=0.07)
    pyautogui.press("enter")
    time.sleep(5)  # Espera a que carguen los resultados
    
    # Tomar captura de pantalla y guardar en el Escritorio
    pyautogui.screenshot()
    print(f"Captura guardada")

def main():
    print("----- CREANDO ARCHIVOS DUMMY -----")
    create_dummy_files()
    
    print("----- SIMULANDO ARRASTRE DE ARCHIVOS -----")
    simulate_drag_and_drop()
    
    print("----- REALIZANDO BÚSQUEDA EN GOOGLE CHROME -----")
    search_in_chrome()
    
    print("Script completado.")

if __name__ == "__main__":
    main()
