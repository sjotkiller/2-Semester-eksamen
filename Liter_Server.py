# Importerer nødvendige biblioteker
import mariadb       # Til databaseforbindelse til MariaDB
import time          # Bruges til at lave pauser mellem gentagelser (sleep)
import json          # Bruges til at skrive/læse JSON-filer

# Databasekonfiguration (hardcoded credentials – ikke anbefalet i produktion)
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_PORT = 3306

# Sti til JSON-fil
DATA_JSON_PATH = "data.json"

# Funktion til at hente antal liter drukket fra databasen "ølbord"
def hent_liter_drukket():
    try:
        # Opret forbindelse til MariaDB
        conn = mariadb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database="ølbord"  # Vælg database
        )
        cur = conn.cursor()  # Opret en cursor til at køre SQL-kommandoer
        cur.execute("SELECT liter_drukket FROM drikke_logg WHERE id = 1")  # Hent liter drukket
        result = cur.fetchone()  # Få første (og eneste) resultat
        conn.close()  # Luk forbindelsen
        return float(result[0]) if result else 0.0  # Returner resultat som float, eller 0 hvis intet
    except:
        return 0.0  # Ved fejl, returner 0.0 (fail-safe)

# Funktion til at hente literprisen for en bestemt øl (Carlsberg)
def hent_pris_carlsberg():
    try:
        conn = mariadb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database="øl"  # Skift af database 
        )
        cur = conn.cursor()
        cur.execute("SELECT price FROM øl WHERE id = 5")  # Antager at ID 5 er Carlsberg
        result = cur.fetchone()
        conn.close()
        return float(result[0]) if result else 0.0
    except:
        return 0.0

# Main loop – Programmet kører løbende
if name == "main":
    try:
        while True:
            liter = hent_liter_drukket()  # Hent nyeste liter-data fra databasen
            pris = hent_pris_carlsberg()  # Hent literprisen fra databasen

            # Konstruer et dataobjekt med liter og samlet pris
            data = {
                "liter": round(liter, 2),  # Afrundet til 2 decimaler
                "total_price": round(liter * pris, 2)
            }

            # Skriv data til JSON-fil – bruges af frontend til visning
            with open(DATA_JSON_PATH, "w") as f:
                json.dump(data, f)

            time.sleep(1)  # Vent 1 sekund før næste måling
    except KeyboardInterrupt:
        print("Stopper...")  # Stop progrma med Ctrl+C
