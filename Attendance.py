import csv
import datetime
import time
import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import os
import pandas as pd
from PIL import Image

window = tk.Tk()

window.attributes('-fullscreen', True)

window.title("Attendance System")

window.configure(background='light blue')

x_cord = 75;
y_cord = 20;
checker = 0;

message = tk.Label(window, text="ATTENDANCE MANAGEMENT PORTAL", bg="light blue", fg="blue4", width=30, height=1,
                   font=('Cambria', 35, 'bold'))
message.place(x=265, y=20)

lbl = tk.Label(window, text="Enter Your College ID", width=20, height=3, fg="black", bg="light blue",
               font=('Times New Roman', 20, ' bold '))
lbl.place(x=150 - x_cord, y=200 - y_cord)

txt = tk.Entry(window, width=30, bg="white", fg="blue", font=('Times New Roman', 15, ' bold '))
txt.place(x=160 - x_cord, y=280 - y_cord)

lbl2 = tk.Label(window, text="Enter Your Name", width=20, fg="black", bg="light blue", height=3,
                font=('Times New Roman', 20, ' bold '))
lbl2.place(x=570 - x_cord, y=200 - y_cord)

txt2 = tk.Entry(window, width=30, bg="white", fg="blue", font=('Times New Roman', 15, ' bold '))
txt2.place(x=580 - x_cord, y=280 - y_cord)

lbl3 = tk.Label(window, text="Notification", width=20, fg="black", bg="light blue", height=3,
                font=('Times New Roman', 20, 'bold  '))
lbl3.place(x=1000 - x_cord, y=200 - y_cord)

message = tk.Label(window, text="", fg="red", width=32, height=2, activebackground="white",
                   font=('Times New Roman', 15,))
message.place(x=980 - x_cord, y=280 - y_cord)

lbl3 = tk.Label(window, text="Attendance Status", width=15, height=2, fg="black", bg="light blue",
                font=('Times New Roman', 30, ' bold '))
lbl3.place(x=80, y=570 - y_cord)

message2 = tk.Label(window, text="", fg="red", activeforeground="green", width=65, height=4,
                    font=('times', 15, ' bold '))
message2.place(x=500, y=570 - y_cord)

lbl4 = tk.Label(window, text="STEP 1", width=20, fg="green", bg="light blue", height=2,
                font=('Times New Roman', 20, ' bold '))
lbl4.place(x=140 - x_cord, y=375 - y_cord)

lbl5 = tk.Label(window, text="STEP 2", width=20, fg="green", bg="light blue", height=2,
                font=('Times New Roman', 20, ' bold '))
lbl5.place(x=580 - x_cord, y=375 - y_cord)

lbl6 = tk.Label(window, text="STEP 3", width=20, fg="green", bg="light blue", height=2,
                font=('Times New Roman', 20, ' bold '))
lbl6.place(x=1000 - x_cord, y=375 - y_cord)


def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        pass


def TakeImages():
    Id = (txt.get())
    name = (txt2.get())
    if (isNumber(Id) and name.isalpha()):
        cam = cv2.VideoCapture("0") #ipcam url (if web cam not available) else "0"
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum = sampleNum + 1
                cv2.imwrite("SampleImages\ " + name + "." + Id + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                cv2.imshow('Face Detecting', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 60:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + Id + " Name : " + name
        row = [Id, name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text=res)
    else:
        if (isNumber(name)):
            res = "Enter Alphabetical Name"
            message.configure(text=res)
        if (Id.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text=res)


def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Id = getImagesAndLabels("SampleImages")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained"
    message.configure(text=res)


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids
def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);
    df = pd.read_csv("StudentDetails\StudentDetails.csv")
    cam = cv2.VideoCapture('0') #ipcam url (if webcam nbot available) else '0'
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['Id'] == Id]['Name'].values
                tt = str(Id) + "-" + aa
                #attendance.loc[len()] = [Id, aa, date, attendancetimeStamp]
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]


            else:
                Id = 'Unknown'
                tt = str(Id)
            if (conf > 75):
                noOfFile = len(os.listdir("ImagesUnknown")) + 1
                cv2.imwrite("ImagesUnknown\Image" + str(noOfFile) + ".jpg", im[y:y + h, x:x + w])
            cv2.putText(im, str(tt), (x, y + h), font, 1, (255, 255, 255), 2)
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('im', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fileName = "Attendance\Attendance_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
    attendance.to_csv(fileName, index=False)
    cam.release()
    cv2.destroyAllWindows()
    res = attendance
    message2.configure(text=res)
    res = "Attendance Taken"
    message.configure(text=res)
    tk.messagebox.showinfo('Completed', 'Congratulations ! Your attendance has been marked successfully for the day!!')


def quit_window():
    MsgBox = tk.messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application',
                                       icon='warning')
    if MsgBox == 'yes':
        tk.messagebox.showinfo("Greetings", "Thank You for using our portal. Have a nice day ahead!!")
        window.destroy()

takeImg = tk.Button(window, text="CAPTURE IMAGE", command=TakeImages, fg="white", bg="blue", width=20, height=1,
                    activebackground="light blue", font=('Times New Roman', 15, ' bold '))
takeImg.place(x=180 - x_cord, y=425 - y_cord)
trainImg = tk.Button(window, text="TRAIN IMAGE", command=TrainImages, fg="white", bg="blue", width=20, height=1,
                     activebackground="light blue", font=('Times New Roman', 15, ' bold '))
trainImg.place(x=610 - x_cord, y=425 - y_cord)
trackImg = tk.Button(window, text="MARK ATTENDANCE", command=TrackImages, fg="white", bg="blue", width=20, height=1,
                     activebackground="light blue", font=('Times New Roman', 15, ' bold '))
trackImg.place(x=1040 - x_cord, y=425 - y_cord)
quitWindow = tk.Button(window, text="QUIT", command=quit_window, fg="white", bg="red", width=7, height=1,
                       activebackground="light blue", font=('Times New Roman', 15, ' bold '))
quitWindow.place(x=600, y=720 - y_cord)

copyWrite = tk.Text(window, background=window.cget("background"), borderwidth=0, font=('times', 10, 'italic bold '))
copyWrite.tag_configure("superscript", offset=10)
copyWrite.insert("insert", "Developed by Sadiq Shaikh" + "\u00A9")
copyWrite.configure(state="disabled", fg="black")
copyWrite.pack(side="left")
copyWrite.place(x=1100, y=720)

window.mainloop()
