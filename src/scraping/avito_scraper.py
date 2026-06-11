import requests
import json
import re
import csv
import time
import random

# =========================
# CONFIG
# =========================

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
}

toutes_annonces = []

MAX_PAGES = 100

# =========================
# SCRAPING
# =========================

for page in range(1, MAX_PAGES + 1):

    url = f"https://www.avito.ma/fr/maroc/appartements-a_vendre?o={page}"

    print(f"\nPage {page}/{MAX_PAGES}...")

    try:
        #telechargement de la page avec gestion des erreurs, on envoi des requetes http ver avito
        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )
        #si avito repond avec une erreur http, on affiche l'erreur 
        response.raise_for_status()

        # =========================
        # EXTRACTION JSON NEXT DATA
        # =========================
            #les sites nextjs stock les données dans next data 
        match = re.search(
            r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
            response.text,
            re.DOTALL
        ) 

        if not match:
            print(f"Aucune donnée trouvée page {page}")
            continue
            #conversion (json a dictionnaire python)
        data = json.loads(match.group(1))

        # =========================
        # RECUPERATION ADS
        # =========================
            #on descend dans l'arbre json 
        ads = (
            data
            .get("props", {})
            .get("pageProps", {})
            .get("componentProps", {})
            .get("ads", {})
            .get("ads", [])
        )

        print(f"{len(ads)} annonces trouvées")

        # =========================
        # EXTRACTION DONNEES
        # =========================

        for ad in ads:

            try:

                params = {
                    p["key"]: p["value"]
                    for p in ad.get("params", {}).get("secondary", [])
                }

                toutes_annonces.append({
                    "id": ad.get("id"),
                    "titre": ad.get("subject"),
                    "prix": ad.get("price", {}).get("value"),
                    "surface": params.get("size"),
                    "chambres": params.get("rooms"),
                    "salles_de_bain": params.get("bathrooms"),
                    "etage": params.get("floor"),
                    "localisation": ad.get("location"),
                    "vendeur": ad.get("seller", {}).get("name"),
                    "type_vendeur": ad.get("seller", {}).get("type"),
                    "date": ad.get("date"),
                    "lien": (
                        "https://www.avito.ma" + ad.get("href", "")
                        if ad.get("href")
                        else None
                    ),
                })

            except Exception as e:
                print(f"Erreur annonce : {e}")

        # =========================
        # ANTI BLOCK
        # =========================

        sleep_time = random.uniform(2, 5)

        print(f"Pause {sleep_time:.2f}s")

        time.sleep(sleep_time)

    # =========================
    # GESTION ERREURS
    # =========================

    except requests.exceptions.Timeout:
        print(f"Timeout page {page}")
        continue

    except requests.exceptions.ConnectionError:
        print(f"Erreur connexion page {page}")
        time.sleep(10)
        continue

    except requests.exceptions.HTTPError as e:
        print(f"Erreur HTTP : {e}")
        continue

    except requests.exceptions.RequestException as e:
        print(f"Erreur Requests : {e}")
        continue

    except json.JSONDecodeError:
        print(f"Erreur JSON page {page}")
        continue

    except Exception as e:
        print(f"Erreur générale : {e}")
        continue

# =========================
# SAVE CSV
# =========================

import os

if toutes_annonces:

    output_file = "data/raw/avito_annonces_multipages.csv"

    # créer data/raw automatiquement
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8-sig", newline="") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=toutes_annonces[0].keys() #prepare les colones 
        )

        writer.writeheader()
        writer.writerows(toutes_annonces)

    print("\n=========================")
    print("SCRAPING TERMINE")
    print("=========================")
    print(f"Total annonces : {len(toutes_annonces)}")
    print(f"Fichier : {output_file}")

else:
    print("Aucune annonce récupérée")