import cv2


class DetectorVideo:

    def __init__(
        self,
        detector,
        tracker="bytetrack.yaml"
    ):
        self.detector = detector
        self.tracker = tracker

    def processar_camera(
        self,
        camera_id=0,
        intervalo_votacao=5,
        confianca_minima=0.10,
        caminho_saida=None
    ):

        captura = cv2.VideoCapture(
            camera_id,
            cv2.CAP_DSHOW
        )

        if not captura.isOpened():
            raise ValueError(
                "Não foi possível abrir a câmera."
            )

        resultados = []

        numero_frame = 0

        escritor = None

        if caminho_saida is not None:

            largura = int(
                captura.get(
                    cv2.CAP_PROP_FRAME_WIDTH
                )
            )

            altura = int(
                captura.get(
                    cv2.CAP_PROP_FRAME_HEIGHT
                )
            )

            fps = captura.get(
                cv2.CAP_PROP_FPS
            )

            if fps <= 0:
                fps = 30

            codec = cv2.VideoWriter_fourcc(
                *"mp4v"
            )

            escritor = cv2.VideoWriter(
                str(caminho_saida),
                codec,
                fps,
                (largura, altura)
            )

        while True:

            sucesso, frame = captura.read()

            if not sucesso:
                break

            resultado = (
                self.detector.rastrear_frame(
                    frame,
                    confianca_minima,
                    self.tracker
                )
            )

            frame_anotado = resultado.plot(
                conf=True,
                labels=True,
                boxes=True
            )

            if escritor is not None:
                escritor.write(
                    frame_anotado
                )

            cv2.imshow(
                "Sistema de Pesagem",
                frame_anotado
            )

            if (
                numero_frame
                % intervalo_votacao
                == 0
            ):

                resultados.append({
                    "frame": numero_frame,
                    "resultado": resultado
                })

            numero_frame += 1

            tecla = cv2.waitKey(1) & 0xFF

            if tecla == ord("q"):
                break

        captura.release()

        if escritor is not None:
            escritor.release()

        cv2.destroyAllWindows()

        return resultados