import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def get_driver():
    """Crée et retourne un navigateur Chrome automatisé."""
    options = Options()
    options.add_argument("--headless")  # pas d'interface graphique
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


def attendre():
    """Attend entre 2 et 4 secondes pour éviter d'être bloqué."""
    time.sleep(random.uniform(2, 4))