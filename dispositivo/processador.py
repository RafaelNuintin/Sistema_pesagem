from collections import Counter


class ProcessadorPesagem:

    def __init__(self, confianca_minima=0.70):
        self.confianca_minima = confianca_minima

    def processar(self, resultado):

        deteccoes_validas = [
            d for d in resultado["deteccoes"]
            if d["confianca"] >= self.confianca_minima
        ]

        if not deteccoes_validas:
            return None

        contador = Counter(
            d["classe"]
            for d in deteccoes_validas
        )

        produto = contador.most_common(1)[0][0]

        return {
            "produto": produto,
            "contagem": dict(contador),
            "quantidade_deteccoes": len(deteccoes_validas)
        }