from detector import Detector
from balanca_simulada import BalancaSimulada
from processador import ProcessadorPesagem
from cliente_api import ClienteAPI


CAMINHO_MODELO = "../models/banana.pt"
CAMINHO_IMAGEM = "../images/RipaBana.jpg"

URL_API = "http://127.0.0.1:8000/api/pesagens/"


# 1. Inicializar componentes

detector = Detector(CAMINHO_MODELO)

balanca = BalancaSimulada(
    peso=12.47
)

processador = ProcessadorPesagem(
    confianca_minima=0.50
)

api = ClienteAPI(
    URL_API
)


# 2. Executar inferência

resultado_yolo = detector.detectar(
    CAMINHO_IMAGEM
)


# 3. Determinar produto

resultado = processador.processar(
    resultado_yolo
)


if resultado is None:

    print("Nenhum produto identificado com confiança suficiente.")

else:

    # 4. Ler peso

    peso = balanca.ler_peso()


    # 5. Montar registro

    pesagem = {

        "produto": resultado["produto"],

        "massa": peso,

        "contagem": resultado["contagem"],

        "quantidade_deteccoes":
            resultado["quantidade_deteccoes"]

    }


    print("\nPesagem:")
    print(pesagem)


    # 6. Enviar para Django

    resposta = api.registrar_pesagem(
        pesagem
    )

    print("\nServidor:")
    print(resposta)