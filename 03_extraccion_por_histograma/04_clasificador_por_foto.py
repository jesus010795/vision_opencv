from picamera2 import Picamera2
# from sklearn.svm import LinearSVC
# from imutils import paths
from time import sleep
import numpy as np
import skimage
import cv2
import os
import time
import RPi.GPIO as gp

import pickle

gp.setmode(gp.BCM)
gp.setup(21, gp.OUT)
gp.setup(20, gp.IN)

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

def eliminar_fotos(carpeta):
    for fichero in carpeta:
        if fichero.endswith("*.jpg"):
            os.remove(carpeta + fichero)

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

def cargar_imagen(ruta):
    img = cv2.imread(ruta)
    # print("Imagen cargada")
    return img

def mandar_pulso():
    gp.output(21, gp.HIGH)
    sleep(.2)
    gp.output(21, gp.LOW)

valores = {"0":"Buena", "1":"Mala"}

with open("modeloClasificadorHistograma.pkl", "rb") as f:
     modelo = pickle.load(f)

camara.start()

while True:
    push_btn = gp.input(20)
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
            if M['m00'] > 500:
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

                Mt = cv2.getPerspectiveTransform(puntos_origen, puntos_destino)
                recorte = cv2.warpPerspective(imagen, Mt, (300, 300))

        
        if push_btn == gp.HIGH:
            sleep(.2)
            print("Boton presionado")
            ruta_captura = "./capturas/" +  time.strftime("%Y%m%d-%H%M%S") + ".jpg" 
            cv2.imwrite(ruta_captura, recorte)
            print("Imagen capturada")

        if ruta_captura != None:
            try:
                imagen_foto = cargar_imagen(ruta_captura)
                caracteristicas_tiempo_real = extraer_color(imagen_foto)
                caracteristicas_tiempo_real = np.array([caracteristicas_tiempo_real])
                resultado_prediccion = prediccion(modelo, caracteristicas_tiempo_real, valores)
                # print(type(resultado_prediccion))
                # cx = int(M['m10'] / M['m00'])
                # cy = int(M['m01'] / M['m00'])
            except:
                print("error")

        resultado_str = valores[resultado_prediccion]
        
        if  resultado_prediccion == "0" or resultado_str == "":
            # cv2.putText(copia_imagen,valores[resultado_prediccion], (cx,cy), cv2.FONT_HERSHEY_COMPLEX,  0.8, (255,0,0), 2)
            # cv2.drawContours(copia_imagen, [box], -1, (0,255,0), 2)
            print(valores[resultado_prediccion])
        else:
            # cv2.drawContours(copia_imagen, [box], -1, (0,0,255), 2)
            # cv2.putText(copia_imagen,valores[resultado_prediccion], (cx,cy), cv2.FONT_HERSHEY_COMPLEX,  0.8, (255,0,0), 2)
            print(valores[resultado_prediccion])
            mandar_pulso()

        # print(resultado_str)
        os.remove(ruta_captura) 
        ruta_captura = None
        resultado_str = None
        resultado_prediccion = None     
    except:
         pass

    cv2.imshow("Contornos", copia_imagen)
    # cv2.imshow("Recorte", recorte)
    cv2.imshow("Binari", th)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):        
        break

gp.cleanup()
cv2.destroyAllWindows()
camara.close()

print("Programa finalizado....")