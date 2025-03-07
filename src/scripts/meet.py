from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import os
import time
import sys

meet_url = os.getenv('MEET_LINK', 'https://meet.jit.si/AdultRingsPlugHowever')


def main():
    service = Service("/snap/bin/firefox.geckodriver")
    
    # Configurar las opciones de Firefox
    options = webdriver.FirefoxOptions()
    
    # Configurar permisos para cámara y micrófono
    options.set_preference("media.navigator.permission.disabled", True)
    options.set_preference("media.navigator.streams.fake", False)
    options.set_preference("permissions.default.microphone", 1)
    options.set_preference("permissions.default.camera", 1)
    
    # Crear el driver con las opciones configuradas
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get(meet_url)
        time.sleep(5)

        elem = driver.find_element(By.ID, "premeeting-name-input")
        elem.clear()
        elem.send_keys("ROBOT")
        elem.send_keys(Keys.RETURN)

        print("El navegador está abierto con los ajustes de ocultación. Presiona Ctrl+C para cerrar manualmente.")
        
        while True:
            if driver.title == "":
                print("El navegador se cerró. Finalizando el script.")
                sys.exit(0)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCerrando el navegador...")
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
