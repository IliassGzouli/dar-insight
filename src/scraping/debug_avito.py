from src.scraping.utils import get_driver, attendre

driver = get_driver()
driver.get("https://www.avito.ma/fr/maroc/appartements-à_vendre")
attendre()

with open("data/raw/avito_debug.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

print("HTML sauvegardé → data/raw/avito_debug.html")
driver.quit()
