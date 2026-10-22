import socket
import threading

clientes = {}

lock_clientes = threading.Lock()


def enviar_para_todos(mensagem, remetente=None):

    for cliente in list(clientes):

        if cliente != remetente:

            try:
                cliente.sendall(mensagem.encode())

            except:
                pass


def listar_usuarios():
    
    with lock_clientes:

        if not clientes:
            return "Nenhum usuário conectado.\n"

        mensagem = "Usuários conectados:\n"

        for nome in clientes.values():
            mensagem += f"- {nome}\n"

        return mensagem


def atender_cliente(conexao, endereco):

    nome = "Anônimo"

    try:

        conexao.sendall("Digite seu nome: ".encode())

        nome_recebido = conexao.recv(1024).decode().strip()

        if nome_recebido:
            nome = nome_recebido

        clientes[conexao] = nome

        print(f"{nome} entrou no chat.")

        enviar_para_todos(
            f"[SISTEMA] {nome} entrou no chat.\n",
            conexao
        )

        while True:

            mensagem = conexao.recv(1024)

            if not mensagem:
                break

            mensagem = mensagem.decode().strip()

            # Comando para sair
            if mensagem.lower() == "/sair":
                break

            # Comando para listar usuários
            if mensagem.lower() == "/usuarios":

                resposta = listar_usuarios()

                conexao.sendall(resposta.encode())

                continue

            print(f"[{nome}]: {mensagem}")

            enviar_para_todos(
                f"[{nome}]: {mensagem}\n",
                conexao
            )

    except ConnectionError:

        pass

    finally:

        if conexao in clientes:

            del clientes[conexao]

            print(f"{nome} saiu do chat.")

            enviar_para_todos(
                f"[SISTEMA] {nome} saiu do chat.\n"
            )

        conexao.close()


servidor = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

servidor.bind(("0.0.0.0", 5000))

servidor.listen()

print("================================")
print("       CHAT DISTRIBUÍDO")
print("================================")
print("Servidor iniciado!")
print("Aguardando clientes...\n")


while True:

    conexao, endereco = servidor.accept()

    thread = threading.Thread(
        target=atender_cliente,
        args=(conexao, endereco)
    )

    thread.daemon = True

    thread.start()