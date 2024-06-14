from picamera2 import Picamera2
from sklearn.svm import LinearSVC
from imutils import paths
from time import sleep
import numpy as np
import skimage
import cv2
import uuid
import os

import pickle

w = 960
h = 720
kernel = np.ones((23,23), np.uint8)

camara = Picamera2()
camara.configure(camara.create_preview_configuration(
    main={
        "format": 'XRGB8888',
        "size": (w, h)
    })
)


with camara.controls as controls:
        controls.Brightness =  0.23
        controls.Contrast = 1.42
        controls.NoiseReductionMode = 2

def extraer_color(img):
   canales = cv2.split(img)
   caracteristicas = []
   for canal in canales:
       hist = cv2.calcHist([canal], [0], None, [256], [0,256]).flatten().tolist()
       caracteristicas.extend(hist)
   return caracteristicas

def prediccion(mod, caracteristicas, valores):
    prediccion = mod.predict(caracteristicas)[0]
    return prediccion

valores = {"0":"Buena", "1":"Mala"}

with open("modeloClasificadorHistograma.pkl", "rb") as f:
     modelo = pickle.load(f)

# -------------------------------------------
#  -------------    MODELO    ---------------
# def cargar_imagen(ruta):
#     img = cv2.imread(ruta)
#     return img
# x = []
# y = []

# for ruta in paths.list_images("./train"):
#     img = cargar_imagen(ruta)
#     caracteristicas = extraer_color(img)
#     # print(caracteristicas)
#     # sleep(1)
#     print(ruta.split(os.path.sep)[-2])
#     y.append(ruta.split(os.path.sep)[-2])
#     x.append(caracteristicas)

# x = np.array(x)
# # print(x,y)
# sleep(0.5)
# modelo = LinearSVC(dual = True,C = 100.0, random_state=1, max_iter=39000)
# sleep(0.5)
# modelo.fit(x,y)

# -------------------------------------------

camara.start()

while True:
    imagen = camara.capture_array()
    copia_imagen = imagen.copy()

    escala_grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    escala_grises = cv2.bilateralFilter(escala_grises, 3,25,25)

    _, th = cv2.threshold(escala_grises, 110, 255, cv2.THRESH_BINARY_INV)
    th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)
    th = skimage.segmentation.clear_border(th)

    contornos = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    try:
        for contorno in contornos[0]:
            M = cv2.moments(contorno)
            # print(M['m00'])
            if M['m00'] > 6000:
                rect = cv2.minAreaRect(contorno)
                box = cv2.boxPoints(rect)
                box = box.astype(int)
                cv2.drawContours(copia_imagen, [box], -1, (0,255,0), 2)

                width = int(rect[1][0])
                height = int(rect[1][1])

                puntos_origen = box.astype("float32")
                puntos_destino = np.array([
                    [0,300],
                    [0,0],
                    [300,0],
                    [300,300]
                ],  dtype = "float32")

                Mt = cv2.getPerspectiveTransform(puntos_origen, puntos_destino)
                recorte = cv2.warpPerspective(imagen, Mt, (300, 300))
                # print(cx,cy)
                sleep(.5)
                caracteristicas_tiempo_real = extraer_color(recorte)
                caracteristicas_tiempo_real = np.array([caracteristicas_tiempo_real])
                try:
                    resultado_prediccion = prediccion(modelo, caracteristicas_tiempo_real, valores)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    # cv2.putText(copia_imagen, valores[predicc], (cx,cy), cv2.FONT_HERSHEY_COMPLEX,  0.8, (255,0,0), 2)
                except:
                    print("error")

    except:
         pass

    cv2.imshow("Contornos", copia_imagen)
    # cv2.imshow("Contos", th)
    # cv2.imshow("Recorte", recorte)
    # camara.wait()
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


cv2.destroyAllWindows()
camara.close()