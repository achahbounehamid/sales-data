import sqlite3

DB_PATH = "/data/ventes.db"

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("Database created or connected")
    return conn, cursor

def create_tables(cursor):


    # Table produits — id_produit est TEXT car REF001, REF002...
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produits (
        id_produit TEXT PRIMARY KEY,
        nom TEXT,
        prix REAL,
        stock INTEGER
    )
    """)

    # Table magasins — seulement 3 colonnes dans le CSV réel
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS magasins (
        id_magasin INTEGER PRIMARY KEY,
        ville TEXT,
        nombre_salaries INTEGER
    )
    """)

    # Table ventes — id_produit est TEXT comme dans produits
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventes (
        id_vente INTEGER PRIMARY KEY AUTOINCREMENT,
        date_vente TEXT,
        quantite INTEGER,
        id_produit TEXT,
        id_magasin INTEGER,
        FOREIGN KEY (id_produit) REFERENCES produits(id_produit),
        FOREIGN KEY (id_magasin) REFERENCES magasins(id_magasin)
    )
    """)

    # Table resultats analyses
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resultats_analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_analyse TEXT,
        valeur REAL,
        date_execution TEXT
    )
    """)

    print("Tables created")

def main():
    conn, cursor = create_database()
    create_tables(cursor)
    conn.commit()
    conn.close()
    print("Initialization completed")

if __name__ == "__main__":
    main()