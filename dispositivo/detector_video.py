import cv2


class DetectorVideo:

    def __init__(self, detector):
        self.detector = detector

    def processar_video(
        self,
        caminho_video,
        intervalo_frames=5,
        confianca_minima=0.50
    ):
        captura = cv2.VideoCapture(str(caminho_video))

        if not captura.isOpened():
            raise ValueError(
                f"Não foi possível abrir o vídeo: {caminho_video}"
            )

        resultados = []

        numero_frame = 0

        while True:

            sucesso, frame = captura.read()

            if not sucesso:
                break

            if numero_frame % intervalo_frames != 0:
                numero_frame += 1
                continue

            resultado = self.detector.detectar_frame(
                frame,
                confianca_minima
            )

            resultados.append({
                "frame": numero_frame,
                "resultado": resultado
            })

            numero_frame += 1

        captura.release()

        return resultados