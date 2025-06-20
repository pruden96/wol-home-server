from flask import Blueprint, Response
from flask_jwt_extended import jwt_required

from services.camera_service import Camera_USB, active_streams, cameras

camera_bp = Blueprint("camera", __name__)


def generate_frames(camera_id: int):
    while active_streams.get(camera_id, False):
        try:
            if camera_id not in cameras or not cameras[camera_id].cap.isOpened():
                print(f"Cámara {camera_id} cerrada, deteniendo stream.")
                break

            frame = cameras[camera_id].get_frame()
            if frame is None:
                continue
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
        except KeyError:
            print(f"Cámara {camera_id} eliminada mientras se ejecutaba el stream.")
            break
        except Exception as e:
            print(f"Error al procesar el frame de la cámara {camera_id}: {str(e)}")
            break

    print(f"Finalizando transmisión de cámara {camera_id}.")


@camera_bp.route("/stream/<int:camera_id>", methods=["GET"])
@jwt_required()
def stream(camera_id: int) -> Response:
    if camera_id not in cameras:
        cameras[camera_id] = Camera_USB(camera_id)

    active_streams[camera_id] = True  # Activar el stream
    return Response(
        generate_frames(camera_id), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@camera_bp.route("/release/<int:camera_id>", methods=["POST"])
@jwt_required()
def release_camera(camera_id: int) -> Response:
    if camera_id in cameras:
        active_streams[camera_id] = False  # Indicar que el stream debe detenerse
        cameras[camera_id].release()
        del cameras[camera_id]
        print(f"Cámara {camera_id} liberada correctamente.")
        return {"message": f"Cámara {camera_id} liberada"}, 200

    return {"error": "Cámara no encontrada"}, 404
