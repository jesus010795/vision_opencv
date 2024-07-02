from picamera2 import Picamera2
from time import sleep, strftime
import numpy as np
import skimage
import uuid
import cv2

w = 960
h = 720

# carpeta en la que se almacenaran las imagenes
# "0" bueno
# "1" malo 
clase = "0"


camara = Picamera2()
camara.configure(camara.create_preview_configuration(
    main={
        "format": 'XRGB8888',
        "size": (w, h)
    })
)

print(camara.camera_controls)

with camara.controls as controls:
        controls.Brightness =  0.23
        # controls.AnalogueGain = gain*.001
        controls.Contrast = 1.42
        controls.NoiseReductionMode = 2
        # controls.Saturation = 2
        # controls.ColourGains = 20

sleep(0.3)
camara.start()

kernel = np.ones((23,23), np.uint8)

while True:
    imagen = camara.capture_array()
    copia_imagen = imagen.copy()

    # Este recorte correspondera al tamano de la imagen capturada
    # recorte = np.zeros((300,300), np.uint8)

    escala_grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    escala_grises = cv2.bilateralFilter(escala_grises, 3,25,25)

    # Binarizacion de imagen
    _, th = cv2.threshold(escala_grises, 110, 255, cv2.THRESH_BINARY_INV)
    #Morfologia de cierre
    th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)
    # Segmentacion para eliminar ruido
    th = skimage.segmentation.clear_border(th)
    contornos = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    try:
         # Se trabajara controno por contorno por medio de moments
        contorno = contornos[0][0]
        M = cv2.moments(contorno)
        # print(M['m00'])
        if M['m00'] > 1000:
            rect = cv2.minAreaRect(contorno)
            box = cv2.boxPoints(rect)
            box = box.astype(int)
            cv2.drawContours(copia_imagen, [box], -1, (0,255,0), 2)

            # width = int(rect[1][0])
            # height = int(rect[1][1])

            puntos_origen = box.astype("float32")
            puntos_destino = np.array([
                 [0,300],
                 [0,0],
                 [300,0],
                 [300,300]
            ],  dtype = "float32")

            matriz_transformacion = cv2.getPerspectiveTransform(puntos_origen, puntos_destino)
            recorte = cv2.warpPerspective(imagen, matriz_transformacion, (300, 300))
    except:
         pass

    cv2.imshow("Binario", th)
    cv2.imshow("Contornos", copia_imagen)
    # cv2.imshow("Recorte", recorte)
    # Tecla de escape para salir de la captura
    key = cv2.waitKey(1) & 0xFF
    
    # Si presionamos la tecla p haremos una captura de la imagen
    if key == ord("p"):
        miUUID = str(uuid.uuid1())
        cv2.imwrite("./train/" + clase + "/" +  strftime("%Y-%m-%d--%H:%M:%S") + ".jpg", recorte)
        print("Imagen capturada")
    if key == ord("q"):
        break


cv2.destroyAllWindows()
camara.close()