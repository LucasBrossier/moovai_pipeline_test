import duckdb

# Chemin vers ta base de données DuckDB
db_path = '/Users/brossierlucas/programmation/moovai_pipeline_test/src/01_ingestion/moovai_data.duckdb'

# Connexion à la base de données DuckDB
con = duckdb.connect(db_path)

# Requête pour obtenir la liste des tables
tables_query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main';"

# Exécution de la requête
tables = con.execute(tables_query).fetchall()

# Affichage des résultats
print("Tables dans la base de données :")
for table in tables:
    print(table[0])

# Fermeture de la connexion
con.close()