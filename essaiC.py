import socket

# Configuration du client
HOST = '192.168.1.56'
PORT = 5555

def start_client():
    """Se connecte au serveur et reçoit ses chiffres"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("Connecté au serveur !")
    
    try:
        # Recevoir les chiffres
        data = client.recv(1024).decode('utf-8')
        print(f"Message du serveur : {data}")

        # Envoyer des messages au serveur
        while True:
            msg = input("Entrez un message (ou 'quit' pour quitter) : ")
            client.sendall(msg.encode('utf-8'))
            if msg.lower() == "quit":
                break
    except:
        print("Erreur de connexion.")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()
