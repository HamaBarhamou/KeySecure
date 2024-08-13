import random
import time
import docker

# Connexion au client Docker
client = docker.from_env()

# Liste des conteneurs Keycloak
containers = ["keycloak-clustered-1", "keycloak-clustered-2", "keycloak-clustered-3", "keycloak-clustered-4"]

def restart_random_container(containers):
    container_name = random.choice(containers)
    print(f"Redémarrage du conteneur : {container_name}")
    container = client.containers.get(container_name)
    container.restart()
    time.sleep(20)  # Attendre que le conteneur redémarre

    # Vérifier l'état du conteneur
    container.reload()
    if container.status == 'running':
        print(f"Le conteneur {container_name} est de nouveau en ligne.")
    else:
        print(f"Le conteneur {container_name} n'a pas pu redémarrer correctement.")
        exit(1)

if __name__ == "__main__":
    for _ in range(3):  # Nombre de redémarrages
        restart_random_container(containers)
    print("Tous les tests de redémarrage ont réussi.")
