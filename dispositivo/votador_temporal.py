from collections import Counter


class VotadorTemporal:

    def __init__(self, exigir_unanimidade=True):
        self.exigir_unanimidade = exigir_unanimidade

    def votar(self, resultados):

        if not resultados:
            return None

        assinaturas = []

        for item in resultados:

            contagem = item["resultado"]["contagem"]

            assinatura = tuple(
                sorted(contagem.items())
            )

            assinaturas.append(assinatura)

        contador = Counter(assinaturas)

        assinatura_vencedora, quantidade = (
            contador.most_common(1)[0]
        )

        total = len(assinaturas)

        if self.exigir_unanimidade:

            if quantidade != total:
                return {
                    "sucesso": False,
                    "motivo": "Não houve unanimidade entre os frames",
                    "frames_analisados": total,
                    "votos": quantidade
                }

        contagem_final = dict(
            assinatura_vencedora
        )

        return {
            "sucesso": True,
            "contagem": contagem_final,
            "frames_analisados": total,
            "votos": quantidade
        }