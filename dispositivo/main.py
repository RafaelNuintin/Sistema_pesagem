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
    BASE_DIR
    / "models"
    / "banana.pt"
)


CAMINHO_VIDEO_SAIDA = (
    BASE_DIR
    / "videos"
    / "captura_camera.mp4"
)


URL_API = (
    "http://127.0.0.1:8000/api/pesagens/"
)


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


resultados = (
    detector_video.processar_camera(
        camera_id=0,
        intervalo_votacao=5,
        confianca_minima=0.10,
        caminho_saida=CAMINHO_VIDEO_SAIDA
    )
)


resultado_final = (
    votador.votar(
        resultados
    )
)


print(
    "\nResultado da votação:"
)

print(
    json.dumps(
        resultado_final,
        indent=4,
        ensure_ascii=False
    )
)