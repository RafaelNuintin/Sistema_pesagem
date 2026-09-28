import cv2
import time


CAMERA_ID = 0

RESOLUCOES = [
    (640, 480),
    (1280, 720),
    (1920, 1080),
]


for largura_desejada, altura_desejada in RESOLUCOES:

    captura = cv2.VideoCapture(
        CAMERA_ID,
        cv2.CAP_MSMF
    )

    if not captura.isOpened():

        print(
            "Não foi possível abrir a câmera."
        )

        continue

    fourcc = cv2.VideoWriter_fourcc(*"MJPG")

    captura.set(
        cv2.CAP_PROP_FOURCC,
        fourcc
    )

    captura.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        largura_desejada
    )

    captura.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        altura_desejada
    )


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


    print(
        f"\nTestando "
        f"{largura_desejada}x{altura_desejada}"
    )

    print(
        f"Obtido: {largura}x{altura}"
    )


    contador = 0

    inicio = time.perf_counter()


    while (
        time.perf_counter() - inicio
        < 5
    ):

        sucesso, frame = (
            captura.read()
        )

        if not sucesso:
            break

        contador += 1

        cv2.imshow(
            "Teste de resolucao",
            frame
        )

        if (
            cv2.waitKey(1) & 0xFF
            == ord("q")
        ):
            break


    tempo = (
        time.perf_counter()
        - inicio
    )

    fps = contador / tempo


    print(
        f"FPS real: {fps:.2f}"
    )


    captura.release()


cv2.destroyAllWindows()