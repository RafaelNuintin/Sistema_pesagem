import cv2


CAMERA_ID = 0


captura = cv2.VideoCapture(
    CAMERA_ID,
    cv2.CAP_DSHOW
)


if not captura.isOpened():
    raise RuntimeError(
        "Não foi possível abrir a câmera."
    )


# Solicita 1920x1080
captura.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    1920
)

captura.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    1080
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

fps = captura.get(
    cv2.CAP_PROP_FPS
)


print(
    f"Resolução: {largura}x{altura}"
)

print(
    f"FPS: {fps}"
)


while True:

    sucesso, frame = captura.read()

    if not sucesso:
        print(
            "Não foi possível receber "
            "um frame da câmera."
        )
        break

    cv2.imshow(
        "Teste da webcam",
        frame
    )

    tecla = cv2.waitKey(1) & 0xFF

    if tecla == ord("q"):
        break


captura.release()

cv2.destroyAllWindows()