import cv2
import numpy as np
from datetime import datetime
import os
from tqdm import tqdm

class TrimVideo:
    def __init__(self, file : str = None, start : int = 0, end : int = 0, pth : str = None, name : str = None) -> None:
        self.file = file
        self.start = start * 60 # to second
        self.end  = end * 60 # to second
        self.pth = pth
        self.name = name
        self.path = os.path.join(self.pth, self.name)

    def __convert(self, second):
        # min, sec = (seconds // seconds, seconds % 60) 
        # hour, min = (sec // min, min % 60)
        min, sec = divmod(second, 60)
        hour, min = divmod(min, 60)
        return "%02d:%02d:%02d" % (hour,min,sec)

    def Trim(self):
        print("Please Wait Video was Created")
        
        cap = cv2.VideoCapture(self.file)
        fps = cap.get(cv2.CAP_PROP_FPS)

        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        o = "00:00:00"
        origin = datetime.strptime(o, "%H:%M:%S")
        starts = datetime.strptime(self.__convert(self.start), "%H:%M:%S")
        ends = datetime.strptime(self.__convert(self.end), "%H:%M:%S")

        strframe = fps * (starts - origin).total_seconds()
        endframe = fps * (ends - origin).total_seconds()
        pbar = tqdm(total=endframe)
        fourcc = cv2.VideoWriter_fourcc(*'MP42')
        out = cv2.VideoWriter(self.path + '.mp4',fourcc, fps, (w,h))

        counter = 1 #set counter
        while(True):           #while the cap is open
            ret, frame = cap.read()       #read frame
            if frame is None:             #if frame is None
                break  
            
            frame=cv2.resize(frame, (w,h))  #resize the frame
            if counter>=strframe and counter<=endframe:  #check for range of output
                pbar.update(1)
                out.write(frame)  #output 
        
                # print(frame)
            # cv2.imshow("Frame", frame)  #display frame
            # if cv2.waitKey(10) == 27 or counter >= endframe:
            #     break
            counter+=1  #increase counter
            if counter == endframe: #break loop
                pbar.clear()
                break 
        cap.release()  
        cv2.destroyAllWindows()
        print("Finish Created Video")

# test
# if __name__ == "__main__":
#     TrimVideo(file=r"C:\Users\user\Videos\2022-10-11 18-58-29.mkv",end=0.2).Trim()