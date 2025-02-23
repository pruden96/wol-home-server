import cv2

class Camera_USB:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(self.camera_id)

    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None
        _, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()

    def release(self):
        self.cap.release()

cameras = {}

# Diccionario para controlar si un stream sigue activo
active_streams = {}