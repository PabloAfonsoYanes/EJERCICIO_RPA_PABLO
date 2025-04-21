import os
import sys
import time
import pandas as pd
import pyautogui
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# —————— Configuración ——————
HISTORY_CSV      = "historial_precios.csv"
EMAIL_RECIPIENTS = ["pabloafonsoyanes@gmail.com"]

# Definición de tiendas con URL, selectores y umbral
TIENDAS = [
    {
        "name": "Asos",
        "start_url": "https://www.asos.com/es/",
        "search_input": "input[name='q']",
        "item_container": "div.productInfo_rwyH5",
        "price_selector": "span.price__B9LP",
        "threshold": 100.00
    },
    {
        "name": "FootLocker",
        "start_url": "https://www.footlocker.es/",
        "search_input": "input[name='query']",
        "item_container": "li.product-container",
        "price_selector": "div.ProductPrice",
        "threshold": 100.00
    },
    {
        "name": "JD",
        "start_url": "https://www.jdsports.es/",
        "search_input": "input[name='q']",
        "item_container": "span.itemContainer",
        "price_selector": "span.pri",
        "threshold": 100.00
    }
]


def buscar_precios_air_force_1():
    """
    Para cada tienda, abre la URL, busca "Air Force 1" y devuelve una lista de alertas.
    Cada alerta es un dict con timestamp, store, url, price y threshold.
    """
    opts = Options()
    opts.add_argument("--start-maximized")
    opts.add_experimental_option("prefs", {
        "profile.default_content_setting_values.cookies": 2,
        "profile.block_third_party_cookies": True
    })
    driver = webdriver.Chrome(options=opts)
    wait = WebDriverWait(driver, 15)
    alertas = []

    for tienda in TIENDAS:
        driver.get(tienda["start_url"])
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, tienda["search_input"])))
        caja = driver.find_element(By.CSS_SELECTOR, tienda["search_input"])
        caja.clear()
        caja.send_keys("Air Force 1")
        caja.send_keys(Keys.RETURN)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, tienda["item_container"])))
        productos = driver.find_elements(By.CSS_SELECTOR, tienda["item_container"])
        for prod in productos:
            try:
                precio_el = prod.find_element(By.CSS_SELECTOR, tienda["price_selector"])
                txt = precio_el.text.strip()
                num = txt.replace("€", "").replace("$", "").replace(".", "").replace(",", ".")
                price = float(num)
                if price < tienda["threshold"]:
                    alertas.append({
                        "timestamp": pd.Timestamp.now(),
                        "store": tienda["name"],
                        "url": tienda["start_url"],
                        "price": price,
                        "threshold": tienda["threshold"]
                    })
            except Exception:
                continue
    driver.quit()
    return alertas


def enviar_email_alertas(alertas):
    """
    Abre Mail.app (macOS) o Outlook (Windows), compone y envía un email con alertas,
    cierra la aplicación y muestra confirmación.
    """
    # Guardar histórico en CSV
    df = pd.DataFrame(alertas)
    if not df.empty:
        if not os.path.exists(HISTORY_CSV):
            df.to_csv(HISTORY_CSV, index=False)
        else:
            df.to_csv(HISTORY_CSV, mode='a', header=False, index=False)

    # Configuración de atajos según SO
    if sys.platform == 'darwin':
        open_cmd    = ['command', 'space']
        app_name    = 'Mail'
        new_mail    = ['command', 'n']
        paste_key   = ['command', 'v']
        send_mail   = ['command', 'shift', 'd']  # two modifiers, then key
        close_app   = ['command', 'q']
    else:
        open_cmd    = ['win', 'r']
        app_name    = 'outlook'
        new_mail    = ['ctrl', 'n']
        paste_key   = ['ctrl', 'v']
        send_mail   = ['alt', 's']
        close_app   = ['alt', 'f4']

    def press_combo(combo):
        # Combo is list: [mod1, mod2, ..., key]
        *mods, key = combo
        for m in mods:
            pyautogui.keyDown(m)
        pyautogui.press(key)
        for m in reversed(mods):
            pyautogui.keyUp(m)
        time.sleep(0.5)

    # Abrir cliente de correo
    press_combo(open_cmd)
    pyautogui.write(app_name, interval=0.1)
    pyautogui.press('enter')
    time.sleep(5)

    # Nuevo mensaje
    press_combo(new_mail)

    # Campo Para: pegar destinatarios
    pyperclip.copy(','.join(EMAIL_RECIPIENTS))
    press_combo(paste_key)

    # Asunto: saltar a Asunto y pegar
    pyautogui.press('tab', presses=3, interval=0.1)
    pyperclip.copy('Alerta: precios bajos Air Force 1')
    press_combo(paste_key)

    # Cuerpo: saltar y pegar contenido
    pyautogui.press('tab')
    body_lines = [f"- {a['store']}: {a['price']} < {a['threshold']} → {a['url']}" for a in alertas]
    body = 'Se han detectado precios bajos en:\n' + '\n'.join(body_lines)
    pyperclip.copy(body)
    press_combo(paste_key)

    # Enviar correo
    press_combo(send_mail)

    # Cerrar la aplicación de correo
    press_combo(close_app)

    # Confirmación final
    pyautogui.alert(text='Correo con alertas enviado.', title='Éxito')


def proceso_monitor():
    alertas = buscar_precios_air_force_1()
    if alertas:
        enviar_email_alertas(alertas)
    else:
        pyautogui.alert(text='No hay precios por debajo del umbral.', title='Sin Alertas')


def main():
    try:
        while True:
            proceso_monitor()
            print('Esperando 1 hora...')
            time.sleep(3600)
    except KeyboardInterrupt:
        print('Monitor detenido por usuario.')

if __name__ == '__main__':
    main()
