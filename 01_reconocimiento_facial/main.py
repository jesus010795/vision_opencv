from picamera2 import Picamera2, Preview
import time
import cv2
from deepface import DeepFace
import pyttsx3

w = 960
h = 720
last_message = ""
error_face = "Rostro no detectado"

def try_to_recognize(frame):
    try:
        recognition = DeepFace.find(frame, db_path='db', model_name='VGG-Face', silent=True)
        recognition2 = recognition['identity'][0]
        name  = recognition2.split("\\")[1].split("/")[0]
        return name
    except ValueError:
        return error_face
    except KeyError:
        return error_face
    

def greeting(message):
    if message != error_face:
        print("Hola {message}")
        # return message

camera = Picamera2()
# se define laconfiguracion de la cmara
# Despues de varias pruebas esta esla mejor configuracion y con la que pude ejecutar el video en vnc viewer para trabajar en remoto a una mejor velocidad
camera.configure(camera.create_preview_configuration(
    main={
        "format": 'XRGB8888',
        # "format": 'SBGGR12',
        "size": (w, h)
    })
)
# Se inicializa el proceso de captura
camera.start()


while True:
    # Almacenamos la captura en tiempo real para despues renderizarla
    video = camera.capture_array()
    vid_cv2 = cv2.VideoCapture(0)
    #Almacenamos ne una variable el reaultado de la consulta de los rostros
    message = try_to_recognize(video)

    if message != last_message:
        greeting(message)

    #Agregamos anuestra ventana el teto con el nombre identificado    
    cv2.putText(video, message, (0,115), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    

    # Se renderiza enuna ventana creada por opencv
    cv2.imshow("Video", video)
    # Tecla de escape para salir de la captura
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    last_message = message


cv2.destroyAllWindows()
camera.close()


