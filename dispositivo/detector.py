from ultralytics import YOLO


class Detector:

    def __init__(self, caminho_modelo):
        self.model = YOLO(caminho_modelo)

    def detectar(self, caminho_imagem):

        results = self.model(caminho_imagem)

        contador_classes = {}

        deteccoes = []

        for result in results:

            boxes = result.boxes

            for box in boxes:

                classe_id = int(box.cls[0])
                confianca = float(box.conf[0])

                nome = self.model.names[classe_id]

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