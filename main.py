import cv2
import joblib
import warnings
import tensorflow as tf
import numpy as np
# from FaceRecognize.Face import GenerateFaceDatabase

# img = cv2.imread(r"D:\Dokumen kuliah\[KULIAH] PROJECT BINA NUSANTARA\SEMESTER 5\Computer Vision\Project\dataset\train\Chris Hemsworth\3.jpg")
# FaceDetection(img).FaceCrop()
# GenerateFaceDatabase("https://youtu.be/yZ31UlUu4CM").Generate()
def Face(image):
    labels = {0: 'Bill Gates',
              1: 'Gema Cita Andika',
              2: 'Jack Ma',
              3: 'Jess No Limit',
              4: 'Jessica Jane',
              5: 'Jokowi',
              6: 'Prambudi',
              7: 'Tara Arts'
            }

    
    warnings.filterwarnings('ignore')
    
    #for ML
    # with open(r'C:\Users\user\Downloads\FaceDetection\Model\Model_Face', 'rb') as file:
    #     mdl = joblib.load(file)

    #for Train Data
    with open(r'C:\Users\user\Downloads\FaceDetection\Model\Train\Train_data', 'rb') as file:
        x_train = joblib.load(file)
    
    with open(r'C:\Users\user\Downloads\FaceDetection\Model\Train\Train_label', 'rb') as file:
        y_train = joblib.load(file)

    # for DEEP LEARNING
    new_model = tf.keras.models.load_model("C:/Users/user/Downloads/FaceDetection/Model/neural_face.h5")

    Face_clasify = cv2.CascadeClassifier("FaceRecognize\FaceClassifier\haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    Faces = Face_clasify.detectMultiScale(gray, 1.6, 6)
 
    if Faces is ():
        print("No detect Image")
        return None

    for (x, y, w, h) in Faces:
        Crop = gray[y:y+h, x:x+w]  
        Facess = cv2.resize(Crop, (64,64))
        Facess = cv2.medianBlur(Facess ,3)
        Facess = Facess / 255.0
        # Facess = cv2.adaptiveThreshold(Facess,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,7,1)
        Facess = Facess.reshape(1,-1)
        predicted = new_model.predict(Facess)
        fcs = labels[np.argmax(predicted[0])]
        # loss, acc = new_model.evaluate(x_train, y_train, verbose=2)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, str(fcs), ((x + w) - w, (y + h) - (h + 10)), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    # return Crop

if __name__ == "__main__":

    cap = cv2.VideoCapture(r"C:\Users\user\Videos\2022-10-11 18-58-29.mkv")
    while True:
        # Read the frame
        ret, images = cap.read()

        Face(images)
        cv2.imshow('Video', images)

        if cv2.waitKey(10) == 27:
            break
    
    