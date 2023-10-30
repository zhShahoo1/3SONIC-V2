import sys
import ctypes
from ctypes import *
import numpy as np
import cv2
import time
import os

# the directory of the currently executing script
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# the path to the DLL
dll_path = os.path.join(script_dir, 'usgfw2wrapper.dll')

usgfw_2 = cdll.LoadLibrary(dll_path)

w = 512
h = 512

def initialize_ultrasound():
    usgfw_2.on_init()
    ERR = usgfw_2.init_ultrasound_usgfw2()

    if (ERR == 2):
        print('Main usgfw_2 library object not created')
        usgfw_2.Close_and_release()
        sys.exit()

    ERR = usgfw_2.find_connected_probe()
    if (ERR != 101):
        print('Probe not detected')
        usgfw_2.Close_and_release()
        sys.exit()

    ERR = usgfw_2.data_view_function()
    if (ERR < 0):
        print('Main ultrasound scanning object for selected probe not created')
        sys.exit()

    ERR = usgfw_2.mixer_control_function(0, 0, w, h, 0, 0, 0)
    if (ERR < 0):
        print('B mixer control not returned')
        usgfw_2.Close_and_release()
        sys.exit()

    return w, h

def generate_image(w, h):
    p_array = (ctypes.c_uint * w * h * 4)()

    while True:  # This will make the loop run indefinitely
        usgfw_2.return_pixel_values(ctypes.pointer(p_array))
        buffer_as_numpy_array = np.frombuffer(p_array, np.uint)
        reshaped_array = np.reshape(buffer_as_numpy_array, (w, h, 4))
        reshaped_array = np.clip(reshaped_array, 0, 255)
        reshaped_array = reshaped_array.astype(np.uint8)
        
        # Flip the image vertically ! 
        reshaped_array = cv2.flip(reshaped_array, 0)    

        ret, jpeg = cv2.imencode('.jpg', reshaped_array[:, :, 0:3])
        frame = jpeg.tobytes()

        #time.sleep(0.1)  # A delay of 0.1 seconds (100 milliseconds) between frames
        yield frame
