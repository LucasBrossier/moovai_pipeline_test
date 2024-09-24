import requests
import duckdb

# URL de base de l'API
BASE_URL = "http://127.0.0.1:8000"  # Remplace par l'URL de déploiement de l'API

# Fonction pour récupérer les tracks depuis l'API
def get_tracks(page: int = 1, size: int = 100):
    response = requests.get(f"{BASE_URL}/tracks", params={"page": page, "size": size})
    if response.status_code == 200:
        data = response.json()
        print("Structure de la réponse des tracks :", data)
        tracks = data.get('items')
        if tracks:
            return tracks
        else:
            print("Erreur : la clé 'items' est absente de la réponse ou vide.")
            return None
    else:
        print(f"Erreur lors de la récupération des tracks: {response.status_code}")
        return None

# Fonction pour récupérer les utilisateurs depuis l'API
def get_users(page: int = 1, size: int = 100):
    response = requests.get(f"{BASE_URL}/users", params={"page": page, "size": size})
    if response.status_code == 200:
        data = response.json()
        print("Structure de la réponse des utilisateurs :", data)
        users = data.get('items')
        if users:
            return users
        else:
            print("Erreur : la clé 'items' est absente de la réponse ou vide.")
            return None
    else:
        print(f"Erreur lors de la récupération des utilisateurs: {response.status_code}")
        return None

# Fonction pour récupérer l'historique d'écoute depuis l'API
def get_listen_history(page: int = 1, size: int = 100):
    response = requests.get(f"{BASE_URL}/listen_history", params={"page": page, "size": size})
    if response.status_code == 200:
        data = response.json()
        print("Structure de la réponse de l'historique d'écoute :", data)
        listen_history = data.get('items')
        if listen_history:
            return listen_history
        else:
            print("Erreur : la clé 'items' est absente de la réponse ou vide.")
            return None
    else:
        print(f"Erreur lors de la récupération de l'historique d'écoute: {response.status_code}")
        return None

# Fonction pour créer la table et insérer les tracks dans DuckDB
def save_tracks_to_duckdb(tracks):
    if not tracks:
        print("Aucun track à insérer.")
        return

    con = duckdb.connect('src_tracks.duckdb')
    con.execute('''
        CREATE TABLE IF NOT EXISTS src_tracks (
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

    for track in tracks:
        if isinstance(track, dict):
            try:
                con.execute('''
                    INSERT INTO src_tracks (
                        id, name, artist, songwriters, duration, genres, album, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                print(f"Erreur lors de l'insertion des données : {e}")
        else:
            print("Erreur : un des éléments de tracks n'est pas un dictionnaire")

    con.close()
    print("Données des tracks stockées dans DuckDB")

# Fonction pour créer la table et insérer les utilisateurs dans DuckDB
def save_users_to_duckdb(users):
    if not users:
        print("Aucun utilisateur à insérer.")
        return

    con = duckdb.connect('src_users.duckdb')
    con.execute('''
        CREATE TABLE IF NOT EXISTS src_users (
            id VARCHAR,
            name VARCHAR,
            email VARCHAR,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
    ''')

    for user in users:
        if isinstance(user, dict):
            try:
                con.execute('''
                    INSERT INTO src_users (
                        id, name, email, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?)
                ''', (
                    user.get('id'),
                    user.get('name'),
                    user.get('email'),
                    user.get('created_at'),
                    user.get('updated_at')
                ))
            except Exception as e:
                print(f"Erreur lors de l'insertion des données : {e}")
        else:
            print("Erreur : un des éléments de users n'est pas un dictionnaire")

    con.close()
    print("Données des utilisateurs stockées dans DuckDB")

# Fonction pour créer la table et insérer l'historique d'écoute dans DuckDB
def save_listen_history_to_duckdb(listen_history):
    if not listen_history:
        print("Aucun historique d'écoute à insérer.")
        return

    con = duckdb.connect('src_listen_history.duckdb')
    con.execute('''
        CREATE TABLE IF NOT EXISTS src_listen_history (
            user_id VARCHAR,
            track_id VARCHAR,
            listen_timestamp TIMESTAMP
        )
    ''')

    for record in listen_history:
        if isinstance(record, dict):
            try:
                con.execute('''
                    INSERT INTO src_listen_history (
                        user_id, track_id, listen_timestamp
                    ) VALUES (?, ?, ?)
                ''', (
                    record.get('user_id'),
                    record.get('track_id'),
                    record.get('listen_timestamp')
                ))
            except Exception as e:
                print(f"Erreur lors de l'insertion des données : {e}")
        else:
            print("Erreur : un des éléments de listen_history n'est pas un dictionnaire")

    con.close()
    print("Données de l'historique d'écoute stockées dans DuckDB")

# Exemple d'utilisation
if __name__ == "__main__":
    tracks = get_tracks()
    if tracks:
        save_tracks_to_duckdb(tracks)

    users = get_users()
    if users:
        save_users_to_duckdb(users)

    listen_history = get_listen_history()
    if listen_history:
        save_listen_history_to_duckdb(listen_history)