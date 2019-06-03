import time
import datetime
import os
import threading
import configparser
import io

from PIL import Image
import picamera

from raspcctv_cctv import CCTVModule

setting_file_dir = 'setting.ini'

def camera_capture(camera, CCTV):
    '''
    capture repeatly and call CCTV module and face recognize module.
    '''
    # capture.
    stream = io.BytesIO()
    camera.capture(stream, format = 'jpeg')
    stream.seek(0)

    # get image and time.
    image = Image.open(stream)
    img_time = datetime.datetime.now()

    #image.save("data/"+str(img_time)+".jpg")

    CCTV.CCTV_thread(image, img_time)

def camera_init():
    camera = picamera.PiCamera()
    return camera  

def configuration_init():
    config = configparser.ConfigParser()
    config.read(setting_file_dir)
    print("config file read : "+setting_file_dir)
    return config

def face_recognition_init():
    pass

def cctv_init(MOVEMENT_SAMPLING_RATE, AUTO_SAVE_RATE, DETAIL_SAMPLING_RATE):
    return CCTVModule(MOVEMENT_SAMPLING_RATE, AUTO_SAVE_RATE, DETAIL_SAMPLING_RATE)

def main():
    # camera initialization
    camera = camera_init()
    print("camera initialization complete")
    
    # setting configuration initialization
    config = configuration_init()
    SAMPLING_TIME           = config.get('CAMERA', 'SamplingTime')
    MOVEMENT_SAMPLING_RATE  = config.get('CCTV', 'MovementSamplingRate')
    AUTO_SAVE_RATE          = config.get('CCTV', 'AutoSaveRate')
    DETAIL_SAMPLING_RATE    = config.get('CCTV', 'DetailSamplingRate')
    print("configuration initialization complete")

    # face recognition module initialization
    #face_recognition_init()
    #print("face recognition module initialization complete")

    # cctv module initialization
    CCTV = cctv_init(MOVEMENT_SAMPLING_RATE, AUTO_SAVE_RATE, DETAIL_SAMPLING_RATE)
    print("cctv module initialization complete")

    # main loop
    while(True):
        camera_capture(camera, CCTV)
        print("camera_captured")
        time.sleep(float(SAMPLING_TIME))

if __name__ == "__main__":
    print(__file__)
    main()
