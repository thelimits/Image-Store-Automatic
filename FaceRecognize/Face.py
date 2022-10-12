import cv2
import numpy as np
import pafy
import os 
from FaceRecognize.VideoTrim.Trim import TrimVideo
from tqdm import tqdm

class GenerateFaceDatabase:
    def __init__(self, url : str = None, file : str = None, start : int = 0, end : int = 0) -> None:
        """
            start and end in minutes ===> 1 minutes = 60 seconds
        """
        self.url = url
        self.file = file
        self.start = start 
        self.end = end 
        name = input("Masukan Nama Kamu: ")
        self.MainPath = r"C:\Users\user\Downloads\FaceDetection\FaceRecognize\FaceDatabase"
        self.temp = r"C:\Users\user\Downloads\FaceDetection\FaceRecognize\FaceDatabase\Temp"
        self.Directory = name
        self.path = os.path.join(self.MainPath, self.Directory)
        self.videos = os.path.join(self.temp, self.Directory) + ".mp4"
        self.isExist = os.path.exists(self.videos)
        
        if (self.start == 0 and self.end != 0):
            video = pafy.new(self.url)
            best  = video.getbest(preftype="mp4")
            if self.isExist == False:
                TrimVideo(file=best.url, start=self.start, end=self.end, pth = self.temp, 
                          name = self.Directory).Trim()
        
        try:
            os.makedirs(self.path, exist_ok = True)
            print("Directory '%s' created successfully" % self.Directory)
        except OSError as error:
            print("Directory '%s' can not be created" % self.Directory)
        
    def __FaceCrop(self, image):
        Face_clasify = cv2.CascadeClassifier("FaceRecognize\FaceClassifier\haarcascade_frontalface_default.xml")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        Faces = Face_clasify.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=6, minSize=(50, 50), flags=cv2.CASCADE_SCALE_IMAGE)
        
        if Faces is ():
            print("No detect Image")
            return None
        for (x, y, w, h) in Faces:  
            # cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            Crop = image[y:(y+h), x:(x+w)]
        return Crop

    def Generate(self):
        flag = 0
        dump = 0
        pbar = tqdm(total = 5000)
        while True:
            if self.url is not None:
                if (self.start == 0 and self.end != 0):
                    cap = cv2.VideoCapture(os.path.join(self.temp, self.Directory) + ".mp4")         
                else:
                    video = pafy.new(self.url)
                    best  = video.getbest(preftype="mp4")
                    cap = cv2.VideoCapture(video.url)
                
                image_number = 0
                if flag == 1:
                    image_number = dump

            elif self.url is None:   
                cap = cv2.VideoCapture(0)
                image_number = 0

            if self.file is not None:
                cap = cv2.VideoCapture(self.file)
                image_number = 0
                if flag == 1:
                    image_number = dump
            count = 0
            isclose = 0  
            while (True):
                # Read the frame
                ret, images = cap.read()
                if ret == True:
                    if self.__FaceCrop(images) is not None:
                        image_number += 1
                        faceimages = cv2.resize(self.__FaceCrop(images), (128,128))
                        faceimages = cv2.cvtColor(faceimages, cv2.COLOR_BGR2GRAY)
                        file_path = self.path + "/" + str(image_number) + ".jpg"
                        cv2.imwrite(file_path, faceimages)
                        cv2.putText(faceimages, str(image_number)+ " " + str(flag), (10,50), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

                        # Display
                        cv2.imshow('Video', faceimages)
                        count += 1
                        if count <= 5000:
                            pbar.update(1)
                        if cv2.waitKey(10) == 27 or int(image_number) == 5000:
                            isclose = 1
                            pbar.clear()
                            break
                else:
                    dump = image_number
                    flag = 1
                    break

            if isclose:
                break
        
        # Release the VideoCapture object  
        cap.release()  
        cv2.destroyAllWindows()
        os.remove(self.videos)
        print("Collect Image Is Complete")
