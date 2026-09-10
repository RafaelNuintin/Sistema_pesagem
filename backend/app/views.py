from django.shortcuts import render

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Pesagem

@csrf_exempt
def api_pesagens(request):

    if request.method != "POST":
        return JsonResponse(
            {"erro": "Método não permitido"},
            status=405
        )

    try:
        dados = json.loads(request.body)

    except json.JSONDecodeError:
        return JsonResponse(
            {"erro": "JSON inválido"},
            status=400
        )

    produto = dados.get("produto")
    massa = dados.get("massa")
    contagem = dados.get("contagem", {})
    quantidade_deteccoes = dados.get(
        "quantidade_deteccoes"
    )

    if produto is None:
        return JsonResponse(
            {"erro": "Campo 'produto' é obrigatório"},
            status=400
        )

    if massa is None:
        return JsonResponse(
            {"erro": "Campo 'massa' é obrigatório"},
            status=400
        )

    if quantidade_deteccoes is None:
        return JsonResponse(
            {
                "erro":
                "Campo 'quantidade_deteccoes' é obrigatório"
            },
            status=400
        )

    pesagem = Pesagem.objects.create(
        produto=produto,
        massa=massa,
        contagem=contagem,
        quantidade_deteccoes=quantidade_deteccoes
    )

    return JsonResponse(
        {
            "mensagem": "Pesagem registrada com sucesso",
            "id": pesagem.id,
            "pesagem": {
                "produto": pesagem.produto,
                "massa": float(pesagem.massa),
                "contagem": pesagem.contagem,
                "quantidade_deteccoes":
                    pesagem.quantidade_deteccoes,
                "data_hora":
                    pesagem.data_hora.isoformat()
            }
        },
        status=201
    )