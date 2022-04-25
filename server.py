import socket
from threading import Thread

# Endereço IP do servidor
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002  # porta que vamos usar
separator_token = "<SEP>"  # separar o nome do cliente e a mensagem

# inicializaremos todos os soquetes do cliente conectado
client_sockets = set()
# criamos um soquete TCP
s = socket.socket()
# porta reutlizavel
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# vincular o soquete ao endereço que especificamos
s.bind((SERVER_HOST, SERVER_PORT))
# Escutamos as proximas conexoes
s.listen(5)
print(f"[*] Ouvindo o {SERVER_HOST}: {SERVER_PORT}")


def listen_for_clients(cs):
    """
    Escutamos as mensagens do soquete do cliente onde a mensagem for recebida
     e transmita-a para todos os outros clientes conectados
    """
    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            # cliente nao esta mais conectado
            # vamos remover do conjunto da lista
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            # se recebermos uma mensagem, substitua o <SEP>
            # token com ": "
            msg = msg.replace(separator_token, ": ")
        # iterar em todos os soquetes conectados
        for client_socket in client_sockets:
            # enviar mensagem
            client_socket.send(msg.encode())
while True:
    #continuamos ouvindo novas conexões o tempo todo
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} conectado")
    #adicione o novo cliente conectado aos soquetes conectados
    client_sockets.add(client_socket)
    # inciar um novo thread que escute as mensagens de cada cliente
    t = Thread(target=listen_for_clients, args=(client_socket,))
    # terminando sempre que o encadeamento principal terminar
    t.daemon = True
    # iniciar a thread
    t.start()
for cs in client_sockets:
    cs.close()
# fechar o soquete do servidor
s.close()