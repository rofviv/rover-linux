from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time
import sys

meet_url = os.getenv('MEET_LINK', 'https://meet.jit.si/AdultRingsPlugHowever')
home_dir = os.getenv('HOME', '/home/rd2-0')

def main():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    user_data_dir = f"{home_dir}/.config/google-chrome/"
    profile = "Default"
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={profile}")

    driver_path = "/usr/local/bin/chromedriver"
    service = Service(driver_path)
    
    driver = webdriver.Chrome(service=service, options=options)

    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            window.navigator.chrome = {
                runtime: {}
            };
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3],
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
        """
    })

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
