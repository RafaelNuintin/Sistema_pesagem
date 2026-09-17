from pathlib import Path

import json

from detector import Detector

from detector_video import DetectorVideo

from votador_temporal import VotadorTemporal

from balanca_simulada import BalancaSimulada

from cliente_api import ClienteAPI


BASE_DIR = (
    Path(__file__).resolve().parent.parent
)


CAMINHO_MODELO = (
    BASE_DIR / "models" / "banana.pt"
)

CAMINHO_VIDEO = (
    BASE_DIR / "videos" / "teste_bananas.mp4"
)

CAMINHO_VIDEO_SAIDA = (
    BASE_DIR / "videos" / "teste_bananas_tracking.mp4"
)

URL_API = (
    "http://127.0.0.1:8000/api/pesagens/"
)


# =====================================================
# 1. Inicializar componentes
# =====================================================

detector = Detector(
    CAMINHO_MODELO
)

detector_video = DetectorVideo(
    detector,
    tracker="bytetrack.yaml"
)

votador = VotadorTemporal(

    razao_minima=0.80,

    observacoes_minimas=3

)

balanca = BalancaSimulada(
    peso=12.47
)

api = ClienteAPI(
    URL_API
)


# =====================================================
# 2. Processar vídeo
# =====================================================

resultados = (
    detector_video.processar_video(
        CAMINHO_VIDEO,
        intervalo_votacao=5,
        confianca_minima=0.10,
        caminho_saida=CAMINHO_VIDEO_SAIDA
    )
)


# =====================================================
# 3. Realizar votação temporal
# =====================================================

resultado_final = (
    votador.votar(
        resultados
    )
)


print("\nResultado da votação:")

print(

    json.dumps(

        resultado_final,

        indent=4,

        ensure_ascii=False

    )

)


# =====================================================
# 4. Verificar resultado
# =====================================================

if not resultado_final["sucesso"]:

    print(
        "\nPesagem não validada."
    )

    print(
        "Nenhum objeto atingiu "
        "a maioria qualificada."
    )

else:

    # =================================================
    # 5. Ler peso da balança
    # =================================================

    peso = (
        balanca.ler_peso()
    )


    # =================================================
    # 6. Montar registro para API
    # =================================================

    pesagem = {

        "massa": peso,

        "contagem":
            resultado_final["classes"],

        "quantidade_deteccoes":
            sum(
                resultado_final["classes"].values()
            ),

        "frames_analisados":
            resultado_final[
                "frames_analisados"
            ],

        "objetos_rastreados":
            resultado_final[
                "objetos_rastreados"
            ]

    }


    print(
        "\nPesagem final:"
    )

    print(

        json.dumps(

            pesagem,

            indent=4,

            ensure_ascii=False

        )

    )


    # =================================================
    # 7. Enviar para Django
    # =================================================

    resposta = (
        api.registrar_pesagem(
            pesagem
        )
    )


    print(
        "\nServidor:"
    )

    print(
        resposta
    )