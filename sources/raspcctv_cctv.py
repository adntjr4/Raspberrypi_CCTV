import time
import datetime
import io


class CCTVModule():
    def __init__(self, MOVEMENT_SAMPLING_RATE, AUTO_SAVE_RATE, DETAIL_SAMPLING_RATE):
        self.MSR = MOVEMENT_SAMPLING_RATE
        self.ASR = AUTO_SAVE_RATE
        self.DSR = DETAIL_SAMPLING_RATE

        self.last_saved_image = Image.open(io.BytesIO())
        self.capture_count = 0

    def movement_detection(self, image):
        '''
        return True, when movement is detected compare with last image.
        '''
        pass

    def save_image(self, image, img_time):
        '''
        Save image with img_time
        '''
        # duplicate image to local "last image"
        self.last_saved_image = image.copy()

        # save it
        image.save("data/CCTV_data/"+img_time.strftime('%Y-%m-%d_%H:%M:%S')+".jpg")

    def get_image(self, img_time):
        '''
        return image, image_name. If there isnt that file return false, ""
        '''
        pass

    def CCTV_thread(self, image, img_time):
        # if the second is 0, save image.
        if self.capture_count % self.ASR == 0:
            save_image(image, img_time)
        # if second is not 0, detect movement.
        elif self.capture_count % self.MSR == 0:
            pass



