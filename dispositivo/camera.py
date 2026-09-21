import cv2


class Camera:

    def __init__(
        self,
        camera_id=0,
        largura=1920,
        altura=1080
    ):

        self.camera_id = camera_id

        self.captura = cv2.VideoCapture(
            camera_id,
            cv2.CAP_DSHOW
        )

        if not self.captura.isOpened():
            raise RuntimeError(
                "Não foi possível abrir a câmera."
            )

        self.captura.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            largura
        )

        self.captura.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            altura
        )

    def ler_frame(self):

        sucesso, frame = (
            self.captura.read()
        )

        if not sucesso:
            return None

        return frame

    def liberar(self):

        self.captura.release()