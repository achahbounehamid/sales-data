import sqlite3
import requests
import csv

DB_PATH = "/data/ventes.db"

# ── URLs des fichiers CSV ─────────────────────────────────────────────────
URL_PRODUITS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv"

URL_MAGASINS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv"

URL_VENTES   = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv"


# ── Fonction : télécharger un CSV depuis une URL ──────────────────────────
def fetch_csv(url):
    print(f"Téléchargement en cours...")
    response = requests.get(url)
    response.encoding = 'utf-8'          
    lignes   = response.text.splitlines()
    reader   = list(csv.DictReader(lignes))
    print("Colonnes reçues :", list(reader[0].keys()))
    return reader


# ── 1. Importer les produits ──────────────────────────────────────────────
def import_produits(cursor):
    rows = fetch_csv(URL_PRODUITS)

    for row in rows:
        cursor.execute("""
            INSERT OR IGNORE INTO produits (id_produit, nom, prix, stock)
            VALUES (?, ?, ?, ?)
        """, (
            row["ID Référence produit"],
            row["Nom"],
            float(row["Prix"]),
            int(row["Stock"])
        ))

    print(f"Produits importés : {len(rows)} lignes")


# ── 2. Importer les magasins ──────────────────────────────────────────────
def import_magasins(cursor):
    rows = fetch_csv(URL_MAGASINS)

    for row in rows:
        cursor.execute("""
            INSERT OR IGNORE INTO magasins (id_magasin, ville, nombre_salaries)
            VALUES (?, ?, ?)
        """, (
            int(row["ID Magasin"]),
            row["Ville"],
            int(row["Nombre de salariés"])
        ))

    print(f"Magasins importés : {len(rows)} lignes")


# ── 3. Importer les ventes AVEC déduplication ─────────────────────────────
def import_ventes(cursor):
    rows        = fetch_csv(URL_VENTES)
    new         = 0   # compteur nouvelles ventes
    doublons    = 0   # compteur doublons ignorés

    for row in rows:
        date    = row["Date"]
        produit = row["ID Référence produit"]
        magasin = row["ID Magasin"]
        qte     = int(row["Quantité"])

        # ── Vérification : cette vente est-elle déjà en base ? ──
        cursor.execute("""
            SELECT id_vente FROM ventes
            WHERE date_vente = ?
            AND   id_produit = ?
            AND   id_magasin = ?
        """, (date, produit, magasin))

        if cursor.fetchone() is None:
            # Nouvelle vente → on insère
            cursor.execute("""
                INSERT INTO ventes (date_vente, quantite, id_produit, id_magasin)
                VALUES (?, ?, ?, ?)
            """, (date, qte, produit, magasin))
            new += 1
        else:
            # Doublon → on ignore
            doublons += 1

    print(f"Ventes nouvelles  : {new}")
    print(f"Doublons ignorés  : {doublons}")


# ── MAIN ──────────────────────────────────────────────────────────────────
def main():
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("=== IMPORT_DATA DÉMARRE ===")
    print("=== Import Produits ===")
    import_produits(cursor)

    print("=== Import Magasins ===")
    import_magasins(cursor)

    print("=== Import Ventes ===")
    import_ventes(cursor)

    conn.commit()
    conn.close()
    print("=== Import terminé ! ===")


if __name__ == "__main__":
    main()