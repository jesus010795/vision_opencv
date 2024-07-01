import RPi.GPIO as gp
from gpiozero import Button
from time import sleep
from signal import pause

gp.setwarnings(False)
gp.setmode(gp.BCM)
gp.setup(21, gp.OUT)
gp.setup(20, gp.IN)

# continuar = True
# while True:
#     valor = ""
#     print(valor)
#     push_btn = gp.input(20)
#     print(push_btn)
#     sleep(1)
#     if push_btn == gp.HIGH:
#         sleep(.5)
#         valor = "p"
#         print(valor)
#         print("Boton presionado")


# gp.cleanup()
# print("Fin de programa")

try:
    while True:
        valor = 0 
        # print("While")
        # sleep(1)
        if gp.input(20) == gp.HIGH:
            sleep(.5)
            gp.output(21, gp.HIGH)
            valor = 1
            # print(valor)
            print("Boton presionado")
        else:
            gp.output(21, gp.LOW)
            # valor= 0
            # print(valor)
except:
    pass

# try:
#     while True:
#         gp.output(21, gp.HIGH)
#         sleep(.5)
#         gp.output(21, gp.LOW)
#         sleep(.5)
    
# except:
#     pass

gp.cleanup()
print("Fin de programa")