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

def prediccion(caracteristicas, modelo, img):
    
    prediccion = modelo.predict(caracteristicas)
    cv2.putText(img, prediccion[0], (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0) )
    return prediccion

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
# print(x)
# print(y)

#Convertimos las caracteristicas en un vector
x = np.array(x)
# Creamos el modelo
sleep(0.5)
modelo = LinearSVC(dual = True,C = 100.0, random_state=1, max_iter=40000)
# Ejecutamos el entrenamiento
sleep(0.5)
modelo.fit(x,y)
sleep(0.5)

for ruta in paths.list_images("./test"):
    # Iteramos sobre todas las imagenes que se encuentran en test
    # Nos devolvera la clase original (0 o 1) y nos devolvera la prediccion (0 o 1)
    img = cargar_imagen(ruta)
    caracteristicas = extraer_color(img)
    caracteristicas = np.array([caracteristicas])
    # clase_verdadera = ruta.split(os.path.sep)[-2]
    # resultado_clase= prediccion(caracteristicas, modelo)
    resultado_img = prediccion(caracteristicas, modelo, img)
    # print(f"Clase original: {clase_verdadera} - Prediccion: {resultado_clase} \n")
    print(caracteristicas)
    cv2.imshow("Prediccion", img)
    cv2.waitKey()

with open("modeloClasificador.pkl", "wb") as f:
    pickle.dump(modelo, f)


cv2.destroyAllWindows()

print("Programa finalizado")