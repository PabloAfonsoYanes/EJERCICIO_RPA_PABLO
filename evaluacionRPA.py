import os
import time
import subprocess
import pyautogui
import pyperclip
import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup

# Importaciones necesarias para Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def obtener_titulares_vivienda_selenium():
    """
    Usa Selenium para:
      1. Abrir Chrome y cargar la página principal de El País.
      2. Al tener bloqueadas las cookies, el popup no aparecerá.
      3. Hacer clic en el enlace "ECONOMÍA".
      4. Hacer clic en el enlace "VIVIENDA".
      5. Extraer los 5 primeros titulares de la sección (usando las etiquetas <h2>).
      
    Devuelve una lista con los 5 titulares o una lista vacía si ocurre algún error.
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    # Configurar para bloquear cookies
    prefs = {
        "profile.default_content_setting_values.cookies": 2,  # Bloquea todas las cookies
        "profile.block_third_party_cookies": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)
    
    try:
        driver.get("https://elpais.com/")
        time.sleep(3)
        
        # Hacer clic en "ECONOMÍA"
        economia_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "ECONOMÍA")))
        economia_button.click()
        time.sleep(3)
        
        # Hacer clic en "VIVIENDA"
        vivienda_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "VIVIENDA")))
        vivienda_button.click()
        time.sleep(3)
        
        # Extraer los titulares de la página
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        titulares = []
        for h2 in soup.find_all("h2"):
            texto = h2.get_text(strip=True)
            if texto:
                titulares.append(texto)
            if len(titulares) >= 5:
                break
                
        return titulares
    except Exception as e:
        print("Error durante la navegación con Selenium:", e)
        return []
    finally:
        driver.quit()

def ver_titulares_vivienda():
    """
    Obtiene titulares de la sección Vivienda y luego:
      - Abre Microsoft Word.
      - Crea un nuevo documento en blanco (simulando Command+N manteniendo pulsado Command).
      - Pega los 5 titulares (usando el portapapeles para preservar caracteres en español).
      - Simula el guardado del documento con el nombre "pruebaRPA" sin cerrar Word.
    """
    titulares = obtener_titulares_vivienda_selenium()
    if not titulares:
        temp_root = tk.Tk()
        temp_root.withdraw()
        messagebox.showerror("Error", "No se han obtenido titulares de la sección Vivienda.")
        temp_root.destroy()
        return

    # Abrir Microsoft Word
    subprocess.Popen(["open", "-a", "Microsoft Word"])
    time.sleep(6)  # Tiempo para que Word se inicie

    # Crear un nuevo documento en blanco usando Command+N (manteniendo pulsado Command)
    pyautogui.keyDown('command')
    pyautogui.press('n')
    pyautogui.keyUp('command')
    time.sleep(3)  # Esperar a que se abra el nuevo documento

    # Escribir los titulares (solo los 5 primeros)
    for i, titular in enumerate(titulares[:5], start=1):
        linea = f"{i}. {titular}"
        pyperclip.copy(linea)
        pyautogui.hotkey('command', 'v')
        pyautogui.press("enter")
        pyautogui.press("enter")  # Línea en blanco entre titulares

    time.sleep(1)
    
    # Simular guardar el documento con Command+S
    pyautogui.hotkey('command', 's')
    time.sleep(2)  # Esperar a que aparezca el diálogo de guardado

    # Escribir el nombre del documento: "pruebaRPA"
    pyautogui.write("pruebaRPA", interval=0.05)
    time.sleep(0.5)
    pyautogui.press("enter")
    
    time.sleep(2)
    temp_root = tk.Tk()
    temp_root.withdraw()
    messagebox.showinfo(
        "Estado", "Listo.\nLos titulares se han pegado y el documento se ha guardado como 'pruebaRPA'.\nWord permanece abierto.")
    temp_root.destroy()

def abrir_word():
    """
    Abre Microsoft Word sin realizar otras acciones.
    """
    subprocess.Popen(["open", "-a", "Microsoft Word"])
    time.sleep(2)
    temp_root = tk.Tk()
    temp_root.withdraw()
    messagebox.showinfo("Estado", "Word abierto.")
    temp_root.destroy()

def main():
    # Interfaz simple con Tkinter para elegir la acción deseada
    root = tk.Tk()
    root.title("RPA: Noticias de Vivienda")
    root.geometry("400x180")
    
    label = tk.Label(root, text="Elige una acción:", font=("Arial", 14))
    label.pack(pady=10)
    
    btn_titulares = tk.Button(root, text="Ver titulares de vivienda", 
                              command=lambda: [root.destroy(), ver_titulares_vivienda()],
                              width=25, height=2, bg="lightblue")
    btn_titulares.pack(pady=5)
    
    btn_word = tk.Button(root, text="Abrir Word", 
                         command=lambda: [root.destroy(), abrir_word()],
                         width=25, height=2, bg="lightgreen")
    btn_word.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()