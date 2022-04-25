import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

#cores de incialização no terminal
init()

#defina as cores disponiveis padrao
colors = [Fore.BLUE, Fore.CYAN, Fore.LIGHTRED_EX]

#escolha uma cor aleatoria para o cliente
client_color = random.choice(colors)

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002  # porta que vamos usar
separator_token = "<SEP>"  # separar o nome do cliente e a mensagem

# inicializar um soquete TCP
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}: {SERVER_PORT}...")
# conectar ao servidor
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Conectado.")
#solcitar ao cliente um nome
name = input("Digite seu nome: ")

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)
# criando uma thread que ouça as mensagens para este cliente e imprima
t = Thread(target=listen_for_messages)
# faça o daemon de encadeamento para que termine sempre que o encadeamento principal terminar
t.daemon = True
# inciar a thread
t.start()

while True:
    # mensagem de entrada que queremos enviar para o servidor
    to_send = input()
    # uma maneira de sair do programa
    if to_send.lower() == 'q':
        break
    # adicione a data, o nome e a cor do remetente
    date_now = datetime.now().strftime('%y-%m-%d %H:%M:%S')
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    # Enviar a mensagem
    s.send(to_send.encode())
# fechando o socket
s.close()