import duckdb

# Chemin vers ta base de données DuckDB
db_path = '/Users/brossierlucas/programmation/moovai_pipeline_test/src/01_ingestion/moovai_data.duckdb'

# Connexion à la base de données DuckDB
con = duckdb.connect(db_path)

# Requête pour obtenir les colonnes et leur type dans la table users
columns_query = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'src_users';"

# Exécution de la requête
columns_info = con.execute(columns_query).fetchall()

# Affichage des résultats
print("Colonnes de la table users et leur type :")
for column in columns_info:
    print(f"Nom de colonne : {column[0]}, Type : {column[1]}")

# Fermeture de la connexion
con.close()