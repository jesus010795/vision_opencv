from picamera2 import Picamera2, Preview
import time
import cv2

w = 960
h = 720
camara = Picamera2()
# camara.start_preview(Preview.QTGL)
camara.configure(camara.create_preview_configuration(
    main={
        "format": 'XRGB8888',
        "size": (w, h)
    })
)

time.sleep(1)
camara.start()


size = camara.capture_metadata()['ScalerCrop'][2:]
full_res = camara.camera_properties['PixelArraySize']

for _ in range(20):
    # This syncs us to the arrival of a new camera frame:
    img = camara.capture_metadata()
    imagen = camara.capture_array()

    size = [int(s * 0.95) for s in size]
    offset = [(r - s) // 2 for r, s in zip(full_res, size)]
    camara.set_controls({"ScalerCrop": offset + 
    size})

    print(f"{size, offset}")
"""
'ScalerCrop': ((0, 0, 128, 128), (0, 0, 4056, 3040), (2, 0, 4052, 3040))
"""
with camara.controls as controls:
    controls.Brightness = 0.27
    print(controls.Brightness)
    # controls.AnalogueGain = gain*.001
    # controls.Contrast = 1
    controls.NoiseReductionMode = 2
    # controls.Saturation = 2
    # controls.ColourGains = 20
    

time.sleep(2)
# print(print(camara.camera_controls['Brightness']))

while True:
    imagen = camara.capture_array()
    
    cv2.imshow("Metadata", imagen)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):        
        break

cv2.destroyAllWindows()
camara.close()