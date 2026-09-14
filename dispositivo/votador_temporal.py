from collections import Counter, defaultdict


class VotadorTemporal:

    def __init__(
        self,
        razao_minima=0.80,
        observacoes_minimas=3
    ):

        self.razao_minima = razao_minima

        self.observacoes_minimas = (
            observacoes_minimas
        )

    def votar(self, resultados):

        if not resultados:

            return {

                "sucesso": False,

                "motivo":
                    "Nenhum frame foi analisado",

                "classes": {},

                "objetos": []

            }

        historico = defaultdict(list)

        # -------------------------------------------------
        # 1. Construir histórico de cada objeto rastreado
        # -------------------------------------------------

        for item in resultados:

            numero_frame = item["frame"]

            resultado = item["resultado"]

            boxes = resultado.boxes

            if boxes is None:
                continue

            if boxes.id is None:
                continue

            ids = (
                boxes.id
                .int()
                .cpu()
                .tolist()
            )

            classes = (
                boxes.cls
                .int()
                .cpu()
                .tolist()
            )

            confiancas = (
                boxes.conf
                .cpu()
                .tolist()
            )

            for track_id, classe_id, confianca in zip(
                ids,
                classes,
                confiancas
            ):

                nome_classe = (
                    resultado.names[classe_id]
                )

                historico[track_id].append({

                    "frame": numero_frame,

                    "classe": nome_classe,

                    "classe_id": classe_id,

                    "confianca": confianca

                })

        # -------------------------------------------------
        # 2. Votar individualmente em cada objeto
        # -------------------------------------------------

        objetos_validos = []

        objetos_rejeitados = []

        for track_id, observacoes in (
            historico.items()
        ):

            quantidade_observacoes = (
                len(observacoes)
            )

            if (
                quantidade_observacoes
                < self.observacoes_minimas
            ):

                objetos_rejeitados.append({

                    "track_id": track_id,

                    "motivo":
                        "Poucas observações",

                    "observacoes":
                        quantidade_observacoes

                })

                continue

            contador_classes = Counter(
                obs["classe"]
                for obs in observacoes
            )

            classe_vencedora, votos = (
                contador_classes.most_common(1)[0]
            )

            razao = (
                votos /
                quantidade_observacoes
            )

            confiancas = [

                obs["confianca"]

                for obs in observacoes

                if obs["classe"]
                == classe_vencedora

            ]

            confianca_media = (

                sum(confiancas)
                / len(confiancas)

            )

            objeto = {

                "track_id": track_id,

                "classe": classe_vencedora,

                "votos": votos,

                "observacoes":
                    quantidade_observacoes,

                "razao": razao,

                "confianca_media":
                    confianca_media

            }

            if razao >= self.razao_minima:

                objetos_validos.append(
                    objeto
                )

            else:

                objeto["motivo"] = (
                    "Maioria qualificada "
                    "não atingida"
                )

                objetos_rejeitados.append(
                    objeto
                )

        # -------------------------------------------------
        # 3. Contar objetos válidos por classe
        # -------------------------------------------------

        contagem_classes = Counter(

            objeto["classe"]

            for objeto in objetos_validos

        )

        return {

            "sucesso":
                len(objetos_validos) > 0,

            "classes":
                dict(contagem_classes),

            "objetos":
                objetos_validos,

            "objetos_rejeitados":
                objetos_rejeitados,

            "frames_analisados":
                len(resultados),

            "objetos_rastreados":
                len(historico)

        }