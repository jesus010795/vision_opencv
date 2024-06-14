from imutils import paths
import numpy as np
import cv2
import os
from sklearn.svm import LinearSVC
import pickle
from time import sleep


def cargar_imagen(ruta):
    img = cv2.imread(ruta)
    # print("Imagen cargada")
    return img


def extraer_color(img):
   canales = cv2.split(img)
   caracteristicas = []
   for canal in canales:
       hist = cv2.calcHist([canal], [0], None, [256], [0,256]).flatten().tolist()
       caracteristicas.extend(hist)
   return caracteristicas

def prediccion(caracteristicas, modelo, img):
    prediccion = modelo.predict(caracteristicas)[0]
    print(type(prediccion))
    cv2.putText(img, prediccion, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0) )
    return prediccion

# Etiquetas de clase
x = []
y = []

# print(list(paths.list_images("./train")))

#Iteramos las rutas dentro de trainj
for ruta in paths.list_images("./train"):
    img = cargar_imagen(ruta)
    caracteristicas = extraer_color(img)
    # sleep(1)
    print(ruta.split(os.path.sep)[-2])
    y.append(ruta.split(os.path.sep)[-2])
    x.append(caracteristicas)

x = np.array(x)

sleep(0.5)
modelo = LinearSVC(dual = True,C = 100.0, random_state=1, max_iter=40000)
sleep(0.5)
modelo.fit(x,y)
sleep(0.5)

for ruta in paths.list_images("./test"):
   
    img = cargar_imagen(ruta)
    caracteristicas = extraer_color(img)
    caracteristicas = np.array([caracteristicas])
    resultado_img = prediccion(caracteristicas, modelo, img)
    print(resultado_img)
    cv2.imshow("Prediccion", img)
    cv2.waitKey()

with open("modeloClasificadorHistograma.pkl", "wb") as f:
    pickle.dump(modelo, f)


cv2.destroyAllWindows()

print("Programa finalizado")