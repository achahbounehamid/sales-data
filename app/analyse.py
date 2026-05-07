import sqlite3
from datetime import datetime

DB_PATH = "/data/ventes.db"


# ── Sauvegarder un résultat en base ──────────────────────────────────────
def sauvegarder_resultat(cursor, nom_analyse, valeur):
    cursor.execute("""
        INSERT INTO resultats_analyses (nom_analyse, valeur, date_execution)
        VALUES (?, ?, ?)
    """, (nom_analyse, valeur, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


# ── a. Chiffre d'affaires total ───────────────────────────────────────────
def analyse_ca_total(cursor):
    cursor.execute("""
        SELECT ROUND(SUM(v.quantite * p.prix), 2) AS ca_total
        FROM ventes v
        JOIN produits p ON v.id_produit = p.id_produit
    """)
    resultat = cursor.fetchone()[0]

    if resultat is None:
        print("Aucune vente trouvée !")
        return

    print(f"Chiffre d affaires total : {resultat} €")
    sauvegarder_resultat(cursor, "ca_total", resultat)


# ── b. Ventes par produit ─────────────────────────────────────────────────
def analyse_ventes_par_produit(cursor):
    cursor.execute("""
        SELECT
            p.nom                          AS produit,
            SUM(v.quantite)                AS total_quantite,
            ROUND(SUM(v.quantite * p.prix), 2) AS ca_produit
        FROM ventes v
        JOIN produits p ON v.id_produit = p.id_produit
        GROUP BY p.nom
        ORDER BY ca_produit DESC
    """)
    resultats = cursor.fetchall()

    print("\nVentes par produit :")
    print(f"  {'Produit':<15} {'Quantité':>10} {'CA (€)':>10}")
    print(f"  {'-'*15} {'-'*10} {'-'*10}")

    for nom, qte, ca in resultats:
        print(f"  {nom:<15} {qte:>10} {ca:>10} €")
        sauvegarder_resultat(cursor, f"ca_produit_{nom}", ca)


# ── c. Ventes par région (ville) ──────────────────────────────────────────
def analyse_ventes_par_region(cursor):
    cursor.execute("""
        SELECT
            m.ville                            AS ville,
            SUM(v.quantite)                    AS total_quantite,
            ROUND(SUM(v.quantite * p.prix), 2) AS ca_ville
        FROM ventes v
        JOIN magasins m  ON v.id_magasin  = m.id_magasin
        JOIN produits p  ON v.id_produit  = p.id_produit
        GROUP BY m.ville
        ORDER BY ca_ville DESC
    """)
    resultats = cursor.fetchall()

    print("\nVentes par ville :")
    print(f"  {'Ville':<15} {'Quantité':>10} {'CA (€)':>10}")
    print(f"  {'-'*15} {'-'*10} {'-'*10}")

    for ville, qte, ca in resultats:
        print(f"  {ville:<15} {qte:>10} {ca:>10} €")
        sauvegarder_resultat(cursor, f"ca_ville_{ville}", ca)


# ── MAIN ──────────────────────────────────────────────────────────────────
def main():
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        print("=== ANALYSE DES VENTES ===")

        print("\n--- a. Chiffre d affaires total ---")
        analyse_ca_total(cursor)

        print("\n--- b. Ventes par produit ---")
        analyse_ventes_par_produit(cursor)

        print("\n--- c. Ventes par region ---")
        analyse_ventes_par_region(cursor)

        conn.commit()
        print("\nResultats sauvegardes en base !")

    except Exception as e:
        conn.rollback()
        print(f"Erreur analyse : {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()