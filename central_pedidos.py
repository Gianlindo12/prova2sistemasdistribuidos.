
import threading
import time

# Servidores simulados
principal = {
    "online": True,
    "estoque": 10
}

replica = {
    "online": True,
    "estoque": 10
}

# Controle de concorrencia
MAXIMO_SIMULTANEO = 2

semaforo = threading.Semaphore(MAXIMO_SIMULTANEO)
trava = threading.Lock()

pedidos_confirmados = []


# Funcao para sincronizar os servidores
def sincronizar():
    with trava:
        replica["estoque"] = principal["estoque"]


# Funcao para consultar o estoque
def consultar_estoque():
    if principal["online"]:
        return (
            "PRINCIPAL",
            principal["estoque"]
        )

    if replica["online"]:
        return (
            "REPLICA",
            replica["estoque"]
        )




# Funcao para processar pedidos
def processar_pedido(numero):

    with semaforo:
        time.sleep(0.1)

        with trava:
            if principal["online"] and principal["estoque"] > 0:

                principal["estoque"] -= 1

                pedidos_confirmados.append(numero)

                print(f"Pedido {numero} confirmado!")

            else:
                print(f"Pedido {numero} recusado!")


# Programa principal
print("=== CENTRAL DE PEDIDOS ===")

print(
    "Limite simultaneo:",
    MAXIMO_SIMULTANEO
)

print(
    "Estoque inicial:",
    principal["estoque"]
)


# Criacao das threads
trabalhadores = [
    threading.Thread(
        target=processar_pedido,
        args=(numero,)
    )
    for numero in [101, 102]
]


# Inicializacao das threads
for trabalhador in trabalhadores:
    trabalhador.start()


# Aguarda todas as threads terminarem
for trabalhador in trabalhadores:
    trabalhador.join()


# Exibicao dos resultados
print("\n=== RESULTADO DOS PEDIDOS ===")

print(
    "Estoque Principal:",
    principal["estoque"]
)

print(
    "Pedidos confirmados:",
    pedidos_confirmados
)

print(
    "Replica antes:",
    replica["estoque"]
)


# Sincronizacao da replica
sincronizar()

print(
    "Replica depois:",
    replica["estoque"]
)


# Simulacao de falha do servidor principal
print("\n=== SIMULACAO DE FALHA ===")

principal["online"] = False

nome, estoque = consultar_estoque()

print(
    "Consulta apos falha:",
    nome,
    estoque
)

        