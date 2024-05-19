from picamera2 import Picamera2, Preview
import time
import cv2
# from deepface import DeepFace
# import pyttsx3

w = 960
h = 720

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
    # Se renderiza enuna ventana creada por opencv
    cv2.imshow("Video", video)


    # Tecla de escape para salir de la captura
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
camera.close()