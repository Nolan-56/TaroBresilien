import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.137.1"  # Remplacez par l'adresse IP de votre serveur
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
        except Exception as e:
            print(f"Impossible de se connecter au serveur : {e}")

    def send(self, data):
        try:
            self.client.send(data.encode('utf-8'))
        except Exception as e:
            print(f"Erreur lors de l'envoi des données : {e}")

    def receive(self):
        try:
            return self.client.recv(2048).decode('utf-8')
        except Exception as e:
            print(f"Erreur lors de la réception des données : {e}")
            return None
