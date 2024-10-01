import requests
import duckdb

# URL de base de l'API
BASE_URL = "http://192.168.0.55:8000"

# Fonction générique pour récupérer toutes les données depuis l'API
def get_all_data():
    data = {}
    for data_type in ['tracks', 'users', 'listen_history']:
        page = 1
        items = []
        while True:
            url = f"{BASE_URL}/{data_type}"
            response = requests.get(url, params={"page": page, "size": 100}, timeout=10)
            if response.status_code == 200:
                data_chunk = response.json()
                items.extend(data_chunk.get('items', []))
                if len(data_chunk.get('items', [])) < 100:  # Si moins de 100 items, on est à la dernière page
                    break
                page += 1
            else:
                print(f"Erreur lors de la récupération des {data_type}: {response.status_code}")
                break
        data[data_type] = items
    return data

# Connexion à DuckDB
def get_duckdb_connection():
    return duckdb.connect('data/moovitamix.db')

# Fonction pour créer les tables et insérer les données dans DuckDB
def save_data_to_duckdb(data):
    con = get_duckdb_connection()

    # Création des tables
    con.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            id VARCHAR,
            name VARCHAR,
            artist VARCHAR,
            songwriters VARCHAR,
            duration VARCHAR,
            genres VARCHAR,
            album VARCHAR,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
    ''')
    con.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR,
            first_name VARCHAR,
            last_name VARCHAR,
            email VARCHAR,
            gender VARCHAR,
            favorite_genres VARCHAR,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
    ''')
    con.execute('''
        CREATE TABLE IF NOT EXISTS listen_history (
            user_id VARCHAR,
            items INTEGER,
            created_at TIMESTAMP
        )
    ''')

    # Insertion des tracks
    if data.get('tracks'):
        for track in data['tracks']:
            if isinstance(track, dict):
                try:
                    con.execute('''
                        INSERT INTO tracks (id, name, artist, songwriters, duration, genres, album, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        track.get('id'),
                        track.get('name'),
                        track.get('artist'),
                        track.get('songwriters'),
                        track.get('duration'),
                        track.get('genres'),
                        track.get('album'),
                        track.get('created_at'),
                        track.get('updated_at')
                    ))
                except Exception as e:
                    print(f"Erreur lors de l'insertion des données des tracks pour l'ID {track.get('id')} : {e}")

    # Insertion des utilisateurs
    if data.get('users'):
        for user in data['users']:
            if isinstance(user, dict):
                try:
                    con.execute('''
                        INSERT INTO users (id, first_name, last_name, email, gender, favorite_genres, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        user.get('id'),
                        user.get('first_name'),
                        user.get('last_name'),
                        user.get('email'),
                        user.get('gender'),
                        user.get('favorite_genres'),
                        user.get('created_at'),
                        user.get('updated_at')
                    ))
                except Exception as e:
                    print(f"Erreur lors de l'insertion des données des utilisateurs pour l'ID {user.get('id')} : {e}")

    # Insertion de l'historique d'écoute avec prise en charge de 'items' en tant qu'entier
    if data.get('listen_history'):
        for record in data['listen_history']:
            if isinstance(record, dict):
                user_id = record.get('user_id')
                items = record.get('items', [])  # Utilisation du champ 'items' qui est une liste
                created_at = record.get('created_at')  # Utilisation de 'created_at' comme timestamp d'écoute

                print(f"Utilisateur: {user_id}, Items: {items}, Created At: {created_at}")

                # Insertion de chaque item de la liste 'items'
                for item in items:
                    if isinstance(item, (int, str)):  # Vérifie que 'item' est bien un 'track_id'
                        try:
                            con.execute('''
                                INSERT INTO listen_history (user_id, items, created_at)
                                VALUES (?, ?, ?)
                            ''', (
                                user_id,
                                int(item),  # 'item' est maintenant un entier
                                created_at
                            ))
                        except Exception as e:
                            print(f"Erreur lors de l'insertion de l'historique d'écoute pour l'utilisateur {user_id} et le track {item} : {e}")


    con.close()
    print("Toutes les données stockées dans DuckDB")


# Fonction principale à appeler depuis Airflow
def execute_data_ingestion():
    data = get_all_data()
    save_data_to_duckdb(data)
