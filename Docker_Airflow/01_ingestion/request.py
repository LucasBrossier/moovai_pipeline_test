import requests
import duckdb

# URL de base de l'API
BASE_URL = "http://127.0.0.1:8000"  # Remplace par l'URL de déploiement de l'API

# Fonction pour récupérer les tracks depuis l'API
def get_tracks(page: int = 1, size: int = 100):
    response = requests.get(f"{BASE_URL}/tracks", params={"page": page, "size": size})
    if response.status_code == 200:
        data = response.json()
        print("Structure de la réponse :", data)
        tracks = data.get('items')  # Vérifie que 'items' contient la liste des tracks
        if tracks:
            return tracks
        else:
            print("Erreur : la clé 'items' est absente de la réponse ou vide.")
            return None
    else:
        print(f"Erreur lors de la récupération des tracks: {response.status_code}")
        return None


import duckdb


# Fonction pour créer la table et insérer les tracks dans DuckDB
def save_tracks_to_duckdb(tracks):
    if not tracks:
        print("Aucun track à insérer.")
        return

    # Connexion à DuckDB et création de la table si nécessaire
    con = duckdb.connect('src_tracks')  # Utilisation d'un fichier DuckDB
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

    # Insertion des tracks dans DuckDB
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

    # Fermeture de la connexion DuckDB
    con.close()
    print("Données des tracks stockées dans DuckDB")

# Exemple d'utilisation
if __name__ == "__main__":
    tracks = get_tracks()
    if tracks:
        save_tracks_to_duckdb(tracks)
        print("Données des tracks stockées dans DuckDB")