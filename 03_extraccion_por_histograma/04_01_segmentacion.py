from picamera2 import Picamera2
# from sklearn.svm import LinearSVC
# from imutils import paths
from time import sleep
import numpy as np
import skimage
import cv2
import os
import time

def extraer_color(imagen, r):
    frameHSV =cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    # imagen_nueva = frameHSV[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
    imagen_nueva = frameHSV[r[1]:r[1]+r[3], r[0]:r[0]+r[2]]

    H = imagen_nueva[:,:,0]
    S = imagen_nueva[:,:,1]
    V = imagen_nueva[:,:,2]
    hmin, hmax = np.min(H), np.max(H)
    smin, smax = np.min(S), np.max(S)
    vmin, vmax = np.min(V), np.max(V)
    bajo = np.array([hmin, smin, vmin, np.uint8])
    alto = np.array([hmax, smax, vmax, np.uint8])
    return bajo, alto

def test_color(imagen, rango_bajo, rango_alto):
    copia_imagen = imagen.copy()
    frameHSV = cv2.cvtColor(copia_imagen, cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(frameHSV, rango_bajo, rango_alto)
    # cx, cy = obtener_centro(mask)
    # # img2[mask == 255] = amarillo
    # cv2.circle(img2, (cx,cy), 5, (0,0,255), -1)
    return copia_imagen, mascara

 
w = 620
h = 480
kernel = np.ones((20,20), np.uint8)

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

sleep(.2)
camara.start()

cuenta = 0
while True:
    imagen = camara.capture_array()

    if cuenta == 10:
        roi = cv2.selectROI("imagen", imagen, showCrosshair=True, fromCenter=False)
        
        roi = tuple(map(int, roi))
            

        rango_bajo, rango_alto = extraer_color(imagen, roi)
        print(f"Bajo: {rango_bajo} \n")
        print(f"A  lto: {rango_alto} \n")
    elif cuenta > 10:
        frame, mascara = test_color(imagen, rango_bajo, rango_alto)
        cv2.imshow("Frame", mascara)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    cuenta += 1

cv2.destroyAllWindows()