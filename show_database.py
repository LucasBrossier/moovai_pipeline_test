import duckdb

# Connexion à la base DuckDB
# Remplacer 'votre_base_duckdb.db' par le chemin de votre fichier DuckDB
con = duckdb.connect('C:\\Users\\achil\\OneDrive\\Bureau\\help_lucas\\moovitamix.db')

# Récupérer la liste des tables
tables = con.execute("SHOW TABLES").fetchall()

# Afficher les tables et leurs colonnes
for table in tables:
    table_name = table[0]
    print(f"\nTable: {table_name}")
    
    # Récupérer les colonnes de la table
    columns = con.execute(f"DESCRIBE {table_name}").fetchall()
    
    # Afficher les colonnes
    for column in columns:
        print(f"  - {column[0]} : {column[1]}")

# Fermer la connexion
con.close()
