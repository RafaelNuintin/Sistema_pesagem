from pathlib import Path
import json

from detector import Detector
from detector_video import DetectorVideo
from votador_temporal import VotadorTemporal
from balanca_simulada import BalancaSimulada
from processador import ProcessadorPesagem
from cliente_api import ClienteAPI


BASE_DIR = Path(__file__).resolve().parent.parent

CAMINHO_MODELO = BASE_DIR / "models" / "banana.pt"
CAMINHO_IMAGEM = BASE_DIR / "images" / "RipaBana.jpg"
CAMINHO_VIDEO = BASE_DIR / "videos" / "teste_bananas.mp4"

URL_API = "http://127.0.0.1:8000/api/pesagens/"

# 1. Inicializar componentes

detector = Detector(CAMINHO_MODELO)

balanca = BalancaSimulada(
    peso=12.47
)

detector_video = DetectorVideo(detector)

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

resultados = detector_video.processar_video(
    CAMINHO_VIDEO,
    intervalo_frames=5,
    confianca_minima=0.50
)

votador = VotadorTemporal(exigir_unanimidade=True)

resultado_final = votador.votar(resultados)

if not resultado_final["sucesso"]:
    print("\nPesagem não validada.")
    print(resultado_final)


else:
    balanca = BalancaSimulada(peso=12.47)

    peso = balanca.ler_peso()

    pesagem = {

        "produto": (
            list(
                resultado_final["contagem"].keys()
            )[0]
        ),

        "massa": peso,

        "contagem": (
            resultado_final["contagem"]
        ),

        "quantidade_deteccoes": sum(
            resultado_final["contagem"].values()
        ),

        "frames_analisados": (
            resultado_final["frames_analisados"]
        ),

        "votos": (
            resultado_final["votos"]
        )
    }

    print("\nPesagem final:")

    print(
        json.dumps(
            pesagem,
            indent=4,
            ensure_ascii=False
        )
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