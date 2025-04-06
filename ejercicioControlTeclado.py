import pyautogui
import time
import subprocess
import pyperclip

def main():
    # Activar TextEdit y crear un nuevo documento mediante AppleScript
    subprocess.Popen(["osascript", "-e", 'tell application "TextEdit" to activate'])
    time.sleep(2)
    subprocess.Popen(["osascript", "-e", 'tell application "TextEdit" to make new document'])
    time.sleep(5)
    
    # Escribir el shebang: "#!/usr/bin/env python3"
    shebang = "#!/usr/bin/env python3"
    pyperclip.copy(shebang)
    time.sleep(1)
    # Usar keyDown/press/keyUp para pegar el contenido del portapapeles
    pyautogui.keyDown('command')
    pyautogui.press('v')
    pyautogui.keyUp('command')
    pyautogui.press('enter')
    
    # Escribir la línea del for: "for i in range(5):"
    pyautogui.write('for i in range', interval=0.05)
    pyautogui.hotkey('shift', '8')   # Simula "(" (Shift+8)
    pyautogui.write('5', interval=0.05)
    pyautogui.hotkey('shift', '9')   # Simula ")" (Shift+9)
    # Para el carácter ":", copiar y pegar (evita que se escriba "Ñ")
    pyperclip.copy(":")
    pyautogui.keyDown('command')
    pyautogui.press('v')
    pyautogui.keyUp('command')
    pyautogui.press('enter')
    
    # Escribir la línea del print: "    print("Hello, World!\n")"
    pyautogui.write('    print', interval=0.05)
    pyautogui.hotkey('shift', '8')   # Simula "("
    pyautogui.write('"Hello, World!', interval=0.05)
    # Insertar la secuencia "\n" copiándola al portapapeles y pegándola
    pyperclip.copy('\\n')
    pyautogui.keyDown('command')
    pyautogui.press('v')
    pyautogui.keyUp('command')
    pyautogui.write('"', interval=0.05)
    pyautogui.hotkey('shift', '9')   # Simula ")" (Shift+9)
    pyautogui.press('enter')
    
    # Convertir el documento a texto plano (Cmd+Shift+T) para poder guardarlo como .py
    pyautogui.hotkey('command', 'shift', 't')
    time.sleep(1)
    
    # Guardar el archivo: simular Cmd+S para abrir el diálogo de guardado
    pyautogui.hotkey('command', 's')
    time.sleep(1)
    
    # Escribir el nombre del archivo y confirmar el guardado
    pyautogui.write('scriptEjemplo.py', interval=0.05)
    pyautogui.press('enter')
    time.sleep(2)
    
    # Cerrar el documento con Cmd+W
    pyautogui.hotkey('command', 'w')
    time.sleep(1)

if __name__ == "__main__":
    main()