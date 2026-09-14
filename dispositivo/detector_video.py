import cv2


class DetectorVideo:

    def __init__(
        self,
        detector,
        tracker="bytetrack.yaml"
    ):

        self.detector = detector
        self.tracker = tracker

    def processar_video(
        self,
        caminho_video,
        intervalo_votacao=5,
        confianca_minima=0.50
    ):

        captura = cv2.VideoCapture(
            str(caminho_video)
        )

        if not captura.isOpened():

            raise ValueError(
                f"Não foi possível abrir o vídeo: "
                f"{caminho_video}"
            )

        resultados = []

        numero_frame = 0

        while True:

            sucesso, frame = captura.read()

            if not sucesso:
                break

            # Tracking ocorre em todos os frames
            resultado = (
                self.detector.rastrear_frame(
                    frame,
                    confianca_minima,
                    self.tracker
                )
            )

            # Somente alguns frames entram
            # efetivamente na votação
            if (
                numero_frame %
                intervalo_votacao == 0
            ):

                resultados.append({

                    "frame": numero_frame,

                    "resultado": resultado

                })

            numero_frame += 1

        captura.release()

        return resultados