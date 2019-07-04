import time
import datetime
import os
import platform

import cv2

class CCTVModule():
    def __init__(self, MOVEMENT_SAMPLING_RATE, AUTO_SAVE_RATE, DETAIL_SAMPLING_RATE, DETAIL_SAMPLING_COUNT, AVG_BLUR_SIZE, IMG_BINARY_THRESHOLD, MOVEMENT_DETECTION_SENSITIVITY, cmdlog=False):
        self.MSR = int(MOVEMENT_SAMPLING_RATE)
        self.ASR = int(AUTO_SAVE_RATE)
        self.DSR = int(DETAIL_SAMPLING_RATE)
        self.DSC = int(DETAIL_SAMPLING_COUNT)
        self.ABS = int(AVG_BLUR_SIZE)
        self.IBT = int(IMG_BINARY_THRESHOLD)
        self.MDS = float(MOVEMENT_DETECTION_SENSITIVITY)

        self.capture_count = 0

        self.last_saved_image = 0

        self.detail_count = 0

        self.cmdlog = cmdlog

    def movement_detection(self, image_A, image_B):
        '''
        return True, when movement is detected compare with last image.
        '''
        if type(self.last_saved_image) == int:
            return False

        re_A_img = cv2.resize(image_A, dsize=(240, 180), interpolation=cv2.INTER_AREA)
        re_B_img = cv2.resize(image_B, dsize=(240, 180), interpolation=cv2.INTER_AREA)

        gray_A_img = cv2.cvtColor(re_A_img, cv2.COLOR_BGR2GRAY)
        gray_B_img = cv2.cvtColor(re_B_img, cv2.COLOR_BGR2GRAY)

        blur_A_img = cv2.blur(gray_A_img, (self.ABS, self.ABS))
        blur_B_img = cv2.blur(gray_B_img, (self.ABS, self.ABS))

        delta_img = cv2.absdiff(blur_A_img, blur_B_img)

        ret, thresh_img = cv2.threshold(delta_img, self.IBT, 255, cv2.THRESH_BINARY)

        total = 0
        for i in range(0,thresh_img.shape[0]):
            for j in range(0,thresh_img.shape[1]):
                total += int(thresh_img.item(i, j)/255)

        if total > self.MDS * thresh_img.shape[0] * thresh_img.shape[1]:
            return True
        return False

    def save_image(self, image, img_time):
        '''
        Save image with img_time
        '''
        # duplicate image to local "last image"
        self.last_saved_image = image

        # save it
        if platform.system() == 'Windows':
            if not os.path.isdir(os.path.split(os.path.dirname(__file__))[0] + "data\\CCTV_data\\"+img_time.strftime('%Y-%m-%d')):
                os.mkdir(os.path.split(os.path.dirname(__file__))[0] + "data\\CCTV_data\\"+img_time.strftime('%Y-%m-%d'))
            cv2.imwrite(os.path.split(os.path.dirname(__file__))[0] + "data\\CCTV_data\\"+img_time.strftime('%Y-%m-%d')+'\\'+img_time.strftime('%H-%M-%S')+".jpg", image)
        elif platform.system() == 'Linux':
            if not os.path.isdir("../data/CCTV_data/" + img_time.strftime('%Y-%m-%d')):
                os.mkdir("../data/CCTV_data/" + img_time.strftime('%Y-%m-%d'))
            cv2.imwrite("../data/CCTV_data/" + img_time.strftime('%Y-%m-%d')+'/'+img_time.strftime('%H-%M-%S')+".jpg", image)
        #image.save("data/CCTV_data/"+img_time.strftime('%Y-%m-%d_%H-%M-%S')+".jpg")

    def get_image(self, img_time):
        '''
        return image, image_name. If there isnt that file return false, ""
        '''
        pass

    def CCTV_thread(self, image, img_time):
        # detail mode on
        if self.detail_count > 0:
            if self.capture_count % self.DSR == 0:
                self.save_image(image, img_time)
                self.detail_count -= 1
                self.cmd_log_print("detail mode activate : left : %d"%self.detail_count)
        # if second is not 0, detect movement.
        elif self.capture_count % self.MSR == 0:
            md = self.movement_detection(self.last_saved_image, image)
            if md:
                self.save_image(image, img_time)
                self.detail_count = self.DSC
                self.cmd_log_print("movement is detected")
            elif self.capture_count % self.ASR == 0:
                self.save_image(image, img_time)
                self.cmd_log_print("auto save...")
        elif self.capture_count % self.ASR == 0:
            self.save_image(image, img_time)
            self.cmd_log_print("auto save...")
        
        self.capture_count += 1

    def cmd_log_print(self, txt):
        if self.cmdlog:
            print("[cctv] "+str(txt))

    def log_print(self, txt, cur_time=None):
        if cur_time is None:
            cur_time = datetime.datetime.now()

        if platform.system() == 'Windows':
            log_file = open(os.path.split(os.path.dirname(__file__))[0]+"\\data\\CCTV_log\\"+cur_time.strftime('%Y-%m-%d')+'.log', 'a')
        elif platform.system() == 'Linux':
            log_file = open("..data/CCTV_log/"+cur_time.strftime('%Y-%m-%d')+'.log', 'a')

        log_file.write(cur_time.strftime('[%Y-%m-%d_%H-%M-%S] ')+str(txt))
        log_file.close()




