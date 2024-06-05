from imutils import paths
import numpy as np
import cv2
import os
from sklearn.svm import LinearSVC


def cargar_imagen(ruta):
    img = cv2.imread(ruta)
    # print("Imagen cargada")
    return img


def extraer_color(img):
    # Nos devuelve el promedio del color de cada imagen 
    # np.mean suma todos los valores de los pixeles de cada canal y los divide entre la cantidad de pixeles en el mismo canal
    #np.std devuelve la desviacion estandar, indicando la dispersion de los datos
    (B,G,R) = cv2.split(img)
    caracteristicas = np.array(
        [np.mean(B),np.mean(G),np.mean(R),
         np.std(B), np.std(G),np.std(R)]
    )
    # print("Caracteristicas obtenidas")
    return caracteristicas

# Etiquetas de clase
x = []
y = []

# print(list(paths.list_images("./train")))

#Iteramos las rutas dentro de trainj
for ruta in paths.list_images("./train"):
    # Pasamos la ruta y se carga la imagen
    img = cargar_imagen(ruta)
    caracteristicas = extraer_color(img)

    #almacenar caracteristicas en etiquetas
    print(ruta.split(os.path.sep)[-2])
    # Spli de la ruta nos devuelve una lista en donde se encuentran divididos los parametros de la ruta ['.', 'train', '1', '63610b2e-22c1-11ef-8148-d83add1963e3.jpg']
    #[-2] Nos devuelve la etiqueta/carpeta en donde se encuentran las imagenes

    y.append(ruta.split(os.path.sep)[-2])
    x.append(caracteristicas)

print(x)
print(y)
print("Programa finalizado")