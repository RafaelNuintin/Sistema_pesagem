import requests


class ClienteAPI:

    def __init__(self, url):
        self.url = url

    def registrar_pesagem(self, dados):

        resposta = requests.post(
            self.url,
            json=dados,
            timeout=10
        )

        resposta.raise_for_status()

        return resposta.json()