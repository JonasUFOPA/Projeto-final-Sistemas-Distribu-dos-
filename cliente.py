import socket
import threading

IP_SERVIDOR = "192.168.76.42"
PORTA = 5000


def receber_mensagens(cliente):

    while True:

        try:

            mensagem = cliente.recv(1024)

            if not mensagem:

                print("\nServidor desconectado.")
                break

            print("\n" + mensagem.decode(), end="")

            print("Você: ", end="", flush=True)

        except ConnectionError:

            print("\nConexão encerrada.")
            break


cliente = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

cliente.connect((IP_SERVIDOR, PORTA))


mensagem = cliente.recv(1024).decode()

print(mensagem, end="")

nome = input()

cliente.sendall(nome.encode())


print(f"\nBem-vindo ao chat, {nome}!")

print("Digite suas mensagens.")

print("Comandos disponíveis:")

print("  /usuarios - lista os usuários conectados")

print("  /sair     - sair do chat")

print()


thread_receber = threading.Thread(
    target=receber_mensagens,
    args=(cliente,)
)

thread_receber.daemon = True

thread_receber.start()


while True:

    mensagem = input("Você: ")

    if mensagem.lower() == "/sair":

        cliente.sendall("/sair".encode())

        break

    try:

        cliente.sendall(mensagem.encode())

    except ConnectionError:

        print("Não foi possível enviar a mensagem.")

        break


cliente.close()