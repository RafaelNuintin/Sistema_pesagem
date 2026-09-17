from ultralytics import YOLO


class Detector:

    def __init__(self, caminho_modelo):

        self.model = YOLO(caminho_modelo)

    def detectar(self, caminho_imagem):

        results = self.model(caminho_imagem)

        return self._processar_resultado(
            results
        )

    def detectar_frame(
        self,
        frame,
        confianca_minima=0.50
    ):

        results = self.model(
            frame,
            conf=confianca_minima
        )

        return self._processar_resultado(
            results
        )

    def rastrear_frame(
        self,
        frame,
        confianca_minima=0.10,
        tracker="bytetrack.yaml",
        imgsz=960
    ):

        results = self.model.track(
            frame,
            persist=True,
            conf=confianca_minima,
            imgsz=imgsz,
            tracker=tracker,
            verbose=False
        )

        return results[0]

    def _processar_resultado(
        self,
        results
    ):

        contador_classes = {}
        deteccoes = []

        for result in results:

            boxes = result.boxes

            for box in boxes:

                classe_id = int(
                    box.cls[0]
                )

                confianca = float(
                    box.conf[0]
                )

                nome = self.model.names[
                    classe_id
                ]

                if nome not in contador_classes:

                    contador_classes[nome] = 0

                contador_classes[nome] += 1

                deteccoes.append({

                    "classe": nome,

                    "classe_id": classe_id,

                    "confianca": confianca

                })

        return {

            "contagem": contador_classes,

            "deteccoes": deteccoes

        }