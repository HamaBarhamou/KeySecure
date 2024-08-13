import requests
import time

# Liste des URLs des nœuds Keycloak
urls = [
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:8082",
]

def get_access_token():
    # Obtenir le jeton d'accès en s'authentifiant sur le serveur Keycloak
    token_url = f"{urls[0]}/realms/master/protocol/openid-connect/token"
    data = {
        "client_id": "admin-cli",
        "username": "admin",
        "password": "admin",
        "grant_type": "password"
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("Jeton d'accès obtenu avec succès.")
        return access_token
    else:
        print(f"Erreur lors de l'obtention du jeton d'accès: {response.status_code} - {response.text}")
        return None

def create_realm(url, access_token):
    print(f"Création du Realm sur {url}")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "realm": "test-realm",
        "enabled": True
    }
    response = requests.post(f"{url}/admin/realms", headers=headers, json=data)
    if response.status_code == 201:
        print(f"Realm créé avec succès sur {url}")
    else:
        print(f"Erreur lors de la création du Realm sur {url}: {response.status_code} - {response.text}")

def check_realm_replication(urls):
    for url in urls:
        print(f"Vérification du Realm sur {url}/realms/test-realm")
        response = requests.get(f"{url}/realms/test-realm")
        if response.status_code == 200:
            print(f"Realm trouvé sur {url}")
        else:
            print(f"Realm NON trouvé sur {url}")

if __name__ == "__main__":
    # Obtenir le jeton d'accès
    access_token = get_access_token()
    
    if access_token:
        # Créer le Realm sur le premier nœud
        create_realm(urls[0], access_token)
        
        # Attendre un peu pour laisser le temps aux autres nœuds de synchroniser
        time.sleep(10)
        
        # Vérifier la réplication
        check_realm_replication(urls)
