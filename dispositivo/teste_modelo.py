from pathlib import Path
import cv2

from detector import Detector


BASE_DIR = Path(__file__).resolve().parent.parent

CAMINHO_MODELO = (
    BASE_DIR / "models" / "banana.pt"
)

CAMINHO_VIDEO = (
    BASE_DIR / "videos" / "teste_bananas.mp4"
)


detector = Detector(CAMINHO_MODELO)

captura = cv2.VideoCapture(
    str(CAMINHO_VIDEO)
)

if not captura.isOpened():
    raise ValueError(
        f"Não foi possível abrir o vídeo: {CAMINHO_VIDEO}"
    )


numero_frame = 0

while True:

    sucesso, frame = captura.read()

    if not sucesso:
        break

    # Testaremos alguns frames
    if numero_frame % 30 == 0:

        resultado = detector.detectar_frame(
            frame,
            confianca_minima=0.10
        )

        print(
            f"\nFrame {numero_frame}"
        )

        print(
            "Contagem:",
            resultado["contagem"]
        )

        print(
            "Detecções:",
            resultado["deteccoes"]
        )

    numero_frame += 1


captura.release()