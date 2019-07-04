import time
import datetime
import os
import configparser
import platform

import cv2

from raspcctv_cctv import CCTVModule

if platform.system() == 'Windows':
    setting_file_dir = os.path.dirname(__file__)+'\\setting.ini'
elif platform.system() == 'Linux':
    setting_file_dir = 'setting.ini'
    from picamera import PiCamera
    from picamera.array import PiRGBArray

def camera_capture(camera, CCTV):
    '''
    capture repeatly and call CCTV module and face recognize module.
    '''
    # capture.
    if platform.system() == 'Windows':
        ret_val, image = camera.read()
    elif platform.system() == 'Linux':
        rawCapture = PiRGBArray(camera)
        camera.capture(rawCapture, format='bgr')
        image = rawCapture.array

    # get time.
    img_time = datetime.datetime.now()

    print("camera capture : "+img_time.strftime('%Y-%m-%d_%H-%M-%S'))

    #image.save("data/"+str(img_time)+".jpg")

    CCTV.CCTV_thread(image, img_time)

def camera_init():
    if platform.system() == 'Windows':
        camera = cv2.VideoCapture(0)
    elif platform.system() == 'Linux':
        camera = PiCamera()
    return camera  

def configuration_init():
    config = configparser.ConfigParser()
    config.read(setting_file_dir)
    print("config file read : "+setting_file_dir)
    return config

def face_recognition_init():
    pass

def cctv_init(MOVEMENT_SAMPLING_RATE, AUTO_SAVE_RATE, DETAIL_SAMPLING_RATE, DETAIL_SAMPLING_COUNT, AVG_BLUR_SIZE, IMG_BINARY_THRESHOLD, MOVEMENT_DETECTION_SENSITIVITY, cmdlog=False):
    return CCTVModule(MOVEMENT_SAMPLING_RATE, AUTO_SAVE_RATE, DETAIL_SAMPLING_RATE, DETAIL_SAMPLING_COUNT, AVG_BLUR_SIZE, IMG_BINARY_THRESHOLD, MOVEMENT_DETECTION_SENSITIVITY, cmdlog)

def main():
    # camera initialization
    camera = camera_init()
    print("camera initialization complete")
    
    # setting configuration initialization
    config = configuration_init()
    SAMPLING_TIME                   = config.get('CAMERA', 'SamplingTime')
    MOVEMENT_SAMPLING_RATE          = config.get('CCTV', 'MovementSamplingRate')
    AUTO_SAVE_RATE                  = config.get('CCTV', 'AutoSaveRate')
    DETAIL_SAMPLING_RATE            = config.get('CCTV', 'DetailSamplingRate')
    DETAIL_SAMPLING_COUNT           = config.get('CCTV', 'DetailSamplingCount')
    AVG_BLUR_SIZE                   = config.get('CCTV', 'AvgBlurSize')
    IMG_BINARY_THRESHOLD            = config.get('CCTV', 'ImgBinaryThreshold')
    MOVEMENT_DETECTION_SENSITIVITY  = config.get('CCTV', 'MovementDetectionSensitivity')
    print("configuration initialization complete")

    # face recognition module initialization
    #face_recognition_init()
    #print("face recognition module initialization complete")

    # cctv module initialization
    CCTV = cctv_init(MOVEMENT_SAMPLING_RATE, AUTO_SAVE_RATE, DETAIL_SAMPLING_RATE, DETAIL_SAMPLING_COUNT, AVG_BLUR_SIZE, IMG_BINARY_THRESHOLD, MOVEMENT_DETECTION_SENSITIVITY, cmdlog=True)
    print("cctv module initialization complete")

    # main loop
    while(True):
        start_time = time.time()
        camera_capture(camera, CCTV)
        while(time.time()-start_time < float(SAMPLING_TIME)):
            time.sleep(0.001)
        print("One cycle : %0.3f"%(time.time()-start_time))

if __name__ == "__main__":
    main()
