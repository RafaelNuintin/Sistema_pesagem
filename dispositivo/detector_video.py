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
        confianca_minima=0.10,
        caminho_saida=None
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

            # -----------------------------------------
            # Tracking
            # -----------------------------------------

            resultado = (
                self.detector.rastrear_frame(
                    frame,
                    confianca_minima,
                    self.tracker
                )
            )

            # -----------------------------------------
            # Visualização
            # -----------------------------------------

            if escritor is not None:

                frame_anotado = resultado.plot(
                    conf=True,
                    labels=True,
                    boxes=True
                )

                escritor.write(
                    frame_anotado
                )

            # -----------------------------------------
            # Diagnóstico
            # -----------------------------------------

            boxes = resultado.boxes

            quantidade = (
                len(boxes)
                if boxes is not None
                else 0
            )

            possui_ids = (
                boxes is not None
                and boxes.id is not None
            )

            # -----------------------------------------
            # Votação
            # -----------------------------------------

            if (
                numero_frame
                % intervalo_votacao
                == 0
            ):

                print(
                    f"Frame {numero_frame}: "
                    f"{quantidade} detecção(ões), "
                    f"IDs disponíveis: "
                    f"{possui_ids}"
                )

                resultados.append({
                    "frame": numero_frame,
                    "resultado": resultado
                })

            numero_frame += 1

        captura.release()

        if escritor is not None:
            escritor.release()

        return resultados