import socket
import threading
import random

# Configuration du serveur
HOST = '0.0.0.0'
PORT = 5555

# Liste des connexions clients
clients = []

# Générer des chiffres pour chaque joueur
player_numbers = {}

def handle_client(conn, addr, player_id):
    """Gère un client spécifique"""
    print(f"Connexion établie avec {addr}. Joueur ID : {player_id}")
    try:
        # Générer les chiffres aléatoires pour ce joueur
        player_numbers[player_id] = [random.randint(1, 100) for _ in range(5)]
        print(f"Chiffres pour le joueur {player_id} : {player_numbers[player_id]}")

        # Envoyer les chiffres au client
        conn.sendall(f"Vos chiffres : {player_numbers[player_id]}".encode('utf-8'))

        # Écouter les messages du client
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data or data.lower() == "quit":
                print(f"Le joueur {player_id} s'est déconnecté.")
                break
            print(f"Message du joueur {player_id} : {data}")
    except:
        print(f"Erreur avec le joueur {player_id}.")
    finally:
        conn.close()
        del player_numbers[player_id]

def start_server():
    """Démarre le serveur et accepte les connexions des clients"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Serveur démarré sur {HOST}:{PORT}")
    
    player_id = 0
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        player_id += 1
        thread = threading.Thread(target=handle_client, args=(conn, addr, player_id))
        thread.start()

if __name__ == "__main__":
    start_server()
