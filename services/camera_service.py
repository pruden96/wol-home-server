import cv2


class Camera_USB:
    def __init__(self, camera_id: int = 0) -> None:
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(self.camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

    def get_frame(self) -> None | bytes:
        success, frame = self.cap.read()
        if not success:
            return None
        _, buffer = cv2.imencode(".jpg", frame)
        return buffer.tobytes()

    def release(self) -> None:
        self.cap.release()


cameras = {}

# Diccionario para controlar si un stream sigue activo
active_streams = {}
