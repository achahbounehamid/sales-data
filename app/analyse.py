import sqlite3
from datetime import datetime

DB_PATH = "/data/ventes.db"


# ── Fonction pour sauvegarder un résultat en base ────────────────────────
def sauvegarder_resultat(cursor, nom_analyse, valeur):
    cursor.execute("""
        INSERT INTO resultats_analyses (nom_analyse, valeur, date_execution)
        VALUES (?, ?, ?)
    """, (nom_analyse, valeur, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


# ── 1. Chiffre d'affaires total ───────────────────────────────────────────
def analyse_ca_total(cursor):
    cursor.execute("""
        SELECT SUM(v.quantite * p.prix) AS ca_total
        FROM ventes v
        JOIN produits p ON v.id_produit = p.id_produit
    """)
    resultat = cursor.fetchone()[0]
    print(f"Chiffre d'affaires total : {resultat:.2f} €")
    sauvegarder_resultat(cursor, "ca_total", resultat)


# ── 2. Ventes par produit ─────────────────────────────────────────────────
def analyse_ventes_par_produit(cursor):
    cursor.execute("""
        SELECT p.nom,
               SUM(v.quantite)            AS total_quantite,
               SUM(v.quantite * p.prix)   AS ca_produit
        FROM ventes v
        JOIN produits p ON v.id_produit = p.id_produit
        GROUP BY p.nom
        ORDER BY ca_produit DESC
    """)
    resultats = cursor.fetchall()

    print("\nVentes par produit :")
    for nom, qte, ca in resultats:
        print(f"  {nom} → {qte} unités → {ca:.2f} €")
        sauvegarder_resultat(cursor, f"ca_produit_{nom}", ca)


# ── 3. Ventes par région (ville) ──────────────────────────────────────────
def analyse_ventes_par_region(cursor):
    cursor.execute("""
        SELECT m.ville,
               SUM(v.quantite)            AS total_quantite,
               SUM(v.quantite * p.prix)   AS ca_region
        FROM ventes v
        JOIN magasins m  ON v.id_magasin  = m.id_magasin
        JOIN produits p  ON v.id_produit  = p.id_produit
        GROUP BY m.ville
        ORDER BY ca_region DESC
    """)
    resultats = cursor.fetchall()

    print("\nVentes par ville :")
    for ville, qte, ca in resultats:
        print(f"  {ville} → {qte} unités → {ca:.2f} €")
        sauvegarder_resultat(cursor, f"ca_ville_{ville}", ca)


# ── MAIN ──────────────────────────────────────────────────────────────────
def main():
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=== Analyse des ventes ===")
    analyse_ca_total(cursor)
    analyse_ventes_par_produit(cursor)
    analyse_ventes_par_region(cursor)

    conn.commit()
    conn.close()
    print("\nRésultats sauvegardés en base !")


if __name__ == "__main__":
    main()